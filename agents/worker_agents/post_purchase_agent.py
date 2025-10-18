"""
Post-Purchase Support Agent - Handles returns, exchanges, shipment tracking, and feedback
Manages the entire post-purchase customer experience
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random
import uuid

logger = logging.getLogger(__name__)

class PostPurchaseAgent:
    def __init__(self):
        """Initialize Post-Purchase Support Agent"""
        self.return_reasons = [
            'Defective product',
            'Wrong item received',
            'Not as described',
            'Changed mind',
            'Better price found',
            'No longer needed',
            'Damaged in shipping',
            'Quality not satisfactory'
        ]
        
        self.return_policy = {
            'standard_period': 30,  # days
            'extended_period': 60,  # days for premium members
            'restocking_fee': 0.15,  # 15% for certain items
            'free_return_shipping': True,
            'instant_refund': False
        }
        
        self.feedback_categories = [
            'Product Quality',
            'Shipping Speed',
            'Packaging',
            'Customer Service',
            'Website Experience',
            'Value for Money'
        ]
        
        # Mock order history for tracking
        self.order_history = {}
    
    def initiate_return(self, order_id: str, items: List[Dict], reason: str, customer_info: Dict) -> Dict:
        """
        Initiate a return request
        
        Args:
            order_id: Order ID
            items: List of items to return
            reason: Return reason
            customer_info: Customer information
            
        Returns:
            Return initiation details
        """
        try:
            # Generate return authorization
            return_id = f"RET{uuid.uuid4().hex[:8].upper()}"
            rma_number = f"RMA{random.randint(100000, 999999)}"
            
            # Check return eligibility
            order_date = datetime.now() - timedelta(days=random.randint(1, 25))
            days_since_order = (datetime.now() - order_date).days
            
            is_premium = customer_info.get('tier', 'bronze') in ['gold', 'platinum']
            return_period = self.return_policy['extended_period'] if is_premium else self.return_policy['standard_period']
            
            if days_since_order > return_period:
                return {
                    'success': False,
                    'error': 'Return period expired',
                    'message': f'Returns must be initiated within {return_period} days of purchase'
                }
            
            # Calculate refund amount
            items_total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
            restocking_fee = 0
            
            # Apply restocking fee for certain reasons
            if reason in ['Changed mind', 'Better price found', 'No longer needed']:
                restocking_fee = items_total * self.return_policy['restocking_fee']
            
            refund_amount = items_total - restocking_fee
            
            # Generate return label
            return_label = {
                'carrier': random.choice(['UPS', 'FedEx', 'USPS']),
                'tracking': f"RTN{uuid.uuid4().hex[:12].upper()}",
                'label_url': f"https://returns.example.com/label/{return_id}",
                'drop_off_locations': [
                    'UPS Store - 123 Main St',
                    'FedEx Office - 456 Oak Ave',
                    'USPS - 789 Elm St'
                ]
            }
            
            result = {
                'success': True,
                'return_id': return_id,
                'rma_number': rma_number,
                'order_id': order_id,
                'items': items,
                'reason': reason,
                'status': 'initiated',
                'refund_amount': round(refund_amount, 2),
                'restocking_fee': round(restocking_fee, 2),
                'return_label': return_label,
                'instructions': [
                    f'Print the return label or show RMA {rma_number} at drop-off',
                    'Pack items securely in original packaging if available',
                    'Include all accessories and documentation',
                    f'Drop off at any {return_label["carrier"]} location',
                    'Refund will be processed within 5-7 business days of receipt'
                ],
                'estimated_refund_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
            }
            
            # Store return request
            self.order_history[order_id] = {
                'return_request': result,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Return initiated: {return_id} for order {order_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error initiating return: {str(e)}")
            return {
                'success': False,
                'error': 'Failed to initiate return',
                'message': str(e)
            }
    
    def process_exchange(self, order_id: str, original_item: Dict, new_item: Dict, reason: str) -> Dict:
        """
        Process an exchange request
        
        Args:
            order_id: Order ID
            original_item: Item to be exchanged
            new_item: New item requested
            reason: Exchange reason
            
        Returns:
            Exchange processing details
        """
        exchange_id = f"EXC{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate price difference
        price_diff = new_item.get('price', 0) - original_item.get('price', 0)
        
        # Determine exchange type
        if price_diff > 0:
            exchange_type = 'upgrade'
            action_required = f'Payment of ${price_diff:.2f} required'
        elif price_diff < 0:
            exchange_type = 'downgrade'
            action_required = f'Refund of ${abs(price_diff):.2f} will be issued'
        else:
            exchange_type = 'even'
            action_required = 'No additional payment required'
        
        # Generate shipping details
        shipping_details = {
            'return_label': f"https://returns.example.com/exchange/{exchange_id}",
            'new_item_tracking': f"EXC{uuid.uuid4().hex[:12].upper()}",
            'estimated_delivery': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        }
        
        return {
            'success': True,
            'exchange_id': exchange_id,
            'order_id': order_id,
            'original_item': original_item,
            'new_item': new_item,
            'exchange_type': exchange_type,
            'price_difference': round(price_diff, 2),
            'action_required': action_required,
            'reason': reason,
            'status': 'approved',
            'shipping_details': shipping_details,
            'next_steps': [
                'Return the original item using provided label',
                'New item will ship once original is received',
                action_required,
                'Track your exchange with ID: ' + exchange_id
            ]
        }
    
    def track_return_status(self, return_id: str) -> Dict:
        """
        Track return shipment and refund status
        
        Args:
            return_id: Return ID
            
        Returns:
            Return tracking information
        """
        # Mock return statuses
        statuses = [
            {'status': 'Return Initiated', 'timestamp': '2024-01-01 10:00', 'description': 'Return request created'},
            {'status': 'Label Generated', 'timestamp': '2024-01-01 10:30', 'description': 'Return label sent to customer'},
            {'status': 'Package Dropped Off', 'timestamp': '2024-01-02 14:00', 'description': 'Package received by carrier'},
            {'status': 'In Transit', 'timestamp': '2024-01-03 09:00', 'description': 'Package on the way to warehouse'},
            {'status': 'Received at Warehouse', 'timestamp': '2024-01-05 11:00', 'description': 'Return received and being processed'},
            {'status': 'Inspection Complete', 'timestamp': '2024-01-06 15:00', 'description': 'Items inspected and approved'},
            {'status': 'Refund Processed', 'timestamp': '2024-01-07 10:00', 'description': 'Refund issued to original payment method'}
        ]
        
        # Randomly select current status
        current_index = random.randint(2, len(statuses) - 1)
        current_status = statuses[current_index]
        
        return {
            'return_id': return_id,
            'current_status': current_status['status'],
            'last_update': current_status['timestamp'],
            'description': current_status['description'],
            'history': statuses[:current_index + 1],
            'refund_status': 'Completed' if current_index >= 6 else 'Pending',
            'estimated_completion': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'contact_support': current_index < 4  # Show support option if not yet received
        }
    
    def track_shipment(self, tracking_number: str) -> Dict:
        """
        Track order shipment
        
        Args:
            tracking_number: Shipment tracking number
            
        Returns:
            Shipment tracking details
        """
        # Mock tracking data
        tracking_events = [
            {'event': 'Order Placed', 'location': 'Online', 'timestamp': '2024-01-01 10:00'},
            {'event': 'Order Confirmed', 'location': 'Warehouse', 'timestamp': '2024-01-01 10:30'},
            {'event': 'Package Prepared', 'location': 'Fulfillment Center', 'timestamp': '2024-01-01 14:00'},
            {'event': 'Shipped', 'location': 'Distribution Center', 'timestamp': '2024-01-01 18:00'},
            {'event': 'In Transit', 'location': 'Regional Hub', 'timestamp': '2024-01-02 06:00'},
            {'event': 'Out for Delivery', 'location': 'Local Facility', 'timestamp': '2024-01-03 08:00'},
            {'event': 'Delivered', 'location': 'Customer Address', 'timestamp': '2024-01-03 14:30'}
        ]
        
        # Randomly select current status
        current_index = random.randint(3, len(tracking_events) - 1)
        
        return {
            'tracking_number': tracking_number,
            'carrier': random.choice(['UPS', 'FedEx', 'USPS', 'DHL']),
            'current_status': tracking_events[current_index]['event'],
            'current_location': tracking_events[current_index]['location'],
            'last_update': tracking_events[current_index]['timestamp'],
            'events': tracking_events[:current_index + 1],
            'estimated_delivery': '2024-01-03 14:00',
            'delivered': current_index == len(tracking_events) - 1,
            'delivery_proof': 'Signature on file' if current_index == len(tracking_events) - 1 else None,
            'additional_info': {
                'weight': '2.5 lbs',
                'dimensions': '12x8x6 inches',
                'service_type': 'Ground',
                'reference_number': f"REF{random.randint(100000, 999999)}"
            }
        }
    
    def collect_feedback(self, order_id: str, customer_id: str, feedback_data: Dict) -> Dict:
        """
        Collect and process customer feedback
        
        Args:
            order_id: Order ID
            customer_id: Customer ID
            feedback_data: Feedback information
            
        Returns:
            Feedback collection result
        """
        feedback_id = f"FB{uuid.uuid4().hex[:8].upper()}"
        
        # Process ratings
        overall_rating = feedback_data.get('overall_rating', 0)
        category_ratings = feedback_data.get('category_ratings', {})
        
        # Calculate sentiment
        if overall_rating >= 4:
            sentiment = 'positive'
            response_message = "Thank you for your positive feedback! We're thrilled you had a great experience."
        elif overall_rating >= 3:
            sentiment = 'neutral'
            response_message = "Thank you for your feedback. We're always working to improve our service."
        else:
            sentiment = 'negative'
            response_message = "We're sorry to hear about your experience. Our team will review your feedback immediately."
        
        # Generate rewards for feedback
        rewards = []
        if overall_rating >= 4:
            rewards.append({
                'type': 'loyalty_points',
                'value': 50,
                'description': 'Bonus points for your review'
            })
        
        if feedback_data.get('detailed_review'):
            rewards.append({
                'type': 'discount_code',
                'value': 'THANKS10',
                'description': '10% off your next purchase'
            })
        
        # Store feedback
        feedback_record = {
            'feedback_id': feedback_id,
            'order_id': order_id,
            'customer_id': customer_id,
            'timestamp': datetime.now().isoformat(),
            'overall_rating': overall_rating,
            'category_ratings': category_ratings,
            'review_text': feedback_data.get('review_text', ''),
            'sentiment': sentiment,
            'verified_purchase': True,
            'helpful_count': 0,
            'response_required': sentiment == 'negative'
        }
        
        return {
            'success': True,
            'feedback_id': feedback_id,
            'message': response_message,
            'sentiment': sentiment,
            'rewards': rewards,
            'follow_up': sentiment == 'negative',
            'next_steps': [
                'Your feedback has been recorded',
                'Rewards have been added to your account' if rewards else 'Thank you for your time',
                'A team member will contact you within 24 hours' if sentiment == 'negative' else 'Shop again soon!'
            ]
        }
    
    def handle_complaint(self, complaint_data: Dict, customer_info: Dict) -> Dict:
        """
        Handle customer complaints and issues
        
        Args:
            complaint_data: Complaint details
            customer_info: Customer information
            
        Returns:
            Complaint handling result
        """
        complaint_id = f"CMP{uuid.uuid4().hex[:8].upper()}"
        
        # Categorize complaint
        category = complaint_data.get('category', 'general')
        severity = self._assess_severity(complaint_data, customer_info)
        
        # Determine resolution
        if severity == 'high':
            resolution = {
                'type': 'immediate',
                'action': 'Escalated to supervisor',
                'compensation': 'Full refund + 25% discount on next order',
                'response_time': '1 hour'
            }
        elif severity == 'medium':
            resolution = {
                'type': 'standard',
                'action': 'Assigned to support team',
                'compensation': 'Partial refund or replacement',
                'response_time': '24 hours'
            }
        else:
            resolution = {
                'type': 'routine',
                'action': 'Added to support queue',
                'compensation': '10% discount code',
                'response_time': '48 hours'
            }
        
        return {
            'success': True,
            'complaint_id': complaint_id,
            'category': category,
            'severity': severity,
            'status': 'open',
            'resolution': resolution,
            'assigned_to': f"Agent_{random.randint(100, 999)}",
            'estimated_resolution': (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M'),
            'message': f"Your complaint has been registered (ID: {complaint_id}). {resolution['action']}.",
            'customer_tier_bonus': customer_info.get('tier', 'bronze') in ['gold', 'platinum']
        }
    
    def get_order_history(self, customer_id: str) -> List[Dict]:
        """
        Get customer's order history for support purposes
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List of past orders
        """
        # Mock order history
        orders = []
        for i in range(random.randint(1, 5)):
            order_date = datetime.now() - timedelta(days=random.randint(1, 90))
            orders.append({
                'order_id': f"ORD{uuid.uuid4().hex[:8].upper()}",
                'date': order_date.strftime('%Y-%m-%d'),
                'total': round(random.uniform(50, 500), 2),
                'status': random.choice(['Delivered', 'In Transit', 'Processing', 'Returned']),
                'items_count': random.randint(1, 5),
                'tracking_available': True,
                'return_eligible': (datetime.now() - order_date).days <= 30
            })
        
        return sorted(orders, key=lambda x: x['date'], reverse=True)
    
    def _assess_severity(self, complaint_data: Dict, customer_info: Dict) -> str:
        """Assess complaint severity"""
        # High severity triggers
        high_triggers = ['damaged', 'defective', 'wrong item', 'fraud', 'safety']
        medium_triggers = ['late delivery', 'missing item', 'quality issue']
        
        complaint_text = complaint_data.get('description', '').lower()
        
        # Check for high severity
        if any(trigger in complaint_text for trigger in high_triggers):
            return 'high'
        
        # Premium customers get higher priority
        if customer_info.get('tier') in ['gold', 'platinum']:
            if any(trigger in complaint_text for trigger in medium_triggers):
                return 'high'
            return 'medium'
        
        # Check for medium severity
        if any(trigger in complaint_text for trigger in medium_triggers):
            return 'medium'
        
        return 'low'
