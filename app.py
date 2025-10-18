"""
Retail Conversational Sales Agent - Main Flask Application
A comprehensive AI-driven sales solution with Master Agent and Worker Agents
"""

from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
import uuid
import json
from datetime import datetime
import logging

from agents.master_sales_agent import MasterSalesAgent
from utils.customer_context import CustomerContextManager
from utils.mock_apis import MockRetailAPIs
from integrations.messaging_coordinator import MessagingCoordinator
from ai_service import get_ai_response, get_product_recommendations, get_cart_summary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
app.secret_key = 'retail-sales-agent-secret-key-2024'
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001'], supports_credentials=True)

# Initialize components
master_agent = MasterSalesAgent()
context_manager = CustomerContextManager()
mock_apis = MockRetailAPIs()
messaging_coordinator = MessagingCoordinator()

@app.route('/')
def index():
    """Serve React app"""
    if os.path.exists('frontend/build/index.html'):
        return send_from_directory('frontend/build', 'index.html')
    else:
        return render_template('index.html')  # Fallback to original template

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve React static files"""
    return send_from_directory('frontend/build/static', filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint for customer interactions"""
    try:
        data = request.json
        message = data.get('message', '')
        channel = data.get('channel', 'web')
        customer_id = data.get('customer_id')
        
        # Generate session ID if not provided
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        
        # Get or create customer context
        if customer_id:
            customer_context = context_manager.get_customer_context(customer_id)
        else:
            customer_context = context_manager.get_anonymous_context(session_id)
        
        # Process message through Master Sales Agent
        response = master_agent.process_message(
            message=message,
            customer_context=customer_context,
            channel=channel,
            session_id=session_id
        )
        
        # Update customer context
        context_manager.update_context(customer_context['customer_id'], {
            'last_interaction': datetime.now().isoformat(),
            'channel': channel,
            'conversation_history': customer_context.get('conversation_history', []) + [
                {'role': 'user', 'message': message, 'timestamp': datetime.now().isoformat()},
                {'role': 'assistant', 'message': response['message'], 'timestamp': datetime.now().isoformat()}
            ]
        })
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'message': 'I apologize, but I encountered an error. Please try again.',
            'error': True
        }), 500

@app.route('/api/customer/<customer_id>/context', methods=['GET'])
def get_customer_context(customer_id):
    """Get customer context for personalization"""
    try:
        context = context_manager.get_customer_context(customer_id)
        return jsonify(context)
    except Exception as e:
        logger.error(f"Error getting customer context: {str(e)}")
        return jsonify({'error': 'Failed to retrieve customer context'}), 500

@app.route('/api/products/search', methods=['POST'])
def search_products():
    """Product search endpoint"""
    try:
        data = request.json
        query = data.get('query', '')
        filters = data.get('filters', {})
        
        products = mock_apis.search_products(query, filters)
        return jsonify({'products': products})
        
    except Exception as e:
        logger.error(f"Error in product search: {str(e)}")
        return jsonify({'error': 'Failed to search products'}), 500

@app.route('/api/inventory/check', methods=['POST'])
def check_inventory():
    """Check product inventory"""
    try:
        data = request.json
        product_id = data.get('product_id')
        store_location = data.get('store_location')
        
        inventory = mock_apis.check_inventory(product_id, store_location)
        return jsonify(inventory)
        
    except Exception as e:
        logger.error(f"Error checking inventory: {str(e)}")
        return jsonify({'error': 'Failed to check inventory'}), 500

@app.route('/api/promotions', methods=['GET'])
def get_promotions():
    """Get current promotions"""
    try:
        customer_id = request.args.get('customer_id')
        promotions = mock_apis.get_promotions(customer_id)
        return jsonify({'promotions': promotions})
        
    except Exception as e:
        logger.error(f"Error getting promotions: {str(e)}")
        return jsonify({'error': 'Failed to get promotions'}), 500

