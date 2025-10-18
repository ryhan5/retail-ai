"""
Promotion Agent - Handles promotions, discounts, and special offers
Manages promotional campaigns and applies relevant discounts
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class PromotionAgent:
    def __init__(self):
        """Initialize Promotion Agent with promotional data"""
        self.active_promotions = self._load_active_promotions()
        self.promotion_rules = self._load_promotion_rules()
        self.customer_segments = self._load_customer_segments()

    def get_applicable_promotions(self, customer_id: str = None, membership_tier: str = 'regular') -> List[Dict]:
        """
        Get promotions applicable to a specific customer
        
        Args:
            customer_id: Customer identifier
            membership_tier: Customer's membership level
            
        Returns:
            List of applicable promotions
        """
        try:
            applicable_promotions = []
            current_time = datetime.now()
            
            for promotion in self.active_promotions:
                # Check if promotion is currently active
                start_date = datetime.fromisoformat(promotion['start_date'])
                end_date = datetime.fromisoformat(promotion['end_date'])
                
                if not (start_date <= current_time <= end_date):
                    continue
                
                # Check customer eligibility
                if self._is_customer_eligible(promotion, customer_id, membership_tier):
                    applicable_promotions.append(promotion)
            
            # Sort by priority and discount value
            applicable_promotions.sort(
                key=lambda x: (x.get('priority', 0), x.get('discount_value', 0)), 
                reverse=True
            )
            
            return applicable_promotions
            
        except Exception as e:
            logger.error(f"Error getting applicable promotions: {str(e)}")
            return []

    def apply_promotion(self, promotion_code: str, cart_items: List[Dict], customer_id: str = None) -> Dict:
        """
        Apply a promotion code to cart items
        
        Args:
            promotion_code: Promotion code to apply
            cart_items: Items in customer's cart
            customer_id: Customer identifier
            
        Returns:
            Dict with promotion application results
        """
        try:
            # Find promotion by code
            promotion = next(
                (p for p in self.active_promotions if p.get('code') == promotion_code.upper()), 
                None
            )
            
            if not promotion:
                return {
                    'success': False,
                    'message': 'Invalid promotion code',
                    'discount_amount': 0
                }
            
            # Check if promotion is active
            current_time = datetime.now()
            start_date = datetime.fromisoformat(promotion['start_date'])
            end_date = datetime.fromisoformat(promotion['end_date'])
            
            if not (start_date <= current_time <= end_date):
                return {
                    'success': False,
                    'message': 'This promotion has expired',
                    'discount_amount': 0
                }
            
            # Check customer eligibility
            if not self._is_customer_eligible(promotion, customer_id):
                return {
                    'success': False,
                    'message': 'You are not eligible for this promotion',
                    'discount_amount': 0
                }
            
            # Calculate discount
            discount_result = self._calculate_discount(promotion, cart_items)
            
            if discount_result['applicable']:
                return {
                    'success': True,
                    'message': f"Promotion applied! You saved ${discount_result['discount_amount']:.2f}",
                    'discount_amount': discount_result['discount_amount'],
                    'promotion_details': promotion,
                    'affected_items': discount_result['affected_items']
                }
            else:
                return {
                    'success': False,
                    'message': discount_result['reason'],
                    'discount_amount': 0
                }
            
        except Exception as e:
            logger.error(f"Error applying promotion {promotion_code}: {str(e)}")
            return {
                'success': False,
                'message': 'Error applying promotion code',
                'discount_amount': 0
            }

    def get_cart_promotions(self, cart_items: List[Dict], customer_id: str = None) -> List[Dict]:
        """
        Get automatic promotions that apply to current cart
        
        Args:
            cart_items: Items in customer's cart
            customer_id: Customer identifier
            
        Returns:
            List of automatic promotions
        """
        try:
            if not cart_items:
                return []
            
            automatic_promotions = []
            cart_total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
            
            for promotion in self.active_promotions:
                if promotion.get('automatic', False):
                    # Check if promotion applies to cart
                    if self._promotion_applies_to_cart(promotion, cart_items, cart_total):
                        discount_result = self._calculate_discount(promotion, cart_items)
                        if discount_result['applicable']:
                            promotion_copy = promotion.copy()
                            promotion_copy['discount_amount'] = discount_result['discount_amount']
                            promotion_copy['affected_items'] = discount_result['affected_items']
                            automatic_promotions.append(promotion_copy)
            
            return automatic_promotions
            
        except Exception as e:
            logger.error(f"Error getting cart promotions: {str(e)}")
            return []

    def get_upsell_promotions(self, current_cart_total: float, customer_id: str = None) -> List[Dict]:
        """
        Get promotions that encourage higher spending
        
        Args:
            current_cart_total: Current cart total amount
            customer_id: Customer identifier
            
        Returns:
            List of upsell promotions
        """
        try:
            upsell_promotions = []
            
            for promotion in self.active_promotions:
                promotion_type = promotion.get('type')
                
                # Free shipping threshold promotions
                if promotion_type == 'free_shipping':
                    threshold = promotion.get('minimum_amount', 0)
                    if current_cart_total < threshold:
                        amount_needed = threshold - current_cart_total
                        promotion_copy = promotion.copy()
                        promotion_copy['upsell_message'] = f"Add ${amount_needed:.2f} more for free shipping!"
                        promotion_copy['amount_needed'] = amount_needed
                        upsell_promotions.append(promotion_copy)
                
                # Spend threshold promotions
                elif promotion_type == 'spend_threshold':
                    threshold = promotion.get('minimum_amount', 0)
                    if current_cart_total < threshold:
                        amount_needed = threshold - current_cart_total
                        discount_value = promotion.get('discount_value', 0)
                        promotion_copy = promotion.copy()
                        promotion_copy['upsell_message'] = f"Spend ${amount_needed:.2f} more and save ${discount_value:.2f}!"
                        promotion_copy['amount_needed'] = amount_needed
                        upsell_promotions.append(promotion_copy)
            
            # Sort by amount needed (ascending)
            upsell_promotions.sort(key=lambda x: x.get('amount_needed', 0))
            
            return upsell_promotions[:3]  # Return top 3 upsell opportunities
            
        except Exception as e:
            logger.error(f"Error getting upsell promotions: {str(e)}")
            return []

    def create_personalized_offer(self, customer_id: str, customer_data: Dict) -> Dict:
        """
        Create a personalized promotional offer for a customer
        
        Args:
            customer_id: Customer identifier
            customer_data: Customer profile and behavior data
            
        Returns:
            Dict with personalized offer details
        """
        try:
            # Analyze customer behavior to create targeted offer
            purchase_history = customer_data.get('purchase_history', [])
            preferences = customer_data.get('preferences', {})
            membership_tier = customer_data.get('membership_tier', 'regular')
            
            # Determine offer type based on customer profile
            if not purchase_history:
                # New customer offer
                offer = self._create_new_customer_offer()
            elif len(purchase_history) >= 5:
                # Loyal customer offer
                offer = self._create_loyal_customer_offer(customer_data)
            else:
                # Regular customer offer
                offer = self._create_regular_customer_offer(customer_data)
            
            # Personalize offer details
            offer['customer_id'] = customer_id
            offer['created_at'] = datetime.now().isoformat()
            offer['expires_at'] = (datetime.now() + timedelta(days=7)).isoformat()
            
            return offer
            
        except Exception as e:
            logger.error(f"Error creating personalized offer: {str(e)}")
            return {}

    def validate_promotion_stack(self, applied_promotions: List[Dict]) -> Dict:
        """
        Validate if multiple promotions can be stacked together
        
        Args:
            applied_promotions: List of promotions to be applied
            
        Returns:
            Dict with validation results
        """
        try:
            if len(applied_promotions) <= 1:
                return {'valid': True, 'message': 'Single promotion is valid'}
            
            # Check stacking rules
            stackable_promotions = []
            non_stackable_found = False
            
            for promotion in applied_promotions:
                if promotion.get('stackable', True):
                    stackable_promotions.append(promotion)
                else:
                    if non_stackable_found:
                        return {
                            'valid': False,
                            'message': 'Cannot combine multiple non-stackable promotions'
                        }
                    non_stackable_found = True
            
            # Check for conflicting promotion types
            promotion_types = [p.get('type') for p in applied_promotions]
            if len(set(promotion_types)) != len(promotion_types):
                return {
                    'valid': False,
                    'message': 'Cannot apply multiple promotions of the same type'
                }
            
            return {
                'valid': True,
                'message': f'Successfully stacked {len(applied_promotions)} promotions'
            }
            
        except Exception as e:
            logger.error(f"Error validating promotion stack: {str(e)}")
            return {'valid': False, 'message': 'Error validating promotions'}

    # Private helper methods

    def _is_customer_eligible(self, promotion: Dict, customer_id: str = None, membership_tier: str = 'regular') -> bool:
        """Check if customer is eligible for promotion"""
        # Check membership tier requirements
        required_tier = promotion.get('required_membership_tier')
        if required_tier:
            tier_hierarchy = {'regular': 1, 'silver': 2, 'gold': 3, 'platinum': 4}
            customer_tier_level = tier_hierarchy.get(membership_tier, 1)
            required_tier_level = tier_hierarchy.get(required_tier, 1)
            
            if customer_tier_level < required_tier_level:
                return False
        
        # Check customer segment requirements
        eligible_segments = promotion.get('eligible_segments', [])
        if eligible_segments and customer_id:
            customer_segment = self._get_customer_segment(customer_id)
            if customer_segment not in eligible_segments:
                return False
        
        # Check usage limits
        max_uses = promotion.get('max_uses_per_customer')
        if max_uses and customer_id:
            current_uses = self._get_customer_promotion_usage(customer_id, promotion['id'])
            if current_uses >= max_uses:
                return False
        
        return True

    def _calculate_discount(self, promotion: Dict, cart_items: List[Dict]) -> Dict:
        """Calculate discount amount for promotion"""
        promotion_type = promotion.get('type')
        
        if promotion_type == 'percentage':
            return self._calculate_percentage_discount(promotion, cart_items)
        elif promotion_type == 'fixed_amount':
            return self._calculate_fixed_discount(promotion, cart_items)
        elif promotion_type == 'buy_x_get_y':
            return self._calculate_bogo_discount(promotion, cart_items)
        elif promotion_type == 'free_shipping':
            return self._calculate_shipping_discount(promotion, cart_items)
        elif promotion_type == 'spend_threshold':
            return self._calculate_threshold_discount(promotion, cart_items)
        else:
            return {'applicable': False, 'reason': 'Unknown promotion type'}

    def _calculate_percentage_discount(self, promotion: Dict, cart_items: List[Dict]) -> Dict:
        """Calculate percentage-based discount"""
        discount_percentage = promotion.get('discount_value', 0) / 100
        eligible_items = self._get_eligible_items(promotion, cart_items)
        
        if not eligible_items:
            return {'applicable': False, 'reason': 'No eligible items in cart'}
        
        subtotal = sum(item['price'] * item.get('quantity', 1) for item in eligible_items)
        discount_amount = subtotal * discount_percentage
        
        # Apply maximum discount limit if specified
        max_discount = promotion.get('max_discount_amount')
        if max_discount and discount_amount > max_discount:
            discount_amount = max_discount
        
        return {
            'applicable': True,
            'discount_amount': discount_amount,
            'affected_items': eligible_items
        }

    def _calculate_fixed_discount(self, promotion: Dict, cart_items: List[Dict]) -> Dict:
        """Calculate fixed amount discount"""
        discount_amount = promotion.get('discount_value', 0)
        eligible_items = self._get_eligible_items(promotion, cart_items)
        
        if not eligible_items:
            return {'applicable': False, 'reason': 'No eligible items in cart'}
        
        subtotal = sum(item['price'] * item.get('quantity', 1) for item in eligible_items)
        
        # Don't allow discount to exceed subtotal
        if discount_amount > subtotal:
            discount_amount = subtotal
        
        return {
            'applicable': True,
            'discount_amount': discount_amount,
            'affected_items': eligible_items
        }

    def _calculate_bogo_discount(self, promotion: Dict, cart_items: List[Dict]) -> Dict:
        """Calculate Buy X Get Y discount"""
        buy_quantity = promotion.get('buy_quantity', 1)
        get_quantity = promotion.get('get_quantity', 1)
        eligible_items = self._get_eligible_items(promotion, cart_items)
        
        if not eligible_items:
            return {'applicable': False, 'reason': 'No eligible items in cart'}
        
        total_quantity = sum(item.get('quantity', 1) for item in eligible_items)
        
        if total_quantity < buy_quantity:
            return {'applicable': False, 'reason': f'Need at least {buy_quantity} items'}
        
        # Calculate how many free items customer gets
        free_items_count = (total_quantity // buy_quantity) * get_quantity
        
        # Find cheapest items to discount
        sorted_items = sorted(eligible_items, key=lambda x: x['price'])
        discount_amount = 0
        
        for item in sorted_items:
            item_quantity = item.get('quantity', 1)
            items_to_discount = min(free_items_count, item_quantity)
            discount_amount += item['price'] * items_to_discount
            free_items_count -= items_to_discount
            
            if free_items_count <= 0:
                break
        
        return {
            'applicable': True,
            'discount_amount': discount_amount,
            'affected_items': eligible_items
        }

    def _calculate_shipping_discount(self, promotion: Dict, cart_items: List[Dict]) -> Dict:
        """Calculate free shipping discount"""
        minimum_amount = promotion.get('minimum_amount', 0)
        cart_total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
        
        if cart_total < minimum_amount:
            return {'applicable': False, 'reason': f'Minimum order of ${minimum_amount:.2f} required'}
        
        shipping_cost = promotion.get('shipping_discount', 9.99)  # Default shipping cost
        
        return {
            'applicable': True,
            'discount_amount': shipping_cost,
            'affected_items': cart_items,
            'discount_type': 'shipping'
        }

    def _calculate_threshold_discount(self, promotion: Dict, cart_items: List[Dict]) -> Dict:
        """Calculate spend threshold discount"""
        minimum_amount = promotion.get('minimum_amount', 0)
        cart_total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
        
        if cart_total < minimum_amount:
            return {'applicable': False, 'reason': f'Minimum spend of ${minimum_amount:.2f} required'}
        
        discount_amount = promotion.get('discount_value', 0)
        
        return {
            'applicable': True,
            'discount_amount': discount_amount,
            'affected_items': cart_items
        }

    def _get_eligible_items(self, promotion: Dict, cart_items: List[Dict]) -> List[Dict]:
        """Get items eligible for promotion"""
        eligible_categories = promotion.get('eligible_categories', [])
        eligible_products = promotion.get('eligible_products', [])
        excluded_categories = promotion.get('excluded_categories', [])
        excluded_products = promotion.get('excluded_products', [])
        
        if not eligible_categories and not eligible_products:
            # If no specific eligibility criteria, all items are eligible
            eligible_items = cart_items.copy()
        else:
            eligible_items = []
            for item in cart_items:
                # Check category eligibility
                if eligible_categories and item.get('category') in eligible_categories:
                    eligible_items.append(item)
                # Check product eligibility
                elif eligible_products and item.get('id') in eligible_products:
                    eligible_items.append(item)
        
        # Remove excluded items
        final_eligible_items = []
        for item in eligible_items:
            if item.get('category') not in excluded_categories and item.get('id') not in excluded_products:
                final_eligible_items.append(item)
        
        return final_eligible_items

    def _promotion_applies_to_cart(self, promotion: Dict, cart_items: List[Dict], cart_total: float) -> bool:
        """Check if promotion applies to current cart"""
        # Check minimum amount requirement
        minimum_amount = promotion.get('minimum_amount', 0)
        if cart_total < minimum_amount:
            return False
        
        # Check if cart has eligible items
        eligible_items = self._get_eligible_items(promotion, cart_items)
        return len(eligible_items) > 0

    def _get_customer_segment(self, customer_id: str) -> str:
        """Get customer segment for targeting"""
        # Mock implementation - in real system, this would query customer database
        return random.choice(['new_customer', 'regular_customer', 'vip_customer'])

    def _get_customer_promotion_usage(self, customer_id: str, promotion_id: str) -> int:
        """Get how many times customer has used this promotion"""
        # Mock implementation - in real system, this would query usage database
        return random.randint(0, 2)

    def _create_new_customer_offer(self) -> Dict:
        """Create offer for new customers"""
        return {
            'id': f'NEW-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'title': 'Welcome! 20% Off Your First Order',
            'description': 'Get 20% off your first purchase with us!',
            'type': 'percentage',
            'discount_value': 20,
            'code': f'WELCOME{random.randint(100, 999)}',
            'minimum_amount': 50,
            'max_uses_per_customer': 1
        }

    def _create_loyal_customer_offer(self, customer_data: Dict) -> Dict:
        """Create offer for loyal customers"""
        return {
            'id': f'LOYAL-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'title': 'VIP Customer: 25% Off + Free Shipping',
            'description': 'Thank you for your loyalty! Enjoy 25% off and free shipping.',
            'type': 'percentage',
            'discount_value': 25,
            'code': f'VIP{random.randint(100, 999)}',
            'includes_free_shipping': True,
            'max_uses_per_customer': 1
        }

    def _create_regular_customer_offer(self, customer_data: Dict) -> Dict:
        """Create offer for regular customers"""
        return {
            'id': f'REG-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'title': '15% Off Your Next Purchase',
            'description': 'Special discount just for you!',
            'type': 'percentage',
            'discount_value': 15,
            'code': f'SAVE{random.randint(100, 999)}',
            'minimum_amount': 75,
            'max_uses_per_customer': 1
        }

    def _load_active_promotions(self) -> List[Dict]:
        """Load active promotions data"""
        return [
            {
                'id': 'PROMO001',
                'title': 'Summer Sale - 30% Off Electronics',
                'description': '30% off all electronics for a limited time',
                'type': 'percentage',
                'discount_value': 30,
                'code': 'SUMMER30',
                'start_date': '2024-01-01T00:00:00',
                'end_date': '2024-12-31T23:59:59',
                'eligible_categories': ['Electronics'],
                'minimum_amount': 100,
                'stackable': False,
                'automatic': False,
                'priority': 10
            },
            {
                'id': 'PROMO002',
                'title': 'Free Shipping on Orders Over $75',
                'description': 'Get free shipping when you spend $75 or more',
                'type': 'free_shipping',
                'shipping_discount': 9.99,
                'start_date': '2024-01-01T00:00:00',
                'end_date': '2024-12-31T23:59:59',
                'minimum_amount': 75,
                'stackable': True,
                'automatic': True,
                'priority': 5
            },
            {
                'id': 'PROMO003',
                'title': 'Buy 2 Get 1 Free - Clothing',
                'description': 'Buy any 2 clothing items and get the cheapest one free',
                'type': 'buy_x_get_y',
                'buy_quantity': 2,
                'get_quantity': 1,
                'start_date': '2024-01-01T00:00:00',
                'end_date': '2024-12-31T23:59:59',
                'eligible_categories': ['Clothing'],
                'stackable': False,
                'automatic': True,
                'priority': 8
            },
            {
                'id': 'PROMO004',
                'title': 'VIP Members: Extra 10% Off',
                'description': 'VIP members get an additional 10% off everything',
                'type': 'percentage',
                'discount_value': 10,
                'code': 'VIP10',
                'start_date': '2024-01-01T00:00:00',
                'end_date': '2024-12-31T23:59:59',
                'required_membership_tier': 'gold',
                'stackable': True,
                'automatic': False,
                'priority': 7
            },
            {
                'id': 'PROMO005',
                'title': 'Spend $200, Save $25',
                'description': 'Save $25 when you spend $200 or more',
                'type': 'spend_threshold',
                'discount_value': 25,
                'start_date': '2024-01-01T00:00:00',
                'end_date': '2024-12-31T23:59:59',
                'minimum_amount': 200,
                'stackable': True,
                'automatic': True,
                'priority': 6
            }
        ]

    def _load_promotion_rules(self) -> Dict:
        """Load promotion business rules"""
        return {
            'max_stacked_promotions': 3,
            'max_total_discount_percentage': 70,
            'stackable_types': ['percentage', 'free_shipping', 'spend_threshold'],
            'non_stackable_types': ['buy_x_get_y']
        }

    def _load_customer_segments(self) -> Dict:
        """Load customer segmentation data"""
        return {
            'new_customer': {
                'criteria': 'No previous purchases',
                'typical_offers': ['welcome_discount', 'first_purchase_bonus']
            },
            'regular_customer': {
                'criteria': '1-4 previous purchases',
                'typical_offers': ['percentage_discount', 'free_shipping']
            },
            'vip_customer': {
                'criteria': '5+ previous purchases or high value',
                'typical_offers': ['exclusive_discount', 'early_access', 'free_shipping']
            }
        }
