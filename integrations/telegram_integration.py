"""
Telegram Bot Integration
Handles Telegram messaging for the retail AI sales assistant
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)

class TelegramIntegration:
    def __init__(self):
        """Initialize Telegram bot integration"""
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', 'your_telegram_bot_token')
        self.webhook_url = os.getenv('TELEGRAM_WEBHOOK_URL', 'https://yourapp.com/webhook/telegram')
        
        if self.bot_token != 'your_telegram_bot_token':
            self.application = Application.builder().token(self.bot_token).build()
            self._setup_handlers()
        else:
            self.application = None
            logger.warning("Telegram integration not configured. Please set TELEGRAM_BOT_TOKEN.")

    def _setup_handlers(self):
        """Set up Telegram bot handlers"""
        if not self.application:
            return
            
        # Command handlers
        self.application.add_handler(CommandHandler("start", self._start_command))
        self.application.add_handler(CommandHandler("help", self._help_command))
        self.application.add_handler(CommandHandler("cart", self._cart_command))
        self.application.add_handler(CommandHandler("products", self._products_command))
        
        # Message handler for text messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self._handle_callback))

    async def send_message(self, chat_id: str, message: str, reply_markup=None) -> Dict:
        """
        Send a Telegram message
        
        Args:
            chat_id: Telegram chat ID
            message: Message text
            reply_markup: Optional keyboard markup
            
        Returns:
            Dict with send status and message ID
        """
        try:
            if not self.application:
                return {
                    'success': False,
                    'error': 'Telegram integration not configured',
                    'message_id': None
                }

            bot = self.application.bot
            sent_message = await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
            return {
                'success': True,
                'message_id': sent_message.message_id,
                'chat_id': sent_message.chat_id
            }
            
        except Exception as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message_id': None
            }

    async def send_interactive_message(self, chat_id: str, message: str, buttons: List[Dict]) -> Dict:
        """
        Send Telegram message with inline keyboard buttons
        
        Args:
            chat_id: Telegram chat ID
            message: Message text
            buttons: List of button objects with 'text' and 'callback_data'
            
        Returns:
            Dict with send status
        """
        try:
            if not buttons:
                return await self.send_message(chat_id, message)

            # Create inline keyboard
            keyboard = []
            for i in range(0, len(buttons), 2):  # 2 buttons per row
                row = []
                for j in range(2):
                    if i + j < len(buttons):
                        btn = buttons[i + j]
                        row.append(InlineKeyboardButton(
                            text=btn.get('text', btn.get('title', 'Option')),
                            callback_data=btn.get('callback_data', btn.get('id', f'btn_{i+j}'))
                        ))
                keyboard.append(row)
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            return await self.send_message(chat_id, message, reply_markup)
            
        except Exception as e:
            logger.error(f"Error sending interactive Telegram message: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def send_product_list(self, chat_id: str, products: List[Dict]) -> Dict:
        """
        Send a formatted product list via Telegram
        
        Args:
            chat_id: Telegram chat ID
            products: List of product dictionaries
            
        Returns:
            Dict with send status
        """
        try:
            if not products:
                return await self.send_message(chat_id, "🔍 No products found matching your criteria.")

            message = "🛍️ *Here are some products for you:*\n\n"
            buttons = []
            
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
                
                # Add buttons for each product
                buttons.extend([
                    {'text': f'📋 Details {i}', 'callback_data': f'product_details_{product.get("id", i)}'},
                    {'text': f'🛒 Add {i}', 'callback_data': f'add_to_cart_{product.get("id", i)}'}
                ])
            
            # Add general action buttons
            buttons.extend([
                {'text': '🛒 View Cart', 'callback_data': 'view_cart'},
                {'text': '🔍 More Products', 'callback_data': 'more_products'}
            ])
            
            return await self.send_interactive_message(chat_id, message, buttons)
            
        except Exception as e:
            logger.error(f"Error sending product list: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def send_cart_summary(self, chat_id: str, cart_items: List[Dict]) -> Dict:
        """
        Send cart summary via Telegram
        
        Args:
            chat_id: Telegram chat ID
            cart_items: List of cart items
            
        Returns:
            Dict with send status
        """
        try:
            if not cart_items:
                buttons = [
                    {'text': '🛍️ Browse Products', 'callback_data': 'browse_products'},
                    {'text': '🎯 Recommendations', 'callback_data': 'get_recommendations'}
                ]
                return await self.send_interactive_message(
                    chat_id, 
                    "🛒 Your cart is empty. Let's find some great products for you!", 
                    buttons
                )

            message = "🛒 *Your Shopping Cart:*\n\n"
            total = 0
            
            for item in cart_items:
                quantity = item.get('quantity', 1)
                price = item.get('price', 0)
                item_total = price * quantity
                total += item_total
                
                message += f"• *{item.get('name', 'Item')}*\n"
                message += f"  Qty: {quantity} × ${price:.2f} = *${item_total:.2f}*\n\n"
            
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
            
            buttons = [
                {'text': '💳 Checkout', 'callback_data': 'checkout'},
                {'text': '🛍️ Continue Shopping', 'callback_data': 'continue_shopping'},
                {'text': '🗑️ Clear Cart', 'callback_data': 'clear_cart'},
                {'text': '🏷️ Apply Promo', 'callback_data': 'apply_promo'}
            ]
            
            return await self.send_interactive_message(chat_id, message, buttons)
            
        except Exception as e:
            logger.error(f"Error sending cart summary: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def _start_command(self, update: Update, context) -> None:
        """Handle /start command"""
        welcome_message = """
