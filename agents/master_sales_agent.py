"""
Master Sales Agent - Orchestrates the entire sales conversation
Coordinates with Worker Agents to provide seamless customer experience
Now powered by Google Gemini AI
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any

from .worker_agents.inventory_agent import InventoryAgent
from .worker_agents.recommendation_agent import RecommendationAgent
from .worker_agents.promotion_agent import PromotionAgent
from .worker_agents.payment_agent import PaymentAgent
from .worker_agents.order_agent import OrderAgent
from .worker_agents.fulfillment_agent import FulfillmentAgent
from .worker_agents.loyalty_offers_agent import LoyaltyOffersAgent
from .worker_agents.post_purchase_agent import PostPurchaseAgent
from .worker_agents.reserve_tryon_agent import ReserveTryOnAgent
from .edge_case_handler import EdgeCaseHandler
from .sales_psychology import SalesPsychology
from .agent_registry import AgentRegistry, initialize_default_agents
from ai_service import get_ai_response, get_product_recommendations
from utils.session_continuity_manager import SessionContinuityManager

logger = logging.getLogger(__name__)

class MasterSalesAgent:
    def __init__(self):
        """Initialize Master Sales Agent with all Worker Agents"""
        # Core Worker Agents
        self.inventory_agent = InventoryAgent()
        self.recommendation_agent = RecommendationAgent()
        self.promotion_agent = PromotionAgent()
        self.payment_agent = PaymentAgent()
        self.order_agent = OrderAgent()
        
        # Extended Worker Agents
        self.fulfillment_agent = FulfillmentAgent()
        self.loyalty_offers_agent = LoyaltyOffersAgent()
        self.post_purchase_agent = PostPurchaseAgent()
        self.reserve_tryon_agent = ReserveTryOnAgent()
        
        # Advanced Features
        self.edge_case_handler = EdgeCaseHandler()
        self.sales_psychology = SalesPsychology()
        self.session_manager = SessionContinuityManager()
        self.agent_registry = initialize_default_agents()
        
        # Conversation states
        self.conversation_states = {}
        
        # Enhanced intent patterns for natural language understanding
        self.intent_patterns = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'product_search': ['looking for', 'need', 'want', 'search', 'find', 'show me'],
            'product_info': ['tell me about', 'details', 'specifications', 'features', 'price'],
            'availability': ['available', 'in stock', 'store', 'inventory', 'check'],
            'recommendations': ['recommend', 'suggest', 'similar', 'alternatives', 'what else'],
            'promotions': ['discount', 'offer', 'deal', 'promotion', 'sale', 'coupon'],
            'purchase': ['buy', 'purchase', 'order', 'checkout', 'add to cart'],
            'payment': ['pay', 'payment', 'card', 'cash', 'paypal', 'wallet'],
            'help': ['help', 'support', 'assistance', 'confused', 'how to'],
            'goodbye': ['bye', 'goodbye', 'thank you', 'thanks', 'done', 'exit'],
            'reserve_tryon': ['reserve', 'try on', 'tryon', 'fitting room', 'in-store', 'pick up'],
            'objection': ['too expensive', 'not sure', 'thinking about it', 'maybe later', 'compare'],
            'gift': ['gift', 'present', 'wrap', 'gift message'],
            'personal_shopper': ['personal shopper', 'help me shop', 'style advice', 'what should i buy'],
            'channel_switch': ['show on whatsapp', 'show on telegram', 'show on mobile', 'switch to whatsapp', 
                             'switch to telegram', 'switch to mobile', 'open in whatsapp', 'open in telegram',
                             'continue on whatsapp', 'continue on telegram', 'continue on mobile', 'use whatsapp',
                             'use telegram', 'use mobile app', 'show in app', 'open app']
        }

    def process_message(self, message: str, customer_context: Dict, channel: str, session_id: str) -> Dict:
        """
        Main message processing logic
        Determines intent and coordinates with appropriate Worker Agents
        """
        try:
            # Initialize conversation state if new session
            if session_id not in self.conversation_states:
                self.conversation_states[session_id] = {
                    'current_intent': None,
                    'context': {},
                    'cart': [],
                    'step': 'greeting'
                }
            
            conversation_state = self.conversation_states[session_id]
            
            # Detect intent from message
            intent = self._detect_intent(message.lower())
            conversation_state['current_intent'] = intent
            
            # Generate personalized response based on intent and context
            response = self._generate_response(
                intent, message, customer_context, conversation_state, channel
            )
            
            # Update conversation state
            self.conversation_states[session_id] = conversation_state
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                'message': "I apologize for the confusion. How can I help you with your shopping today?",
                'intent': 'error',
                'suggestions': ['Show me products', 'Check promotions', 'Help me find something']
            }

    def _detect_intent(self, message: str) -> str:
        """Detect customer intent from message"""
        message_lower = message.lower()
        
        # Check for greeting first (only if it's a short greeting message)
        greeting_words = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(word == message_lower.strip() or message_lower.strip().startswith(word + ' ') for word in greeting_words):
            # Only return greeting if message is short (likely just a greeting)
            if len(message_lower.split()) <= 3:
                return 'greeting'
        
        # Check for specific intents (excluding greeting which we already handled)
        for intent, patterns in self.intent_patterns.items():
            if intent == 'greeting':
                continue  # Skip greeting, we handled it above
            if any(pattern in message_lower for pattern in patterns):
                return intent
        
        # Check if message contains product-related keywords
        product_keywords = ['shirt', 'shoe', 'headphone', 'watch', 'speaker', 'backpack', 
                          'electronics', 'clothing', 'footwear', 'accessories', 'phone',
                          'laptop', 'jeans', 'jacket', 'dress', 'boots', 'sneakers']
        if any(keyword in message_lower for keyword in product_keywords):
            return 'product_search'
        
        # Default to product search if no specific intent detected
        return 'product_search'

    def _generate_response(self, intent: str, message: str, customer_context: Dict, 
                          conversation_state: Dict, channel: str) -> Dict:
        """Generate appropriate response based on intent"""
        
        customer_name = customer_context.get('name', 'there')
        
        if intent == 'greeting':
            return self._handle_greeting(customer_name, customer_context, channel)
        
        elif intent == 'product_search':
            return self._handle_product_search(message, customer_context, conversation_state)
        
        elif intent == 'product_info':
            return self._handle_product_info(message, customer_context)
        
        elif intent == 'availability':
            return self._handle_availability_check(message, customer_context)
        
        elif intent == 'recommendations':
            return self._handle_recommendations(customer_context, conversation_state)
        
        elif intent == 'promotions':
            return self._handle_promotions(customer_context)
        
        elif intent == 'purchase':
            return self._handle_purchase(message, customer_context, conversation_state)
        
        elif intent == 'payment':
            return self._handle_payment(message, customer_context, conversation_state)
        
        elif intent == 'help':
            return self._handle_help(channel)
        
        elif intent == 'goodbye':
            return self._handle_goodbye(customer_name, conversation_state)
        
        elif intent == 'reserve_tryon':
            return self._handle_reserve_tryon(message, customer_context, conversation_state)
        
        elif intent == 'objection':
            return self._handle_objection(message, customer_context, conversation_state)
        
        elif intent == 'gift':
            return self._handle_gift_options(message, customer_context, conversation_state)
        
        elif intent == 'personal_shopper':
            return self._handle_personal_shopper(message, customer_context, conversation_state)
        
        else:
            # Try modular agent registry first
            registry_response = self.agent_registry.route_request(intent, message, customer_context)
            if registry_response.get('handled_by'):
                return registry_response
            
            return self._handle_general_query(message, customer_context)

    def _handle_greeting(self, customer_name: str, customer_context: Dict, channel: str) -> Dict:
        """Handle greeting messages"""
        channel_specific = {
            'web': "Welcome to our online store!",
            'mobile': "Welcome to our mobile app!",
            'whatsapp': "Hello! Thanks for reaching out on WhatsApp!",
            'instore': "Welcome to our store!",
            'voice': "Hello! I'm your voice shopping assistant!"
        }
        
        greeting = channel_specific.get(channel, "Hello!")
        
        # Personalize based on customer history
        if customer_context.get('purchase_history'):
            recent_category = customer_context['purchase_history'][0].get('category', 'products')
            message = f"{greeting} Hi {customer_name}! I see you've shopped with us before. Looking for more {recent_category} today, or something different?"
        else:
            message = f"{greeting} Hi {customer_name}! I'm your personal shopping assistant. I can help you find products, check availability, and even process your order. What are you looking for today?"
        
        return {
            'message': message,
            'intent': 'greeting',
            'suggestions': [
                'Show me new arrivals',
                'I\'m looking for electronics',
                'What promotions do you have?',
                'Help me find a gift'
            ],
            'quick_actions': [
                {'text': 'Browse Categories', 'action': 'show_categories'},
                {'text': 'Current Deals', 'action': 'show_promotions'}
            ]
        }

    def _handle_product_search(self, message: str, customer_context: Dict, conversation_state: Dict) -> Dict:
        """Handle product search requests using Gemini AI"""
        # Extract search terms from message
        search_query = self._extract_search_terms(message)
        customer_name = customer_context.get('name', 'there')
        
        # Get products from Recommendation Agent
        products = self.recommendation_agent.search_products(
            query=search_query,
            customer_preferences=customer_context.get('preferences', {}),
            purchase_history=customer_context.get('purchase_history', [])
        )
        
        # Use Gemini AI to generate intelligent product recommendations
        if products:
            conversation_state['context']['last_search'] = products
            conversation_state['context']['last_product_id'] = products[0]['id']
            
            # Get AI-powered recommendation response with full context
            ai_response = get_product_recommendations(message, products)
            
            # Check availability for top products
            for product in products[:3]:
                availability = self.inventory_agent.check_availability(
                    product['id'], 
                    customer_context.get('location', 'online')
                )
                product['availability'] = availability
            
            # Generate dynamic suggestions based on products
            suggestions = [
                f'Tell me about {products[0]["name"]}',
                'Show me more options',
                f'Add {products[0]["name"]} to cart',
                'Check store availability'
            ]
            
            # Use AI-generated message or create a dynamic one
            ai_message = ai_response.get('message', '')
            if not ai_message or len(ai_message) < 50:
                # Fallback to dynamic message generation
                ai_message = f"Great choice, {customer_name}! I found {len(products)} perfect match{'es' if len(products) > 1 else ''} for '{search_query}'.\n\n"
                ai_message += f"🌟 **{products[0]['name']}** - ${products[0]['price']:.2f}\n"
                ai_message += f"{products[0]['description']}\n"
                ai_message += f"⭐ Rating: {products[0].get('rating', 4.5)}/5 ({products[0].get('reviews', 0)} reviews)\n\n"
                if len(products) > 1:
                    ai_message += f"I also found {len(products) - 1} more option{'s' if len(products) > 2 else ''} that might interest you. Would you like to see them?"
            
            return {
                'message': ai_message,
                'intent': 'product_search',
                'suggestions': suggestions,
                'products': products[:3],
                'type': ai_response.get('type', 'recommendation')
            }
        else:
            # Use Gemini to generate helpful response for no results
            context = {
                'customer_name': customer_context.get('name', 'there'),
                'search_query': search_query
            }
            
            ai_message = get_ai_response(
                f"The customer searched for '{search_query}' but we don't have exact matches. Help them find alternatives or browse categories.",
                context
            )
            
            suggestions = [
                'Show me similar products',
                'Browse categories',
                'Try a different search',
                'Speak to a human agent'
            ]
            
            return {
                'message': ai_message,
                'intent': 'product_search',
                'suggestions': suggestions,
                'products': []
            }

    def _handle_availability_check(self, message: str, customer_context: Dict) -> Dict:
        """Handle inventory/availability checks"""
        # Extract product reference from message or conversation context
        product_id = self._extract_product_reference(message)
        location = customer_context.get('location', 'online')
        
        if product_id:
            availability = self.inventory_agent.check_availability(product_id, location)
            
            if availability['available']:
                message = f"✅ Good news! This item is available. We have {availability['stock_level']} in stock."
                if location != 'online':
                    message += f" You can pick it up at our {location} store or have it delivered."
                
                suggestions = [
                    'Add to cart',
                    'Reserve for pickup',
                    'Check other locations',
                    'See similar products'
                ]
            else:
                # Use edge case handler for out-of-stock scenarios
                product = self._get_product_details(product_id)
                out_of_stock_response = self.edge_case_handler.handle_out_of_stock(
                    product, customer_context
                )
                
                message = out_of_stock_response['message']
                suggestions = out_of_stock_response.get('suggestions', [
                    'Show similar products',
                    'Get notified when back in stock',
                    'Browse alternatives',
                    'Continue shopping'
                ])
        else:
            message = "I'd be happy to check availability for you! Which product are you interested in?"
            suggestions = [
                'Check the last product I viewed',
                'Search for a specific item',
                'Browse categories',
                'Show me what\'s in stock'
            ]
        
        return {
            'message': message,
            'intent': 'availability',
            'suggestions': suggestions
        }

    def _handle_recommendations(self, customer_context: Dict, conversation_state: Dict) -> Dict:
        """Handle recommendation requests"""
        recommendations = self.recommendation_agent.get_personalized_recommendations(
            customer_context.get('preferences', {}),
            customer_context.get('purchase_history', []),
            conversation_state.get('context', {})
        )
        
        if recommendations:
            message = "Based on your preferences and shopping history, I think you'll love these:\n\n"
            
            for i, product in enumerate(recommendations[:3], 1):
                message += f"{i}. **{product['name']}** - ${product['price']}\n"
                message += f"   {product['reason']}\n\n"
            
            message += "Would you like to see more details about any of these?"
            
            suggestions = [
                f'Tell me about {recommendations[0]["name"]}',
                'Show me more recommendations',
                'Add to cart',
                'Check availability'
            ]
        else:
            message = "Let me learn more about your preferences to give you better recommendations. What type of products are you usually interested in?"
            suggestions = [
                'Electronics',
                'Fashion & Clothing',
                'Home & Garden',
                'Sports & Outdoors'
            ]
        
        return {
            'message': message,
            'intent': 'recommendations',
            'suggestions': suggestions,
            'products': recommendations[:3] if recommendations else []
        }

    def _handle_promotions(self, customer_context: Dict) -> Dict:
        """Handle promotion inquiries"""
        promotions = self.promotion_agent.get_applicable_promotions(
            customer_context.get('customer_id'),
            customer_context.get('membership_tier', 'regular')
        )
        
        if promotions:
            message = "🎉 Great news! Here are the current promotions available to you:\n\n"
            
            for promo in promotions[:3]:
                message += f"**{promo['title']}**\n"
                message += f"{promo['description']}\n"
                message += f"Valid until: {promo['valid_until']}\n\n"
            
            message += "Would you like to shop these deals or see products that qualify?"
            
            suggestions = [
                'Shop these deals',
                'See qualifying products',
                'Apply promo code',
                'Continue shopping'
            ]
        else:
            message = "I don't see any specific promotions for you right now, but we often have great deals! Let me check what's on sale..."
            suggestions = [
                'Show me sale items',
                'Sign up for deal alerts',
                'Browse clearance',
                'Continue shopping'
            ]
        
        return {
            'message': message,
            'intent': 'promotions',
            'suggestions': suggestions,
            'promotions': promotions
        }

    def _handle_purchase(self, message: str, customer_context: Dict, conversation_state: Dict) -> Dict:
        """Handle purchase/checkout requests"""
        cart = conversation_state.get('cart', [])
        
        if not cart:
            # Try to add product from context
            product_id = self._extract_product_reference(message)
            if product_id:
                # Add to cart
                product = self._get_product_details(product_id)
                if product:
                    cart.append(product)
                    conversation_state['cart'] = cart
                    message_text = f"Great! I've added {product['name']} to your cart. Ready to checkout?"
                else:
                    message_text = "I'd be happy to help you purchase something! What would you like to buy?"
            else:
                message_text = "I'd be happy to help you purchase something! What would you like to buy?"
        else:
            # Show cart summary
            total = sum(item['price'] for item in cart)
            message_text = f"Here's your cart:\n\n"
            
            for item in cart:
                message_text += f"• {item['name']} - ${item['price']}\n"
            
            message_text += f"\n**Total: ${total:.2f}**\n\n"
            message_text += "Ready to proceed to checkout?"
        
        suggestions = [
            'Proceed to checkout',
            'Add more items',
            'Apply promo code',
            'Remove items'
        ] if cart else [
            'Show me products',
            'Add items to cart',
            'Browse categories',
            'See recommendations'
        ]
        
        return {
            'message': message_text,
            'intent': 'purchase',
            'suggestions': suggestions,
            'cart': cart
        }

    def _handle_payment(self, message: str, customer_context: Dict, conversation_state: Dict) -> Dict:
        """Handle payment processing"""
        cart = conversation_state.get('cart', [])
        
        if not cart:
            return {
                'message': "Your cart is empty. Please add some items before proceeding to payment.",
                'intent': 'payment',
                'suggestions': ['Browse products', 'Show recommendations', 'View promotions']
            }
        
        # Process payment through Payment Agent
        payment_result = self.payment_agent.process_payment({
            'customer_id': customer_context.get('customer_id'),
            'cart': cart,
            'payment_method': 'default'  # In real implementation, extract from message
        })
        
        if payment_result['success']:
            # Create order through Order Agent
            order = self.order_agent.create_order({
                'customer_id': customer_context.get('customer_id'),
                'items': cart,
                'payment_id': payment_result['payment_id'],
                'total': payment_result['amount']
            })
            
            # Clear cart
            conversation_state['cart'] = []
            
            message = f"🎉 Payment successful! Your order #{order['order_id']} has been confirmed.\n\n"
            message += f"Total: ${payment_result['amount']:.2f}\n"
            message += f"Estimated delivery: {order['estimated_delivery']}\n\n"
            message += "You'll receive a confirmation email shortly. Is there anything else I can help you with?"
            
            suggestions = [
                'Track my order',
                'Continue shopping',
                'Rate my experience',
                'Contact support'
            ]
        else:
            # Use edge case handler for payment failures
            retry_count = conversation_state.get('payment_retry_count', 0)
            
            payment_data = {
                'customer_name': customer_context.get('name', 'there'),
                'amount': sum(item['price'] for item in cart),
                'payment_method': 'card'
            }
            
            failure_response = self.edge_case_handler.handle_payment_failure(
                payment_data,
                payment_result.get('error', 'Unknown error'),
                retry_count
            )
            
            # Update retry count
            conversation_state['payment_retry_count'] = failure_response.get('retry_count', retry_count + 1)
            
            message = failure_response['message']
            suggestions = failure_response.get('suggestions', [
                'Try again',
                'Use different payment method',
                'Contact support',
                'Save cart for later'
            ])
        
        return {
            'message': message,
            'intent': 'payment',
            'suggestions': suggestions
        }

    def _handle_help(self, channel: str) -> Dict:
        """Handle help requests"""
        message = "I'm here to help! Here's what I can do for you:\n\n"
        message += "🔍 **Search & Discovery**: Find products, get recommendations\n"
        message += "📦 **Inventory**: Check availability and store locations\n"
        message += "💰 **Promotions**: Show current deals and discounts\n"
        message += "🛒 **Shopping**: Add to cart, checkout, and payment\n"
        message += "📱 **Multi-channel**: Available on web, mobile, WhatsApp, and in-store\n\n"
        message += "Just tell me what you're looking for in natural language!"
        
        suggestions = [
            'Find me a product',
            'Show current promotions',
            'Check my cart',
            'Browse categories'
        ]
        
        return {
            'message': message,
            'intent': 'help',
            'suggestions': suggestions
        }

    def _handle_goodbye(self, customer_name: str, conversation_state: Dict) -> Dict:
        """Handle goodbye messages"""
        cart = conversation_state.get('cart', [])
        
        if cart:
            message = f"Thanks for shopping with us, {customer_name}! 👋\n\n"
            message += f"Don't forget - you have {len(cart)} item(s) in your cart. "
            message += "I've saved them for you. Come back anytime to complete your purchase!"
        else:
            message = f"Thanks for visiting, {customer_name}! 👋 It was great helping you today. "
            message += "Feel free to come back anytime - I'll be here to assist you!"
        
        suggestions = [
            'Complete my purchase',
            'Save items for later',
            'Browse more products',
            'Get deal notifications'
        ] if cart else [
            'Start shopping again',
            'Get deal notifications',
            'Browse categories',
            'Rate my experience'
        ]
        
        return {
            'message': message,
            'intent': 'goodbye',
            'suggestions': suggestions
        }

    def _handle_general_query(self, message: str, customer_context: Dict) -> Dict:
        """Handle general queries using Gemini AI"""
        # Build context for Gemini
        context = {
            'customer_name': customer_context.get('name', 'there'),
            'previous_messages': customer_context.get('conversation_history', [])[-3:],
            'cart_items': customer_context.get('cart', [])
        }
        
        # Get AI response for the general query
        ai_message = get_ai_response(message, context)
        
        suggestions = [
            'Show me popular products',
            'Browse by category',
            'What deals do you have?',
            'Help me find something specific'
        ]
        
        return {
            'message': ai_message,
            'intent': 'general',
            'suggestions': suggestions
        }

    def _handle_reserve_tryon(self, message: str, customer_context: Dict, conversation_state: Dict) -> Dict:
        """Handle reserve for try-on requests"""
        customer_name = customer_context.get('name', 'there')
        
        # Check if customer wants to reserve a specific product
        if 'reserve' in message.lower() or 'try on' in message.lower():
            # Get nearby stores
            stores_response = self.reserve_tryon_agent.get_nearby_stores(
                customer_location=customer_context.get('location'),
                product_id=conversation_state.get('context', {}).get('last_product_id')
            )
            
            message_text = f"Great idea, {customer_name}! " + stores_response['message']
            message_text += "\n\nWould you like to reserve this item for try-on at one of these locations?"
            
            return {
                'message': message_text,
                'intent': 'reserve_tryon',
                'stores': stores_response.get('stores', []),
                'suggestions': [
                    'Reserve at nearest store',
                    'Schedule try-on appointment',
                    'Buy online, pick up in-store',
                    'Get directions'
                ]
            }
        
        # General inquiry about try-on options
        return {
            'message': f"Absolutely, {customer_name}! We offer several convenient options:\n\n"
                      "🏪 **Reserve for Try-On**: Hold items at your nearest store\n"
                      "📦 **Buy Online, Pick Up In-Store** (BOPIS): Order now, pick up today\n"
                      "👗 **Personal Shopping**: Book a stylist appointment\n"
                      "🏠 **Try at Home**: Free returns within 30 days\n\n"
                      "Which option interests you?",
            'intent': 'reserve_tryon',
            'suggestions': [
                'Reserve for try-on',
                'Buy online, pick up in-store',
                'Schedule personal shopping',
                'Try at home with free returns'
            ]
        }
    
    def _handle_objection(self, message: str, customer_context: Dict, conversation_state: Dict) -> Dict:
        """Handle customer objections using sales psychology"""
        customer_name = customer_context.get('name', 'there')
        
        # Detect objection type
        objection_type = 'price' if any(word in message.lower() for word in ['expensive', 'price', 'cost']) else \
                        'quality' if any(word in message.lower() for word in ['quality', 'good', 'worth']) else \
                        'timing' if any(word in message.lower() for word in ['later', 'think', 'decide']) else \
                        'comparison' if any(word in message.lower() for word in ['compare', 'other', 'alternative']) else \
                        'uncertainty'
        
        # Use sales psychology to handle objection
        objection_response = self.sales_psychology.handle_objection(
            objection_type, message, customer_context
        )
        
        # Add rapport building
        rapport_message = self.sales_psychology.build_rapport(customer_context, 
                                                              customer_context.get('conversation_history', []))
        
        return {
            'message': rapport_message + "\n\n" + objection_response['message'],
            'intent': 'objection',
            'objection_type': objection_type,
            'suggestions': objection_response.get('suggestions', [])
        }
    
    def _handle_gift_options(self, message: str, customer_context: Dict, conversation_state: Dict) -> Dict:
        """Handle gift-related requests through modular agent"""
        # Route to Gift Wrapping Agent through registry
        return self.agent_registry.route_request('gift', message, customer_context)
    
    def _handle_personal_shopper(self, message: str, customer_context: Dict, conversation_state: Dict) -> Dict:
        """Handle personal shopping requests"""
        # Route to Personal Shopper Agent through registry
        return self.agent_registry.route_request('personal_shopper', message, customer_context)

    # Helper methods
    def _handle_channel_switch(self, message: str, customer_context: Dict, current_channel: str) -> Dict:
        """Handle channel switching requests"""
        message_lower = message.lower()
        customer_name = customer_context.get('name', 'there')
        
        # Detect target channel
        target_channel = None
        if 'whatsapp' in message_lower:
            target_channel = 'whatsapp'
            channel_name = 'WhatsApp'
        elif 'telegram' in message_lower:
            target_channel = 'telegram'
            channel_name = 'Telegram'
        elif 'mobile' in message_lower or 'app' in message_lower:
            target_channel = 'mobile'
            channel_name = 'Mobile App'
        elif 'web' in message_lower or 'browser' in message_lower:
            target_channel = 'web'
            channel_name = 'Web Chat'
        elif 'store' in message_lower or 'kiosk' in message_lower:
            target_channel = 'in-store'
            channel_name = 'In-Store Kiosk'
        elif 'voice' in message_lower:
            target_channel = 'voice'
            channel_name = 'Voice Assistant'
        
        if target_channel:
            # Generate channel switch response
            response_message = f"Great idea, {customer_name}! You can continue shopping on {channel_name}.\n\n"
            response_message += f"✅ **Your cart and conversation are automatically synced**\n"
            response_message += f"✅ All your items are preserved\n"
            response_message += f"✅ Your preferences are saved\n\n"
            
            if target_channel == 'whatsapp':
                response_message += "📱 To continue on WhatsApp:\n"
                response_message += "1. Message us at: +1 (415) 523-8886\n"
                response_message += "2. Your cart will be waiting for you!\n"
                response_message += "3. Complete your purchase seamlessly\n\n"
                response_message += "💡 Tip: Save our number for quick shopping anytime!"
            elif target_channel == 'telegram':
                response_message += "✈️ To continue on Telegram:\n"
                response_message += "1. Search for our bot: @YourRetailBot\n"
                response_message += "2. Start a chat with /start\n"
                response_message += "3. Your cart will be synced automatically!\n\n"
                response_message += "💡 Tip: Pin our bot for easy access!"
            elif target_channel == 'mobile':
                response_message += "📱 To continue on Mobile App:\n"
                response_message += "1. Download our app from App Store or Google Play\n"
                response_message += "2. Log in with your customer ID\n"
                response_message += "3. Your cart will be there waiting!\n\n"
                response_message += "💡 Tip: Enable notifications for exclusive mobile deals!"
            elif target_channel == 'in-store':
                response_message += "🏪 To continue in-store:\n"
                response_message += "1. Visit any of our store locations\n"
                response_message += "2. Use the in-store kiosk\n"
                response_message += "3. Enter your customer ID or phone number\n"
                response_message += "4. Your cart will be loaded instantly!\n\n"
                response_message += "💡 Tip: You can also reserve items for in-store pickup!"
            
            return {
                'message': response_message,
                'intent': 'channel_switch',
                'target_channel': target_channel,
                'suggestions': [
                    f'Continue shopping here',
                    'View my cart',
                    'Check out now',
                    'Tell me about store locations'
                ]
            }
        else:
            # Generic channel switching info
            return {
                'message': f"Hi {customer_name}! You can shop with us across multiple channels:\n\n"
                          "🖥️ **Web Chat** - Right here in your browser\n"
                          "📱 **Mobile App** - Download from App Store or Google Play\n"
                          "💬 **WhatsApp** - Message us at +1 (415) 523-8886\n"
                          "✈️ **Telegram** - Find our bot @YourRetailBot\n"
                          "🏪 **In-Store Kiosk** - Visit any store location\n"
                          "🎤 **Voice Assistant** - Use voice commands\n\n"
                          "Your cart and conversation are automatically synced across all channels!",
                'intent': 'channel_switch',
                'suggestions': [
                    'Show on WhatsApp',
                    'Show on Telegram',
                    'Show on Mobile',
                    'Continue shopping here'
                ]
            }

    def _extract_search_terms(self, message: str) -> str:
        """Extract search terms from natural language message"""
        # Remove common words and extract meaningful terms
        stop_words = ['i', 'am', 'looking', 'for', 'need', 'want', 'show', 'me', 'find', 'a', 'an', 'the']
        words = message.lower().split()
        search_terms = [word for word in words if word not in stop_words and len(word) > 2]
        return ' '.join(search_terms)

    def _extract_product_reference(self, message: str) -> str:
        """Extract product reference from message or conversation context"""
        # In a real implementation, this would use NLP to extract product references
        # For now, return a mock product ID
        return "PROD001" if any(word in message.lower() for word in ['this', 'that', 'it']) else None

    def _get_product_details(self, product_id: str) -> Dict:
        """Get product details by ID"""
        # Mock product details - in real implementation, fetch from database
        return {
            'id': product_id,
            'name': 'Sample Product',
            'price': 99.99,
            'category': 'Electronics'
        }
