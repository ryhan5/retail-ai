"""
WhatsApp Business API Integration
Handles WhatsApp messaging for the retail AI sales assistant
"""

import os
import json
import logging
import requests
from typing import Dict, List, Any
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

logger = logging.getLogger(__name__)

class WhatsAppIntegration:
    def __init__(self):
        """Initialize WhatsApp integration with Twilio"""
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'your_twilio_account_sid')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'your_twilio_auth_token')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')  # Twilio Sandbox
        
        if self.account_sid != 'your_twilio_account_sid':
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            logger.warning("WhatsApp integration not configured. Please set Twilio credentials.")

    def send_message(self, to_number: str, message: str, media_url: str = None) -> Dict:
        """
        Send a WhatsApp message
        
        Args:
            to_number: Recipient's WhatsApp number (format: whatsapp:+1234567890)
            message: Message text
            media_url: Optional media URL for images/documents
            
        Returns:
            Dict with send status and message ID
        """
        try:
            if not self.client:
                return {
                    'success': False,
                    'error': 'WhatsApp integration not configured',
                    'message_id': None
                }

            message_data = {
                'from_': self.whatsapp_number,
                'to': to_number,
                'body': message
            }
            
            if media_url:
                message_data['media_url'] = media_url

            message_obj = self.client.messages.create(**message_data)
            
            return {
                'success': True,
                'message_id': message_obj.sid,
                'status': message_obj.status
            }
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message_id': None
            }

    def send_interactive_message(self, to_number: str, message: str, buttons: List[Dict]) -> Dict:
        """
        Send WhatsApp message with interactive buttons
        
        Args:
            to_number: Recipient's WhatsApp number
            message: Message text
            buttons: List of button objects with 'id' and 'title'
            
        Returns:
            Dict with send status
        """
        try:
            if not self.client:
                return {'success': False, 'error': 'WhatsApp integration not configured'}

            # For Twilio, we'll send the message with numbered options
            button_text = "\n\n" + "\n".join([f"{i+1}. {btn['title']}" for i, btn in enumerate(buttons)])
            full_message = message + button_text + "\n\nReply with the number of your choice."
            
            return self.send_message(to_number, full_message)
            
        except Exception as e:
            logger.error(f"Error sending interactive WhatsApp message: {str(e)}")
            return {'success': False, 'error': str(e)}

    def send_product_list(self, to_number: str, products: List[Dict]) -> Dict:
        """
        Send a formatted product list via WhatsApp
        
        Args:
            to_number: Recipient's WhatsApp number
            products: List of product dictionaries
            
        Returns:
            Dict with send status
        """
        try:
            if not products:
                return self.send_message(to_number, "No products found matching your criteria.")

            message = "🛍️ *Here are some products for you:*\n\n"
            
            for i, product in enumerate(products[:5], 1):  # Limit to 5 products
                message += f"*{i}. {product.get('name', 'Product')}*\n"
                message += f"💰 ${product.get('price', '0.00')}\n"
                
                if product.get('rating'):
                    stars = '⭐' * int(product.get('rating', 0))
                    message += f"{stars} ({product.get('rating')})\n"
                
                if product.get('features'):
                    features = ', '.join(product['features'][:2])  # First 2 features
                    message += f"✨ {features}\n"
                
                message += "\n"
            
            message += "Reply with the product number for more details or type 'cart' to view your cart."
            
            return self.send_message(to_number, message)
            
        except Exception as e:
            logger.error(f"Error sending product list: {str(e)}")
            return {'success': False, 'error': str(e)}

    def send_cart_summary(self, to_number: str, cart_items: List[Dict]) -> Dict:
        """
        Send cart summary via WhatsApp
        
        Args:
            to_number: Recipient's WhatsApp number
            cart_items: List of cart items
            
        Returns:
            Dict with send status
        """
        try:
            if not cart_items:
                return self.send_message(to_number, "🛒 Your cart is empty. Browse our products to get started!")

            message = "🛒 *Your Shopping Cart:*\n\n"
            total = 0
            
            for item in cart_items:
                quantity = item.get('quantity', 1)
                price = item.get('price', 0)
                item_total = price * quantity
                total += item_total
                
                message += f"• {item.get('name', 'Item')}\n"
                message += f"  Qty: {quantity} × ${price:.2f} = ${item_total:.2f}\n\n"
            
            # Add tax and shipping
            tax = total * 0.08
            shipping = 0 if total > 75 else 9.99
            final_total = total + tax + shipping
            
            message += f"Subtotal: ${total:.2f}\n"
            message += f"Tax (8%): ${tax:.2f}\n"
            message += f"Shipping: ${shipping:.2f}\n"
            message += f"*Total: ${final_total:.2f}*\n\n"
            
            if total < 75:
                message += f"💡 Add ${75 - total:.2f} more for FREE shipping!\n\n"
            
            message += "Reply 'checkout' to proceed with payment or 'continue' to keep shopping."
            
            return self.send_message(to_number, message)
            
        except Exception as e:
            logger.error(f"Error sending cart summary: {str(e)}")
            return {'success': False, 'error': str(e)}

    def process_webhook(self, request_data: Dict) -> Dict:
        """
        Process incoming WhatsApp webhook
        
        Args:
            request_data: Webhook data from Twilio
            
        Returns:
            Dict with processed message data
        """
        try:
            from_number = request_data.get('From', '')
            message_body = request_data.get('Body', '').strip()
            message_sid = request_data.get('MessageSid', '')
            
            # Extract phone number without whatsapp: prefix
            phone_number = from_number.replace('whatsapp:', '')
            
            return {
                'platform': 'whatsapp',
                'user_id': phone_number,
                'message': message_body,
                'message_id': message_sid,
                'channel_data': {
                    'from_number': from_number,
                    'to_number': request_data.get('To', ''),
                    'account_sid': request_data.get('AccountSid', '')
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing WhatsApp webhook: {str(e)}")
            return {
                'platform': 'whatsapp',
                'user_id': 'unknown',
                'message': '',
                'error': str(e)
            }

    def format_response_for_platform(self, response_data: Dict) -> str:
        """
        Format AI response for WhatsApp
        
        Args:
            response_data: Response from the AI agent
            
        Returns:
            Formatted message string
        """
        try:
            message = response_data.get('message', '')
            
            # Format message for WhatsApp (add emojis, formatting)
            if response_data.get('intent') == 'greeting':
                message = f"👋 {message}"
            elif response_data.get('intent') == 'product_search':
                message = f"🔍 {message}"
            elif response_data.get('intent') == 'promotions':
                message = f"🎉 {message}"
            elif response_data.get('intent') == 'purchase':
                message = f"🛒 {message}"
            
            # Add suggestions as numbered options
            if response_data.get('suggestions'):
                message += "\n\n*Quick Options:*\n"
                for i, suggestion in enumerate(response_data['suggestions'][:4], 1):
                    message += f"{i}. {suggestion}\n"
                message += "\nReply with a number or type your message."
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting WhatsApp response: {str(e)}")
            return response_data.get('message', 'Sorry, I encountered an error.')

    def get_setup_instructions(self) -> Dict:
        """Get setup instructions for WhatsApp integration"""
        return {
            'platform': 'WhatsApp',
            'provider': 'Twilio',
            'steps': [
                '1. Create a Twilio account at https://www.twilio.com',
                '2. Get your Account SID and Auth Token from Twilio Console',
                '3. Set up WhatsApp Sandbox or get approved WhatsApp Business number',
                '4. Set environment variables:',
                '   - TWILIO_ACCOUNT_SID=your_account_sid',
                '   - TWILIO_AUTH_TOKEN=your_auth_token',
                '   - TWILIO_WHATSAPP_NUMBER=whatsapp:+your_number',
                '5. Configure webhook URL in Twilio: https://yourapp.com/webhook/whatsapp',
                '6. Test the integration by sending a message to your WhatsApp number'
            ],
            'test_number': 'whatsapp:+14155238886',  # Twilio Sandbox
            'test_message': 'join <sandbox_keyword>'
        }