👋 *Welcome to Retail AI Assistant!*

I'm your personal shopping companion, ready to help you:
🔍 Find products
💰 Get best deals
🛒 Manage your cart
📦 Track orders
🎯 Get personalized recommendations

Type anything to start shopping or use these commands:
/products - Browse products
/cart - View your cart
/help - Get help
        """
        
        buttons = [
            {'text': '🛍️ Start Shopping', 'callback_data': 'start_shopping'},
            {'text': '🎯 Get Recommendations', 'callback_data': 'get_recommendations'},
            {'text': '🏷️ View Deals', 'callback_data': 'view_deals'},
            {'text': '❓ Help', 'callback_data': 'help'}
        ]
        
        await self.send_interactive_message(update.effective_chat.id, welcome_message, buttons)

    async def _help_command(self, update: Update, context) -> None:
        """Handle /help command"""
        help_message = """
🤖 *Retail AI Assistant Help*

*Commands:*
/start - Start shopping
/products - Browse products
/cart - View your cart
/help - Show this help

*What I can do:*
• 🔍 Search for products by name, category, or description
• 💰 Find best deals and apply promotions
• 🛒 Add items to cart and manage quantities
• 📦 Help with checkout and order tracking
• 🎯 Provide personalized recommendations
• 📱 Work across web, mobile, and messaging apps

*Examples:*
"Show me wireless headphones under $200"
"What deals do you have today?"
"Add this to my cart"
"Help me find a gift for my friend"