@app.route('/api/order/create', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.json
        order = mock_apis.create_order(data)
        return jsonify(order)
        
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return jsonify({'error': 'Failed to create order'}), 500

@app.route('/api/payment/process', methods=['POST'])
def process_payment():
    """Process payment"""
    try:
        data = request.json
        payment_result = mock_apis.process_payment(data)
        return jsonify(payment_result)
        
    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        return jsonify({'error': 'Failed to process payment'}), 500

@app.route('/api/analytics/dashboard', methods=['GET'])
def analytics_dashboard():
    """Analytics dashboard data"""
    try:
        analytics = mock_apis.get_analytics()
        return jsonify(analytics)
        
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        return jsonify({'error': 'Failed to get analytics'}), 500

# WhatsApp webhook endpoint
@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages"""
    try:
        # Process WhatsApp webhook
        webhook_data = messaging_coordinator.process_webhook('whatsapp', request.form.to_dict())
        
        if webhook_data.get('error'):
            logger.error(f"WhatsApp webhook error: {webhook_data['error']}")
            return '', 400
        
        user_id = webhook_data['user_id']
        message = webhook_data['message']
        
        # Get customer context
        customer_context = context_manager.get_customer_context(user_id)
        
        # Process message through Master Sales Agent
        response = master_agent.process_message(
            message=message,
            customer_context=customer_context,
            channel='whatsapp',
            session_id=user_id
        )
        
        # Format response for WhatsApp
        formatted_response = messaging_coordinator.format_response_for_platform('whatsapp', response)
        
        # Send response back to WhatsApp
        from_number = webhook_data['channel_data']['from_number']
        send_result = messaging_coordinator.whatsapp.send_message(from_number, formatted_response)
        
        # Send products if available
        if response.get('products'):
            messaging_coordinator.whatsapp.send_product_list(from_number, response['products'])
        
        # Send cart summary if available
        if response.get('cart'):
            messaging_coordinator.whatsapp.send_cart_summary(from_number, response['cart'])
        
        # Update customer context
        context_manager.update_context(user_id, {
            'last_interaction': datetime.now().isoformat(),
            'channel': 'whatsapp',
            'conversation_history': customer_context.get('conversation_history', []) + [
                {'role': 'user', 'message': message, 'timestamp': datetime.now().isoformat()},
                {'role': 'assistant', 'message': response['message'], 'timestamp': datetime.now().isoformat()}
            ]
        })
        
        return '', 200
        
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {str(e)}")
        return '', 500

# Telegram webhook endpoint
@app.route('/webhook/telegram', methods=['POST'])
def telegram_webhook():
    """Handle incoming Telegram messages"""
    try:
        import asyncio
        
        # Process Telegram webhook
        webhook_data = messaging_coordinator.process_webhook('telegram', request.json)
        
        if webhook_data.get('error'):
            logger.error(f"Telegram webhook error: {webhook_data['error']}")
            return '', 400
        
        user_id = webhook_data['user_id']
        chat_id = webhook_data.get('chat_id', user_id)
        message = webhook_data['message']
        message_type = webhook_data.get('message_type', 'text')
        
        # Handle callback queries differently
        if message_type == 'callback':
            # Handle button callbacks
            if message == 'start_shopping':
                response_message = "🛍️ Great! What are you looking for today? You can search for products, browse categories, or ask for recommendations."
            elif message == 'get_recommendations':
                response_message = "🎯 Let me get some personalized recommendations for you based on popular products..."
            elif message == 'view_deals':
                response_message = "🏷️ Here are today's best deals and promotions..."
            elif message == 'view_cart':
                # Get customer context and show cart
                customer_context = context_manager.get_customer_context(user_id)
                cart_items = customer_context.get('cart', [])
                asyncio.run(messaging_coordinator.send_cart_summary('telegram', chat_id, cart_items))
                return '', 200
            else:
                response_message = f"Processing your selection: {message}"
            
            # Send simple response for callbacks
            asyncio.run(messaging_coordinator.send_message('telegram', chat_id, response_message))
            return '', 200
        
        # Get customer context
        customer_context = context_manager.get_customer_context(user_id)
        
        # Process message through Master Sales Agent
        response = master_agent.process_message(
            message=message,
            customer_context=customer_context,
            channel='telegram',
            session_id=user_id
        )
        
        # Format response for Telegram
        formatted_response = messaging_coordinator.format_response_for_platform('telegram', response)
        
        # Send response back to Telegram
        asyncio.run(messaging_coordinator.send_message('telegram', chat_id, formatted_response))
        
        # Send products if available
        if response.get('products'):
            asyncio.run(messaging_coordinator.send_product_list('telegram', chat_id, response['products']))
        
        # Send cart summary if available
        if response.get('cart'):
            asyncio.run(messaging_coordinator.send_cart_summary('telegram', chat_id, response['cart']))
        
        # Update customer context
        context_manager.update_context(user_id, {
            'last_interaction': datetime.now().isoformat(),
            'channel': 'telegram',
            'conversation_history': customer_context.get('conversation_history', []) + [
                {'role': 'user', 'message': message, 'timestamp': datetime.now().isoformat()},
                {'role': 'assistant', 'message': response['message'], 'timestamp': datetime.now().isoformat()}
            ]
        })
        
        return '', 200
        
    except Exception as e:
        logger.error(f"Telegram webhook error: {str(e)}")
        return '', 500

# Messaging platform status endpoint
@app.route('/api/messaging/status', methods=['GET'])
def messaging_status():
    """Get status of messaging platforms"""
    try:
        status = messaging_coordinator.get_platform_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting messaging status: {str(e)}")
        return jsonify({'error': 'Failed to get messaging status'}), 500

# Setup instructions endpoint
@app.route('/api/messaging/setup', methods=['GET'])
def messaging_setup():
    """Get setup instructions for messaging platforms"""
    try:
        instructions = messaging_coordinator.get_setup_instructions()
        return jsonify(instructions)
    except Exception as e:
        logger.error(f"Error getting setup instructions: {str(e)}")
        return jsonify({'error': 'Failed to get setup instructions'}), 500

# Telegram webhook setup endpoint
@app.route('/webhook/telegram/set', methods=['POST'])
def set_telegram_webhook():
    """Set Telegram webhook URL"""
    try:
        import asyncio
        
        data = request.json
        webhook_url = data.get('webhook_url', f"{request.host_url}webhook/telegram")
        
        result = asyncio.run(messaging_coordinator.telegram.set_webhook(webhook_url))
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error setting Telegram webhook: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🛍️ Starting Retail Conversational Sales Agent...")
    print("📱 Multi-channel support: Web, Mobile, WhatsApp, Telegram, In-store")
    print("🤖 AI Agents: Master Sales + 5 Worker Agents")
    print("💬 Messaging: WhatsApp & Telegram integration ready")
    print("🌐 Access the application at: http://localhost:5000")
    print("\n📋 Setup Instructions:")
    print("   WhatsApp: Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER")
    print("   Telegram: Set TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_URL")
    print("   Webhooks: /webhook/whatsapp, /webhook/telegram")
    app.run(debug=True, host='0.0.0.0', port=5000)
