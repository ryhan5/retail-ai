"""
Messaging Coordinator
Coordinates messaging across WhatsApp and Telegram platforms
Now powered by Google Gemini AI
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from .whatsapp_integration import WhatsAppIntegration
from .telegram_integration import TelegramIntegration
from ai_service import get_ai_response, get_product_recommendations

logger = logging.getLogger(__name__)

class MessagingCoordinator:
    def __init__(self):
        """Initialize messaging coordinator with all platforms"""
        self.whatsapp = WhatsAppIntegration()
        self.telegram = TelegramIntegration()
        
        # Platform mapping
        self.platforms = {
            'whatsapp': self.whatsapp,
            'telegram': self.telegram
        }

    async def send_message(self, platform: str, recipient: str, message: str, **kwargs) -> Dict:
        """
        Send message through specified platform
        
        Args:
            platform: Platform name ('whatsapp' or 'telegram')
            recipient: Recipient identifier (phone number or chat ID)
            message: Message text
            **kwargs: Platform-specific parameters
            
        Returns:
            Dict with send status
        """
        try:
            if platform not in self.platforms:
                return {
                    'success': False,
                    'error': f'Unsupported platform: {platform}',
                    'platform': platform
                }

            platform_handler = self.platforms[platform]
            
            if platform == 'whatsapp':
                # WhatsApp uses synchronous methods
                return platform_handler.send_message(recipient, message, **kwargs)
            elif platform == 'telegram':
                # Telegram uses async methods
                return await platform_handler.send_message(recipient, message, **kwargs)
                
        except Exception as e:
            logger.error(f"Error sending message via {platform}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'platform': platform
            }

    async def send_interactive_message(self, platform: str, recipient: str, message: str, buttons: List[Dict]) -> Dict:
        """
        Send interactive message with buttons
        
        Args:
            platform: Platform name
            recipient: Recipient identifier
            message: Message text
            buttons: List of button objects
            
        Returns:
            Dict with send status
        """
        try:
            if platform not in self.platforms:
                return {'success': False, 'error': f'Unsupported platform: {platform}'}

            platform_handler = self.platforms[platform]
            
            if platform == 'whatsapp':
                return platform_handler.send_interactive_message(recipient, message, buttons)
            elif platform == 'telegram':
                return await platform_handler.send_interactive_message(recipient, message, buttons)
                
        except Exception as e:
            logger.error(f"Error sending interactive message via {platform}: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def send_product_list(self, platform: str, recipient: str, products: List[Dict]) -> Dict:
        """
        Send formatted product list
        
        Args:
            platform: Platform name
            recipient: Recipient identifier
            products: List of product dictionaries
            
        Returns:
            Dict with send status
        """
        try:
            if platform not in self.platforms:
                return {'success': False, 'error': f'Unsupported platform: {platform}'}

            platform_handler = self.platforms[platform]
            
            if platform == 'whatsapp':
                return platform_handler.send_product_list(recipient, products)
            elif platform == 'telegram':
                return await platform_handler.send_product_list(recipient, products)
                
        except Exception as e:
            logger.error(f"Error sending product list via {platform}: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def send_cart_summary(self, platform: str, recipient: str, cart_items: List[Dict]) -> Dict:
        """
        Send cart summary
        
        Args:
            platform: Platform name
            recipient: Recipient identifier
            cart_items: List of cart items
            
        Returns:
            Dict with send status
        """
        try:
            if platform not in self.platforms:
                return {'success': False, 'error': f'Unsupported platform: {platform}'}

            platform_handler = self.platforms[platform]
            
            if platform == 'whatsapp':
                return platform_handler.send_cart_summary(recipient, cart_items)
            elif platform == 'telegram':
                return await platform_handler.send_cart_summary(recipient, cart_items)
                
        except Exception as e:
            logger.error(f"Error sending cart summary via {platform}: {str(e)}")
            return {'success': False, 'error': str(e)}

    def process_webhook(self, platform: str, request_data: Dict) -> Dict:
        """
        Process incoming webhook from any platform
        
        Args:
            platform: Platform name
            request_data: Webhook data
            
        Returns:
            Dict with processed message data
        """
        try:
            if platform not in self.platforms:
                return {
                    'platform': platform,
                    'user_id': 'unknown',
                    'message': '',
                    'error': f'Unsupported platform: {platform}'
                }

            platform_handler = self.platforms[platform]
            return platform_handler.process_webhook(request_data)
            
        except Exception as e:
            logger.error(f"Error processing {platform} webhook: {str(e)}")
            return {
                'platform': platform,
                'user_id': 'unknown',
                'message': '',
                'error': str(e)
            }

    def format_response_for_platform(self, platform: str, response_data: Dict) -> str:
        """
        Format AI response for specific platform
        
        Args:
            platform: Platform name
            response_data: Response from AI agent
            
        Returns:
            Formatted message string
        """
        try:
            if platform not in self.platforms:
                return response_data.get('message', 'Error: Unsupported platform')

            platform_handler = self.platforms[platform]
            return platform_handler.format_response_for_platform(response_data)
            
        except Exception as e:
            logger.error(f"Error formatting response for {platform}: {str(e)}")
            return response_data.get('message', 'Sorry, I encountered an error.')

    def get_platform_status(self) -> Dict:
        """Get status of all messaging platforms"""
        status = {}
        
        for platform_name, platform_handler in self.platforms.items():
            if platform_name == 'whatsapp':
                status[platform_name] = {
                    'configured': platform_handler.client is not None,
                    'provider': 'Twilio',
                    'features': ['text_messages', 'media', 'interactive_buttons']
                }
            elif platform_name == 'telegram':
                status[platform_name] = {
                    'configured': platform_handler.application is not None,
                    'provider': 'Telegram Bot API',
                    'features': ['text_messages', 'media', 'inline_keyboards', 'commands']
                }
        
        return status

    def get_setup_instructions(self) -> Dict:
        """Get setup instructions for all platforms"""
        instructions = {}
        
        for platform_name, platform_handler in self.platforms.items():
            instructions[platform_name] = platform_handler.get_setup_instructions()
        
        return instructions

    async def broadcast_message(self, recipients: List[Dict], message: str) -> Dict:
        """
        Broadcast message to multiple recipients across platforms
        
        Args:
            recipients: List of recipient dicts with 'platform', 'recipient_id'
            message: Message to broadcast
            
        Returns:
            Dict with broadcast results
        """
        results = {
            'total_sent': 0,
            'total_failed': 0,
            'results': []
        }
        
        for recipient in recipients:
            platform = recipient.get('platform')
            recipient_id = recipient.get('recipient_id')
            
            if not platform or not recipient_id:
                results['results'].append({
                    'platform': platform,
                    'recipient_id': recipient_id,
                    'success': False,
                    'error': 'Missing platform or recipient_id'
                })
                results['total_failed'] += 1
                continue
            
            try:
                result = await self.send_message(platform, recipient_id, message)
                results['results'].append({
                    'platform': platform,
                    'recipient_id': recipient_id,
                    **result
                })
                
                if result.get('success'):
                    results['total_sent'] += 1
                else:
                    results['total_failed'] += 1
                    
            except Exception as e:
                results['results'].append({
                    'platform': platform,
                    'recipient_id': recipient_id,
                    'success': False,
                    'error': str(e)
                })
                results['total_failed'] += 1
        
        return results

    def create_platform_user_id(self, platform: str, platform_user_id: str) -> str:
        """
        Create unified user ID across platforms
        
        Args:
            platform: Platform name
            platform_user_id: Platform-specific user ID
            
        Returns:
            Unified user ID
        """
        return f"{platform}:{platform_user_id}"

    def parse_platform_user_id(self, unified_user_id: str) -> Dict:
        """
        Parse unified user ID to get platform and platform-specific ID
        
        Args:
            unified_user_id: Unified user ID
            
        Returns:
            Dict with platform and platform_user_id
        """
        try:
            if ':' in unified_user_id:
                platform, platform_user_id = unified_user_id.split(':', 1)
                return {
                    'platform': platform,
                    'platform_user_id': platform_user_id
                }
            else:
                return {
                    'platform': 'unknown',
                    'platform_user_id': unified_user_id
                }
        except Exception as e:
            logger.error(f"Error parsing user ID {unified_user_id}: {str(e)}")
            return {
                'platform': 'unknown',
                'platform_user_id': unified_user_id
            }