Just type naturally - I understand conversational language!
        """
        
        await self.send_message(update.effective_chat.id, help_message)

    async def _cart_command(self, update: Update, context) -> None:
        """Handle /cart command"""
        # This would integrate with the main cart system
        await self.send_cart_summary(update.effective_chat.id, [])

    async def _products_command(self, update: Update, context) -> None:
        """Handle /products command"""
        # This would integrate with the product system
        sample_products = [
            {'id': '1', 'name': 'Wireless Headphones', 'price': 199.99, 'rating': 4.5},
            {'id': '2', 'name': 'Smart Watch', 'price': 299.99, 'rating': 4.3}
        ]
        await self.send_product_list(update.effective_chat.id, sample_products)

    async def _handle_message(self, update: Update, context) -> None:
        """Handle regular text messages"""
        # This would integrate with the main AI agent
        user_message = update.message.text
        chat_id = update.effective_chat.id
        
        # For now, send a placeholder response
        response = f"I received your message: '{user_message}'. This will be processed by the AI agent."
        await self.send_message(chat_id, response)

    async def _handle_callback(self, update: Update, context) -> None:
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        chat_id = query.message.chat_id
        
        # Handle different callback actions
        if callback_data == 'start_shopping':
            await self.send_message(chat_id, "🛍️ Great! What are you looking for today?")
        elif callback_data == 'get_recommendations':
            await self.send_message(chat_id, "🎯 Let me get some personalized recommendations for you...")
        elif callback_data == 'view_deals':
            await self.send_message(chat_id, "🏷️ Here are today's best deals...")
        elif callback_data == 'view_cart':
            await self.send_cart_summary(chat_id, [])
        else:
            await self.send_message(chat_id, f"Processing: {callback_data}")

    def process_webhook(self, request_data: Dict) -> Dict:
        """
        Process incoming Telegram webhook
        
        Args:
            request_data: Webhook data from Telegram
            
        Returns:
            Dict with processed message data
        """
        try:
            message = request_data.get('message', {})
            callback_query = request_data.get('callback_query', {})
            
            if message:
                # Regular message
                chat_id = str(message.get('chat', {}).get('id', ''))
                user_id = str(message.get('from', {}).get('id', ''))
                message_text = message.get('text', '')
                message_id = message.get('message_id', '')
                
                return {
                    'platform': 'telegram',
                    'user_id': user_id,
                    'chat_id': chat_id,
                    'message': message_text,
                    'message_id': message_id,
                    'message_type': 'text',
                    'channel_data': {
                        'first_name': message.get('from', {}).get('first_name', ''),
                        'username': message.get('from', {}).get('username', ''),
                        'chat_type': message.get('chat', {}).get('type', 'private')
                    }
                }
            
            elif callback_query:
                # Inline button callback
                chat_id = str(callback_query.get('message', {}).get('chat', {}).get('id', ''))
                user_id = str(callback_query.get('from', {}).get('id', ''))
                callback_data = callback_query.get('data', '')
                
                return {
                    'platform': 'telegram',
                    'user_id': user_id,
                    'chat_id': chat_id,
                    'message': callback_data,
                    'message_id': callback_query.get('id', ''),
                    'message_type': 'callback',
                    'channel_data': {
                        'first_name': callback_query.get('from', {}).get('first_name', ''),
                        'username': callback_query.get('from', {}).get('username', '')
                    }
                }
            
            return {
                'platform': 'telegram',
                'user_id': 'unknown',
                'message': '',
                'error': 'No message or callback_query found'
            }
            
        except Exception as e:
            logger.error(f"Error processing Telegram webhook: {str(e)}")
            return {
                'platform': 'telegram',
                'user_id': 'unknown',
                'message': '',
                'error': str(e)
            }

    def format_response_for_platform(self, response_data: Dict) -> str:
        """
        Format AI response for Telegram
        
        Args:
            response_data: Response from the AI agent
            
        Returns:
            Formatted message string
        """
        try:
            message = response_data.get('message', '')
            
            # Format message for Telegram (Markdown formatting)
            if response_data.get('intent') == 'greeting':
                message = f"👋 {message}"
            elif response_data.get('intent') == 'product_search':
                message = f"🔍 {message}"
            elif response_data.get('intent') == 'promotions':
                message = f"🎉 {message}"
            elif response_data.get('intent') == 'purchase':
                message = f"🛒 {message}"
            
            # Convert to Markdown formatting
            message = message.replace('**', '*')  # Bold formatting
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting Telegram response: {str(e)}")
            return response_data.get('message', 'Sorry, I encountered an error.')

    async def set_webhook(self, webhook_url: str) -> Dict:
        """Set webhook URL for Telegram bot"""
        try:
            if not self.application:
                return {'success': False, 'error': 'Telegram integration not configured'}
                
            bot = self.application.bot
            result = await bot.set_webhook(url=webhook_url)
            
            return {
                'success': result,
                'webhook_url': webhook_url
            }
            
        except Exception as e:
            logger.error(f"Error setting Telegram webhook: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_setup_instructions(self) -> Dict:
        """Get setup instructions for Telegram integration"""
        return {
            'platform': 'Telegram',
            'provider': 'Telegram Bot API',
            'steps': [
                '1. Create a new bot by messaging @BotFather on Telegram',
                '2. Send /newbot command and follow instructions',
                '3. Get your bot token from BotFather',
                '4. Set environment variable: TELEGRAM_BOT_TOKEN=your_bot_token',
                '5. Set webhook URL: TELEGRAM_WEBHOOK_URL=https://yourapp.com/webhook/telegram',
                '6. Configure webhook by calling /webhook/telegram/set endpoint',
                '7. Test by messaging your bot on Telegram'
            ],
            'bot_commands': [
                '/start - Start the bot',
                '/help - Get help',
                '/products - Browse products',
                '/cart - View cart'
            ]
        }
