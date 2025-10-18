"""
Loyalty and Offers Agent - Manages loyalty points, coupon codes, and personalized offers
Calculates final pricing with all applicable discounts and savings
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random
import uuid

logger = logging.getLogger(__name__)

class LoyaltyOffersAgent:
    def __init__(self):
        """Initialize Loyalty and Offers Agent with rewards system"""
        self.loyalty_tiers = {
            'bronze': {'min_points': 0, 'multiplier': 1.0, 'benefits': ['Birthday discount', '5% off']},
            'silver': {'min_points': 500, 'multiplier': 1.5, 'benefits': ['Free shipping', '10% off', 'Early access']},
            'gold': {'min_points': 2000, 'multiplier': 2.0, 'benefits': ['Premium support', '15% off', 'Exclusive deals']},
            'platinum': {'min_points': 5000, 'multiplier': 3.0, 'benefits': ['VIP treatment', '20% off', 'Personal shopper']}
        }
        
        self.active_coupons = {
            'WELCOME10': {'discount': 10, 'type': 'percentage', 'min_purchase': 50, 'valid_until': '2024-12-31'},
            'SAVE20': {'discount': 20, 'type': 'fixed', 'min_purchase': 100, 'valid_until': '2024-12-31'},
            'FREESHIP': {'discount': 100, 'type': 'shipping', 'min_purchase': 75, 'valid_until': '2024-12-31'},
            'BUNDLE15': {'discount': 15, 'type': 'percentage', 'min_purchase': 150, 'valid_until': '2024-12-31'},
            'VIP25': {'discount': 25, 'type': 'percentage', 'min_purchase': 200, 'valid_until': '2024-12-31', 'tier_required': 'gold'}
        }
        
        self.personalized_offers = {
            'frequent_buyer': {'name': 'Frequent Buyer Bonus', 'discount': 15, 'condition': '5+ purchases'},
            'category_lover': {'name': 'Category Specialist', 'discount': 20, 'condition': 'Buy 3+ from same category'},
            'big_spender': {'name': 'Big Spender Reward', 'discount': 25, 'condition': 'Orders over $500'},
            'comeback': {'name': 'We Missed You', 'discount': 30, 'condition': 'First purchase after 30 days'}
        }
        
        # Mock customer loyalty data
        self.customer_loyalty_data = {}
    
    def get_customer_loyalty_status(self, customer_id: str) -> Dict:
        """
        Get customer's loyalty status and points
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Loyalty status information
        """
        # Get or create customer loyalty data
        if customer_id not in self.customer_loyalty_data:
            self.customer_loyalty_data[customer_id] = {
                'points': random.randint(0, 3000),
                'tier': 'bronze',
                'lifetime_value': random.randint(100, 5000),
                'join_date': '2023-01-01',
                'last_purchase': '2024-01-01'
            }
        
        data = self.customer_loyalty_data[customer_id]
        
        # Determine tier based on points
        tier = self._calculate_tier(data['points'])
        tier_info = self.loyalty_tiers[tier]
        
        # Calculate points to next tier
        next_tier = self._get_next_tier(tier)
        points_to_next = 0
        if next_tier:
            points_to_next = self.loyalty_tiers[next_tier]['min_points'] - data['points']
        
        return {
            'customer_id': customer_id,
            'current_points': data['points'],
            'tier': tier,
            'tier_benefits': tier_info['benefits'],
            'points_multiplier': tier_info['multiplier'],
            'points_to_next_tier': points_to_next,
            'next_tier': next_tier,
            'lifetime_value': data['lifetime_value'],
            'member_since': data['join_date'],
            'points_expiring': {
                'amount': random.randint(0, 100),
                'date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            }
        }
    
    def apply_coupon_code(self, code: str, cart: Dict, customer_info: Dict) -> Dict:
        """
        Apply coupon code to cart
        
        Args:
            code: Coupon code
            cart: Shopping cart with items and total
            customer_info: Customer information including tier
            
        Returns:
            Coupon application result with discount details
        """
        code = code.upper()
        
        if code not in self.active_coupons:
            return {
                'success': False,
                'error': 'Invalid coupon code',
                'message': f"The code '{code}' is not valid"
            }
        
        coupon = self.active_coupons[code]
        cart_total = cart.get('subtotal', 0)
        
        # Check validity
        if datetime.now().strftime('%Y-%m-%d') > coupon['valid_until']:
            return {
                'success': False,
                'error': 'Expired coupon',
                'message': f"The code '{code}' has expired"
            }
        
        # Check minimum purchase requirement
        if cart_total < coupon['min_purchase']:
            return {
                'success': False,
                'error': 'Minimum not met',
                'message': f"Minimum purchase of ${coupon['min_purchase']} required"
            }
        
        # Check tier requirement if any
        if 'tier_required' in coupon:
            customer_tier = customer_info.get('tier', 'bronze')
            if not self._is_tier_eligible(customer_tier, coupon['tier_required']):
                return {
                    'success': False,
                    'error': 'Tier requirement not met',
                    'message': f"This coupon requires {coupon['tier_required']} tier or higher"
                }
        
        # Calculate discount
        discount_amount = 0
        if coupon['type'] == 'percentage':
            discount_amount = cart_total * (coupon['discount'] / 100)
        elif coupon['type'] == 'fixed':
            discount_amount = min(coupon['discount'], cart_total)
        elif coupon['type'] == 'shipping':
            discount_amount = cart.get('shipping_cost', 0)
        
        return {
            'success': True,
            'code': code,
            'discount_type': coupon['type'],
            'discount_value': coupon['discount'],
            'discount_amount': round(discount_amount, 2),
            'message': f"Coupon '{code}' applied successfully!",
            'new_total': round(cart_total - discount_amount, 2)
        }
    
    def calculate_loyalty_points(self, order: Dict, customer_info: Dict) -> Dict:
        """
        Calculate loyalty points earned from order
        
        Args:
            order: Order details
            customer_info: Customer information
            
        Returns:
            Points calculation details
        """
        base_points = int(order['total'])  # 1 point per dollar
        tier = customer_info.get('tier', 'bronze')
        multiplier = self.loyalty_tiers[tier]['multiplier']
        
        # Calculate bonus points
        bonus_points = 0
        bonus_reasons = []
        
        # Category bonus
        if order.get('category_count', 0) >= 3:
            bonus_points += 50
            bonus_reasons.append('Multi-category purchase: +50 points')
        
        # High value order bonus
        if order['total'] > 200:
            bonus_points += 100
            bonus_reasons.append('High value order: +100 points')
        
        # Special day bonus (mock)
        if random.random() > 0.7:
            bonus_points += 25
            bonus_reasons.append('Happy Hour bonus: +25 points')
        
        total_points = int((base_points + bonus_points) * multiplier)
        
        return {
            'base_points': base_points,
            'bonus_points': bonus_points,
            'bonus_reasons': bonus_reasons,
            'multiplier': multiplier,
            'total_points_earned': total_points,
            'new_balance': customer_info.get('current_points', 0) + total_points,
            'tier_progress': self._calculate_tier_progress(
                customer_info.get('current_points', 0) + total_points
            )
        }
    
    def get_personalized_offers(self, customer_id: str, purchase_history: List[Dict]) -> List[Dict]:
        """
        Get personalized offers for customer
        
        Args:
            customer_id: Customer ID
            purchase_history: Customer's purchase history
            
        Returns:
            List of personalized offers
        """
        offers = []
        
        # Analyze purchase patterns
        total_purchases = len(purchase_history)
        total_spent = sum(p.get('total', 0) for p in purchase_history)
        
        # Frequent buyer offer
        if total_purchases >= 5:
            offer = self.personalized_offers['frequent_buyer'].copy()
            offer['code'] = f"FREQ{customer_id[:4].upper()}"
            offer['valid_until'] = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            offers.append(offer)
        
        # Big spender offer
        if total_spent > 500:
            offer = self.personalized_offers['big_spender'].copy()
            offer['code'] = f"BIG{customer_id[:4].upper()}"
            offer['valid_until'] = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            offers.append(offer)
        
        # Category specialist offer
        categories = {}
        for purchase in purchase_history:
            cat = purchase.get('category', 'general')
            categories[cat] = categories.get(cat, 0) + 1
        
        for category, count in categories.items():
            if count >= 3:
                offer = self.personalized_offers['category_lover'].copy()
                offer['code'] = f"CAT{category[:3].upper()}"
                offer['category'] = category
                offer['valid_until'] = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
                offers.append(offer)
                break
        
        # Comeback offer
        if purchase_history:
            last_purchase = datetime.strptime(purchase_history[-1].get('date', '2024-01-01'), '%Y-%m-%d')
            days_since = (datetime.now() - last_purchase).days
            if days_since > 30:
                offer = self.personalized_offers['comeback'].copy()
                offer['code'] = f"BACK{customer_id[:4].upper()}"
                offer['valid_until'] = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
                offers.append(offer)
        
        return offers
    
    def calculate_final_price(self, cart: Dict, applied_discounts: List[Dict], customer_info: Dict) -> Dict:
        """
        Calculate final price with all discounts and loyalty benefits
        
        Args:
            cart: Shopping cart
            applied_discounts: List of applied discounts
            customer_info: Customer information
            
        Returns:
            Final pricing breakdown
        """
        subtotal = cart.get('subtotal', 0)
        shipping = cart.get('shipping_cost', 10)
        tax_rate = 0.08  # 8% tax
        
        # Apply discounts
        total_discount = 0
        discount_breakdown = []
        
        for discount in applied_discounts:
            amount = discount.get('amount', 0)
            total_discount += amount
            discount_breakdown.append({
                'type': discount.get('type'),
                'description': discount.get('description'),
                'amount': amount
            })
        
        # Apply tier discount
        tier = customer_info.get('tier', 'bronze')
        tier_discount_percent = {'bronze': 5, 'silver': 10, 'gold': 15, 'platinum': 20}
        tier_discount = subtotal * (tier_discount_percent.get(tier, 0) / 100)
        
        if tier_discount > 0:
            total_discount += tier_discount
            discount_breakdown.append({
                'type': 'loyalty',
                'description': f'{tier.capitalize()} tier discount',
                'amount': tier_discount
            })
        
        # Calculate totals
        discounted_subtotal = subtotal - total_discount
        tax = discounted_subtotal * tax_rate
        final_total = discounted_subtotal + shipping + tax
        
        # Calculate savings
        total_savings = total_discount
        savings_percentage = (total_savings / subtotal * 100) if subtotal > 0 else 0
        
        return {
            'subtotal': round(subtotal, 2),
            'shipping': round(shipping, 2),
            'tax': round(tax, 2),
            'total_discount': round(total_discount, 2),
            'discount_breakdown': discount_breakdown,
            'final_total': round(final_total, 2),
            'total_savings': round(total_savings, 2),
            'savings_percentage': round(savings_percentage, 1),
            'loyalty_points_earned': int(final_total),
            'payment_due': round(final_total, 2)
        }
    
    def redeem_points(self, customer_id: str, points_to_redeem: int) -> Dict:
        """
        Redeem loyalty points for rewards
        
        Args:
            customer_id: Customer ID
            points_to_redeem: Number of points to redeem
            
        Returns:
            Redemption result
        """
        customer_data = self.customer_loyalty_data.get(customer_id, {})
        current_points = customer_data.get('points', 0)
        
        if points_to_redeem > current_points:
            return {
                'success': False,
                'error': 'Insufficient points',
                'message': f'You have {current_points} points available'
            }
        
        # Calculate reward value (100 points = $10)
        reward_value = points_to_redeem / 10
        
        # Update points
        customer_data['points'] = current_points - points_to_redeem
        self.customer_loyalty_data[customer_id] = customer_data
        
        # Generate reward code
        reward_code = f"REWARD{uuid.uuid4().hex[:6].upper()}"
        
        return {
            'success': True,
            'points_redeemed': points_to_redeem,
            'reward_value': round(reward_value, 2),
            'reward_code': reward_code,
            'remaining_points': customer_data['points'],
            'message': f'Successfully redeemed {points_to_redeem} points for ${reward_value:.2f}'
        }
    
    def _calculate_tier(self, points: int) -> str:
        """Calculate tier based on points"""
        if points >= 5000:
            return 'platinum'
        elif points >= 2000:
            return 'gold'
        elif points >= 500:
            return 'silver'
        else:
            return 'bronze'
    
    def _get_next_tier(self, current_tier: str) -> str:
        """Get next tier level"""
        tiers = ['bronze', 'silver', 'gold', 'platinum']
        current_index = tiers.index(current_tier)
        if current_index < len(tiers) - 1:
            return tiers[current_index + 1]
        return None
    
    def _is_tier_eligible(self, customer_tier: str, required_tier: str) -> bool:
        """Check if customer tier meets requirement"""
        tier_levels = {'bronze': 0, 'silver': 1, 'gold': 2, 'platinum': 3}
        return tier_levels.get(customer_tier, 0) >= tier_levels.get(required_tier, 0)
    
    def _calculate_tier_progress(self, points: int) -> Dict:
        """Calculate progress to next tier"""
        current_tier = self._calculate_tier(points)
        next_tier = self._get_next_tier(current_tier)
        
        if not next_tier:
            return {
                'current_tier': current_tier,
                'next_tier': None,
                'progress_percentage': 100,
                'points_needed': 0
            }
        
        current_min = self.loyalty_tiers[current_tier]['min_points']
        next_min = self.loyalty_tiers[next_tier]['min_points']
        progress = ((points - current_min) / (next_min - current_min)) * 100
        
        return {
            'current_tier': current_tier,
            'next_tier': next_tier,
            'progress_percentage': min(progress, 100),
            'points_needed': max(0, next_min - points)
        }
