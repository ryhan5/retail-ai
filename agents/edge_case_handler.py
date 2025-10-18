"""
Edge Case Handler
Handles exceptional scenarios gracefully:
- Payment failures
- Out-of-stock items
- Order modifications
- Delivery issues
- Returns and refunds
"""

import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class EdgeCaseHandler:
    """
    Handles edge cases and exceptional scenarios with grace and customer-first approach
    """
    
    def __init__(self):
        self.payment_retry_limit = 3
        self.alternative_payment_methods = ['credit_card', 'debit_card', 'paypal', 'apple_pay', 'google_pay']
    
    def handle_payment_failure(self, payment_data: Dict, failure_reason: str, 
                               retry_count: int = 0) -> Dict:
        """
        Handle payment failure scenarios with helpful recovery options
        """
        customer_name = payment_data.get('customer_name', 'there')
        amount = payment_data.get('amount', 0)
        payment_method = payment_data.get('payment_method', 'card')
        
        # Categorize failure reason
        failure_category = self._categorize_payment_failure(failure_reason)
        
        if retry_count >= self.payment_retry_limit:
            # Max retries reached
            return {
                'success': False,
                'message': f"I'm sorry {customer_name}, we've tried processing your payment {retry_count} times without success. "
                          f"Let's try a different approach to complete your ${amount:.2f} purchase.",
                'recovery_options': [
                    {
                        'action': 'try_different_payment',
                        'label': 'Try a different payment method',
                        'description': 'Use another card or payment option'
                    },
                    {
                        'action': 'save_cart',
                        'label': 'Save cart for later',
                        'description': 'We\'ll hold your items for 24 hours'
                    },
                    {
                        'action': 'contact_support',
                        'label': 'Speak to support',
                        'description': 'Get help from our payment specialists'
                    },
                    {
                        'action': 'split_payment',
                        'label': 'Split payment',
                        'description': 'Pay with multiple methods'
                    }
                ],
                'failure_category': failure_category,
                'suggestions': [
                    'Try another payment method',
                    'Save cart and try later',
                    'Contact support for help',
                    'Use a different card'
                ]
            }
        
        # First or second retry - provide specific guidance
        recovery_message = self._get_payment_recovery_message(failure_category, customer_name)
        
        return {
            'success': False,
            'message': recovery_message,
            'recovery_options': [
                {
                    'action': 'retry_payment',
                    'label': 'Try again',
                    'description': f'Retry with {payment_method}'
                },
                {
                    'action': 'update_payment_info',
                    'label': 'Update payment details',
                    'description': 'Check card number, CVV, or expiry date'
                },
                {
                    'action': 'try_different_payment',
                    'label': 'Use different payment method',
                    'description': 'Try PayPal, Apple Pay, or another card'
                },
                {
                    'action': 'contact_bank',
                    'label': 'Contact your bank',
                    'description': 'Your bank may need to approve this transaction'
                }
            ],
            'failure_category': failure_category,
            'retry_count': retry_count + 1,
            'suggestions': self._get_payment_failure_suggestions(failure_category)
        }
    
    def handle_out_of_stock(self, product: Dict, customer_context: Dict) -> Dict:
        """
        Handle out-of-stock scenarios with alternatives and notifications
        """
        product_name = product.get('name', 'this item')
        customer_name = customer_context.get('name', 'there')
        
        # Check alternative options
        alternatives = self._find_alternatives(product, customer_context)
        other_locations = self._check_other_store_locations(product)
        restock_date = self._get_estimated_restock_date(product)
        
        message = f"I'm sorry {customer_name}, {product_name} is currently out of stock. "
        
        # Provide recovery options based on what's available
        recovery_options = []
        
        if other_locations:
            message += f"However, it's available at {len(other_locations)} other location(s). "
            recovery_options.append({
                'action': 'reserve_other_location',
                'label': f'Reserve at {other_locations[0]["name"]}',
                'description': f'{other_locations[0]["distance"]} away',
                'data': other_locations[0]
            })
        
        if restock_date:
            message += f"We expect to restock by {restock_date}. "
            recovery_options.append({
                'action': 'notify_restock',
                'label': 'Notify me when back in stock',
                'description': f'Get an alert around {restock_date}',
                'data': {'product_id': product['id'], 'restock_date': restock_date}
            })
        
        if alternatives:
            message += f"I found {len(alternatives)} similar product(s) that might interest you. "
            recovery_options.append({
                'action': 'show_alternatives',
                'label': 'Show similar products',
                'description': f'{len(alternatives)} alternatives available',
                'data': alternatives
            })
        
        # Always offer to continue shopping
        recovery_options.append({
            'action': 'continue_shopping',
            'label': 'Continue shopping',
            'description': 'Browse other products'
        })
        
        return {
            'success': False,
            'out_of_stock': True,
            'message': message,
            'product': product,
            'alternatives': alternatives[:3],
            'other_locations': other_locations,
            'restock_date': restock_date,
            'recovery_options': recovery_options,
            'suggestions': [
                'Show me similar products',
                'Notify me when back in stock',
                'Check other store locations',
                'Continue shopping'
            ]
        }
    
    def handle_order_modification(self, order_id: str, modification_type: str, 
                                  modification_data: Dict, customer_context: Dict) -> Dict:
        """
        Handle order modification requests (change items, address, delivery time, etc.)
        """
        customer_name = customer_context.get('name', 'there')
        
        # Check if modification is possible
        order_status = self._get_order_status(order_id)
        modification_window = self._check_modification_window(order_id, modification_type)
        
        if not modification_window['allowed']:
            # Modification not allowed
            return {
                'success': False,
                'message': f"I'm sorry {customer_name}, {modification_window['reason']} "
                          f"However, I can help you with some alternatives.",
                'recovery_options': [
                    {
                        'action': 'cancel_and_reorder',
                        'label': 'Cancel and place new order',
                        'description': 'Full refund, then create new order'
                    },
                    {
                        'action': 'contact_support',
                        'label': 'Speak to support',
                        'description': 'Our team may be able to help'
                    },
                    {
                        'action': 'track_order',
                        'label': 'Track current order',
                        'description': 'See order status and delivery time'
                    }
                ],
                'suggestions': [
                    'Cancel and reorder',
                    'Contact support',
                    'Track my order',
                    'Accept current order'
                ]
            }
        
        # Process modification
        modification_result = self._process_order_modification(
            order_id, modification_type, modification_data
        )
        
        if modification_result['success']:
            message = f"Great news {customer_name}! I've successfully updated your order #{order_id}. "
            
            if modification_type == 'add_items':
                message += f"Added {len(modification_data['items'])} item(s) to your order. "
                if modification_result.get('price_difference'):
                    message += f"Additional charge: ${modification_result['price_difference']:.2f}"
            
            elif modification_type == 'remove_items':
                message += f"Removed {len(modification_data['items'])} item(s) from your order. "
                if modification_result.get('refund_amount'):
                    message += f"Refund: ${modification_result['refund_amount']:.2f}"
            
            elif modification_type == 'change_address':
                message += f"Updated delivery address to {modification_data['new_address']}. "
            
            elif modification_type == 'change_delivery_time':
                message += f"Updated delivery time to {modification_data['new_time']}. "
            
            return {
                'success': True,
                'message': message,
                'order_id': order_id,
                'modification_type': modification_type,
                'updated_order': modification_result['updated_order'],
                'suggestions': [
                    'View updated order',
                    'Track delivery',
                    'Make another change',
                    'Continue shopping'
                ]
            }
        else:
            # Modification failed
            return {
                'success': False,
                'message': f"I encountered an issue updating your order: {modification_result['error']}. "
                          f"Let me help you resolve this.",
                'recovery_options': [
                    {
                        'action': 'retry_modification',
                        'label': 'Try again',
                        'description': 'Retry the modification'
                    },
                    {
                        'action': 'contact_support',
                        'label': 'Contact support',
                        'description': 'Get help from our team'
                    },
                    {
                        'action': 'keep_original',
                        'label': 'Keep original order',
                        'description': 'Proceed with current order'
                    }
                ],
                'suggestions': [
                    'Try again',
                    'Contact support',
                    'Keep original order'
                ]
            }
    
    def handle_delivery_issue(self, order_id: str, issue_type: str, 
                             customer_context: Dict) -> Dict:
        """
        Handle delivery issues (delayed, damaged, wrong item, etc.)
        """
        customer_name = customer_context.get('name', 'there')
        
        issue_responses = {
            'delayed': {
                'message': f"I'm sorry your order is delayed, {customer_name}. Let me check the latest status and provide options.",
                'actions': ['track_order', 'expedite_delivery', 'cancel_refund', 'contact_carrier']
            },
            'damaged': {
                'message': f"I'm very sorry your item arrived damaged, {customer_name}. We'll make this right immediately.",
                'actions': ['replacement', 'full_refund', 'partial_refund', 'store_credit']
            },
            'wrong_item': {
                'message': f"I apologize for sending the wrong item, {customer_name}. Let's fix this right away.",
                'actions': ['send_correct_item', 'full_refund', 'keep_and_discount', 'return_and_reorder']
            },
            'not_received': {
                'message': f"I'm sorry you haven't received your order, {customer_name}. Let me investigate this immediately.",
                'actions': ['track_order', 'file_claim', 'resend_order', 'full_refund']
            }
        }
        
        response = issue_responses.get(issue_type, issue_responses['delayed'])
        
        return {
            'success': True,
            'message': response['message'],
            'issue_type': issue_type,
            'order_id': order_id,
            'recovery_options': self._get_delivery_issue_options(issue_type, order_id),
            'suggestions': [
                'Get immediate replacement',
                'Process full refund',
                'Track order status',
                'Speak to support'
            ]
        }
    
    # Private helper methods
    def _categorize_payment_failure(self, failure_reason: str) -> str:
        """Categorize payment failure for appropriate response"""
        reason_lower = failure_reason.lower()
        
        if any(word in reason_lower for word in ['insufficient', 'funds', 'balance']):
            return 'insufficient_funds'
        elif any(word in reason_lower for word in ['declined', 'denied', 'rejected']):
            return 'card_declined'
        elif any(word in reason_lower for word in ['expired', 'expiry']):
            return 'card_expired'
        elif any(word in reason_lower for word in ['cvv', 'security', 'code']):
            return 'security_code_error'
        elif any(word in reason_lower for word in ['network', 'connection', 'timeout']):
            return 'network_error'
        else:
            return 'unknown_error'
    
    def _get_payment_recovery_message(self, failure_category: str, customer_name: str) -> str:
        """Get appropriate recovery message based on failure category"""
        messages = {
            'insufficient_funds': f"It looks like there might not be enough funds available, {customer_name}. Would you like to try a different payment method or split the payment?",
            'card_declined': f"Your card was declined, {customer_name}. This sometimes happens for security reasons. Try contacting your bank or using a different payment method.",
            'card_expired': f"It appears your card has expired, {customer_name}. Please update your card details or use a different payment method.",
            'security_code_error': f"The security code (CVV) doesn't match, {customer_name}. Please double-check the 3-digit code on the back of your card.",
            'network_error': f"We're experiencing a temporary connection issue, {customer_name}. Let's try again in a moment.",
            'unknown_error': f"We encountered an unexpected issue processing your payment, {customer_name}. Let's try a different approach."
        }
        
        return messages.get(failure_category, messages['unknown_error'])
    
    def _get_payment_failure_suggestions(self, failure_category: str) -> List[str]:
        """Get contextual suggestions based on failure type"""
        suggestions = {
            'insufficient_funds': ['Try different card', 'Split payment', 'Remove some items', 'Save cart for later'],
            'card_declined': ['Contact your bank', 'Try different card', 'Use PayPal', 'Speak to support'],
            'card_expired': ['Update card details', 'Use different card', 'Try PayPal', 'Save cart'],
            'security_code_error': ['Re-enter CVV', 'Check card details', 'Try different card', 'Get help'],
            'network_error': ['Try again', 'Wait a moment', 'Check connection', 'Save cart'],
            'unknown_error': ['Try again', 'Different payment method', 'Contact support', 'Save cart']
        }
        
        return suggestions.get(failure_category, suggestions['unknown_error'])
    
    def _find_alternatives(self, product: Dict, customer_context: Dict) -> List[Dict]:
        """Find alternative products"""
        # Mock implementation - in production, use recommendation engine
        return [
            {
                'id': 'ALT001',
                'name': f"Similar to {product.get('name', 'product')}",
                'price': product.get('price', 0) * 0.95,
                'in_stock': True,
                'reason': 'Similar features and price'
            }
        ]
    
    def _check_other_store_locations(self, product: Dict) -> List[Dict]:
        """Check product availability at other stores"""
        # Mock implementation
        return [
            {'name': 'Downtown Store', 'distance': '2.5 miles', 'stock': 5},
            {'name': 'Mall Location', 'distance': '5.1 miles', 'stock': 3}
        ]
    
    def _get_estimated_restock_date(self, product: Dict) -> str:
        """Get estimated restock date"""
        # Mock implementation
        restock = datetime.now() + timedelta(days=7)
        return restock.strftime('%B %d, %Y')
    
    def _get_order_status(self, order_id: str) -> str:
        """Get current order status"""
        # Mock implementation
        return 'processing'
    
    def _check_modification_window(self, order_id: str, modification_type: str) -> Dict:
        """Check if modification is allowed"""
        # Mock implementation - in production, check actual order status
        order_status = self._get_order_status(order_id)
        
        if order_status in ['shipped', 'delivered']:
            return {
                'allowed': False,
                'reason': 'your order has already been shipped.'
            }
        
        return {
            'allowed': True,
            'reason': ''
        }
    
    def _process_order_modification(self, order_id: str, modification_type: str, 
                                   modification_data: Dict) -> Dict:
        """Process the actual modification"""
        # Mock implementation
        return {
            'success': True,
            'updated_order': {
                'order_id': order_id,
                'status': 'modified',
                'modification_type': modification_type
            },
            'price_difference': 10.00 if modification_type == 'add_items' else None,
            'refund_amount': 15.00 if modification_type == 'remove_items' else None
        }
    
    def _get_delivery_issue_options(self, issue_type: str, order_id: str) -> List[Dict]:
        """Get recovery options for delivery issues"""
        options = {
            'delayed': [
                {'action': 'track_order', 'label': 'Track order', 'description': 'See real-time location'},
                {'action': 'expedite', 'label': 'Expedite delivery', 'description': 'Upgrade to faster shipping'},
                {'action': 'cancel_refund', 'label': 'Cancel & refund', 'description': 'Full refund processed'},
            ],
            'damaged': [
                {'action': 'replacement', 'label': 'Send replacement', 'description': 'Free expedited shipping'},
                {'action': 'full_refund', 'label': 'Full refund', 'description': 'Keep damaged item'},
                {'action': 'store_credit', 'label': 'Store credit + 20%', 'description': 'Extra 20% credit'},
            ],
            'wrong_item': [
                {'action': 'send_correct', 'label': 'Send correct item', 'description': 'Free return label included'},
                {'action': 'full_refund', 'label': 'Full refund', 'description': 'Keep wrong item'},
                {'action': 'discount', 'label': 'Keep with 50% off', 'description': 'Partial refund'},
            ],
            'not_received': [
                {'action': 'file_claim', 'label': 'File claim', 'description': 'Investigate with carrier'},
                {'action': 'resend', 'label': 'Resend order', 'description': 'Free expedited shipping'},
                {'action': 'full_refund', 'label': 'Full refund', 'description': 'Immediate refund'},
            ]
        }
        
        return options.get(issue_type, options['delayed'])
