"""
Customer Context Manager - Manages customer data and personalization context
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class CustomerContextManager:
    def __init__(self):
        """Initialize Customer Context Manager with mock customer data"""
        self.customers = self._load_mock_customers()
        self.anonymous_sessions = {}

    def get_customer_context(self, customer_id: str) -> Dict:
        """Get comprehensive customer context"""
        try:
            customer = self.customers.get(customer_id)
            if not customer:
                return self._create_new_customer_context(customer_id)
            
            # Enrich context with behavioral data
            context = customer.copy()
            context['behavioral_data'] = self._get_behavioral_data(customer_id)
            context['recommendations_context'] = self._get_recommendations_context(customer)
            context['current_session'] = {
                'start_time': datetime.now().isoformat(),
                'channel': 'web',
                'location': customer.get('location', 'online')
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting customer context: {str(e)}")
            return self._create_default_context()

    def get_anonymous_context(self, session_id: str) -> Dict:
        """Get context for anonymous users"""
        if session_id not in self.anonymous_sessions:
            self.anonymous_sessions[session_id] = {
                'customer_id': f'ANON-{session_id[:8]}',
                'name': 'Guest',
                'session_id': session_id,
                'is_anonymous': True,
                'preferences': {},
                'purchase_history': [],
                'conversation_history': [],
                'created_at': datetime.now().isoformat()
            }
        
        return self.anonymous_sessions[session_id]

    def update_context(self, customer_id: str, updates: Dict) -> bool:
        """Update customer context with new information"""
        try:
            if customer_id.startswith('ANON-'):
                # Update anonymous session
                session_id = customer_id.replace('ANON-', '')
                if session_id in self.anonymous_sessions:
                    self.anonymous_sessions[session_id].update(updates)
                    return True
            else:
                # Update registered customer
                if customer_id in self.customers:
                    self.customers[customer_id].update(updates)
                    return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error updating customer context: {str(e)}")
            return False

    def get_customer_preferences(self, customer_id: str) -> Dict:
        """Get customer preferences for personalization"""
        customer = self.customers.get(customer_id, {})
        return customer.get('preferences', {})

    def update_preferences(self, customer_id: str, preferences: Dict) -> bool:
        """Update customer preferences"""
        try:
            if customer_id in self.customers:
                current_prefs = self.customers[customer_id].get('preferences', {})
                current_prefs.update(preferences)
                self.customers[customer_id]['preferences'] = current_prefs
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error updating preferences: {str(e)}")
            return False

    def track_interaction(self, customer_id: str, interaction_data: Dict) -> bool:
        """Track customer interaction for behavioral analysis"""
        try:
            interaction = {
                'timestamp': datetime.now().isoformat(),
                'type': interaction_data.get('type', 'message'),
                'content': interaction_data.get('content', ''),
                'channel': interaction_data.get('channel', 'web'),
                'intent': interaction_data.get('intent', 'unknown')
            }
            
            if customer_id in self.customers:
                interactions = self.customers[customer_id].get('interactions', [])
                interactions.append(interaction)
                self.customers[customer_id]['interactions'] = interactions[-50:]  # Keep last 50
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error tracking interaction: {str(e)}")
            return False

    def get_customer_segment(self, customer_id: str) -> str:
        """Determine customer segment for targeting"""
        customer = self.customers.get(customer_id, {})
        purchase_history = customer.get('purchase_history', [])
        membership_tier = customer.get('membership_tier', 'regular')
        
        if not purchase_history:
            return 'new_customer'
        elif len(purchase_history) >= 10 or membership_tier in ['gold', 'platinum']:
            return 'vip_customer'
        else:
            return 'regular_customer'

    def _get_behavioral_data(self, customer_id: str) -> Dict:
        """Get customer behavioral analysis"""
        customer = self.customers.get(customer_id, {})
        purchase_history = customer.get('purchase_history', [])
        interactions = customer.get('interactions', [])
        
        # Analyze purchase patterns
        if purchase_history:
            categories = [item.get('category') for item in purchase_history]
            favorite_category = max(set(categories), key=categories.count) if categories else None
            
            total_spent = sum(item.get('amount', 0) for item in purchase_history)
            avg_order_value = total_spent / len(purchase_history) if purchase_history else 0
        else:
            favorite_category = None
            total_spent = 0
            avg_order_value = 0
        
        # Analyze interaction patterns
        recent_interactions = interactions[-10:] if interactions else []
        common_intents = []
        if recent_interactions:
            intents = [interaction.get('intent') for interaction in recent_interactions]
            common_intents = list(set(intents))
        
        return {
            'favorite_category': favorite_category,
            'total_spent': total_spent,
            'avg_order_value': avg_order_value,
            'purchase_frequency': len(purchase_history),
            'common_intents': common_intents,
            'last_purchase_date': purchase_history[-1].get('date') if purchase_history else None
        }

    def _get_recommendations_context(self, customer: Dict) -> Dict:
        """Get context for recommendation engine"""
        return {
            'preferred_categories': customer.get('preferences', {}).get('categories', []),
            'preferred_brands': customer.get('preferences', {}).get('brands', []),
            'price_sensitivity': customer.get('preferences', {}).get('price_range', {}),
            'recent_views': customer.get('recent_views', []),
            'wishlist': customer.get('wishlist', [])
        }

    def _create_new_customer_context(self, customer_id: str) -> Dict:
        """Create context for new customer"""
        new_customer = {
            'customer_id': customer_id,
            'name': 'Valued Customer',
            'email': f'{customer_id.lower()}@example.com',
            'membership_tier': 'regular',
            'preferences': {},
            'purchase_history': [],
            'conversation_history': [],
            'location': 'online',
            'created_at': datetime.now().isoformat()
        }
        
        self.customers[customer_id] = new_customer
        return new_customer

    def _create_default_context(self) -> Dict:
        """Create default context for error cases"""
        return {
            'customer_id': 'DEFAULT',
            'name': 'Guest',
            'preferences': {},
            'purchase_history': [],
            'conversation_history': [],
            'location': 'online'
        }

    def _load_mock_customers(self) -> Dict:
        """Load mock customer data"""
        return {
            'CUST001': {
                'customer_id': 'CUST001',
                'name': 'Alice Johnson',
                'email': 'alice.johnson@email.com',
                'phone': '+1-555-0101',
                'membership_tier': 'gold',
                'location': 'downtown',
                'preferences': {
                    'categories': ['Electronics', 'Home'],
                    'brands': ['AudioTech', 'SmartHome'],
                    'price_range': {'min': 50, 'max': 500},
                    'communication_channel': 'email'
                },
                'purchase_history': [
                    {
                        'order_id': 'ORD-001',
                        'date': '2024-01-10',
                        'amount': 199.99,
                        'category': 'Electronics',
                        'product': 'Wireless Headphones'
                    },
                    {
                        'order_id': 'ORD-002',
                        'date': '2024-01-05',
                        'amount': 149.99,
                        'category': 'Home',
                        'product': 'Coffee Maker'
                    }
                ],
                'recent_views': ['PROD001', 'PROD004', 'PROD008'],
                'wishlist': ['PROD002', 'PROD005'],
                'conversation_history': [],
                'created_at': '2023-12-01T10:00:00'
            },
            'CUST002': {
                'customer_id': 'CUST002',
                'name': 'Bob Smith',
                'email': 'bob.smith@email.com',
                'phone': '+1-555-0102',
                'membership_tier': 'silver',
                'location': 'mall',
                'preferences': {
                    'categories': ['Sports', 'Clothing'],
                    'brands': ['ZenFit', 'DenimCraft'],
                    'price_range': {'min': 25, 'max': 200},
                    'communication_channel': 'sms'
                },
                'purchase_history': [
                    {
                        'order_id': 'ORD-003',
                        'date': '2024-01-08',
                        'amount': 59.99,
                        'category': 'Sports',
                        'product': 'Yoga Mat'
                    }
                ],
                'recent_views': ['PROD005', 'PROD007'],
                'wishlist': ['PROD003'],
                'conversation_history': [],
                'created_at': '2024-01-01T14:30:00'
            },
            'CUST003': {
                'customer_id': 'CUST003',
                'name': 'Carol Davis',
                'email': 'carol.davis@email.com',
                'phone': '+1-555-0103',
                'membership_tier': 'platinum',
                'location': 'online',
                'preferences': {
                    'categories': ['Electronics', 'Clothing'],
                    'brands': ['FitTech', 'EcoWear'],
                    'price_range': {'min': 100, 'max': 1000},
                    'communication_channel': 'whatsapp'
                },
                'purchase_history': [
                    {
                        'order_id': 'ORD-004',
                        'date': '2024-01-12',
                        'amount': 299.99,
                        'category': 'Electronics',
                        'product': 'Smart Fitness Watch'
                    },
                    {
                        'order_id': 'ORD-005',
                        'date': '2024-01-06',
                        'amount': 29.99,
                        'category': 'Clothing',
                        'product': 'Organic T-Shirt'
                    },
                    {
                        'order_id': 'ORD-006',
                        'date': '2023-12-20',
                        'amount': 129.99,
                        'category': 'Electronics',
                        'product': 'Smart Speaker'
                    }
                ],
                'recent_views': ['PROD002', 'PROD003', 'PROD008'],
                'wishlist': ['PROD001', 'PROD006'],
                'conversation_history': [],
                'created_at': '2023-11-15T09:15:00'
            }
        }
