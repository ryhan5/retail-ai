"""
Recommendation Agent - Provides personalized product recommendations
Uses customer preferences, purchase history, and behavioral data
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class RecommendationAgent:
    def __init__(self):
        """Initialize Recommendation Agent with product catalog and algorithms"""
        self.product_catalog = self._load_product_catalog()
        self.recommendation_algorithms = {
            'collaborative_filtering': self._collaborative_filtering,
            'content_based': self._content_based_filtering,
            'popularity_based': self._popularity_based,
            'hybrid': self._hybrid_recommendations
        }

    def search_products(self, query: str, customer_preferences: Dict = None, 
                       purchase_history: List = None) -> List[Dict]:
        """
        Search products based on query and personalize results
        
        Args:
            query: Search query string
            customer_preferences: Customer preference data
            purchase_history: Customer's purchase history
            
        Returns:
            List of relevant products with personalization
        """
        try:
            # Basic text search in product catalog
            matching_products = []
            query_terms = query.lower().split()
            
            for product in self.product_catalog:
                # Check if query terms match product name, description, or category
                searchable_text = f"{product['name']} {product['description']} {product['category']}".lower()
                
                match_score = 0
                for term in query_terms:
                    if term in searchable_text:
                        match_score += 1
                
                if match_score > 0:
                    product_copy = product.copy()
                    product_copy['relevance_score'] = match_score / len(query_terms)
                    matching_products.append(product_copy)
            
            # Sort by relevance
            matching_products.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Apply personalization if customer data available
            if customer_preferences or purchase_history:
                matching_products = self._personalize_results(
                    matching_products, customer_preferences, purchase_history
                )
            
            return matching_products[:10]  # Return top 10 results
            
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return []

    def get_personalized_recommendations(self, customer_preferences: Dict, 
                                       purchase_history: List, context: Dict = None) -> List[Dict]:
        """
        Get personalized product recommendations
        
        Args:
            customer_preferences: Customer preference data
            purchase_history: Customer's purchase history
            context: Current conversation context
            
        Returns:
            List of recommended products with reasoning
        """
        try:
            # Use hybrid approach combining multiple algorithms
            recommendations = self.recommendation_algorithms['hybrid'](
                customer_preferences, purchase_history, context
            )
            
            # Add recommendation reasons
            for rec in recommendations:
                rec['reason'] = self._generate_recommendation_reason(
                    rec, customer_preferences, purchase_history
                )
            
            return recommendations[:5]  # Return top 5 recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_fallback_recommendations()

    def get_alternatives(self, original_query: str) -> List[Dict]:
        """
        Get alternative product suggestions when original search fails
        
        Args:
            original_query: Original search query that failed
            
        Returns:
            List of alternative products
        """
        try:
            # Extract category hints from query
            category_hints = self._extract_category_hints(original_query)
            
            alternatives = []
            for hint in category_hints:
                category_products = [p for p in self.product_catalog if hint in p['category'].lower()]
                alternatives.extend(category_products[:3])  # Top 3 from each category
            
            # If no category hints, return popular products
            if not alternatives:
                alternatives = self._popularity_based({}, [])
            
            return alternatives[:8]  # Return up to 8 alternatives
            
        except Exception as e:
            logger.error(f"Error getting alternatives: {str(e)}")
            return self._get_fallback_recommendations()

    def get_cross_sell_recommendations(self, cart_items: List[Dict]) -> List[Dict]:
        """
        Get cross-sell recommendations based on cart contents
        
        Args:
            cart_items: Items currently in customer's cart
            
        Returns:
            List of complementary products
        """
        try:
            if not cart_items:
                return []
            
            cross_sell_products = []
            
            for item in cart_items:
                # Find complementary products
                complementary = self._find_complementary_products(item)
                cross_sell_products.extend(complementary)
            
            # Remove duplicates and items already in cart
            cart_product_ids = {item['id'] for item in cart_items}
            unique_cross_sells = []
            seen_ids = set()
            
            for product in cross_sell_products:
                if product['id'] not in cart_product_ids and product['id'] not in seen_ids:
                    unique_cross_sells.append(product)
                    seen_ids.add(product['id'])
            
            return unique_cross_sells[:4]  # Return top 4 cross-sell items
            
        except Exception as e:
            logger.error(f"Error getting cross-sell recommendations: {str(e)}")
            return []

    def get_upsell_recommendations(self, product_id: str) -> List[Dict]:
        """
        Get upsell recommendations for a specific product
        
        Args:
            product_id: ID of the product to find upsells for
            
        Returns:
            List of higher-value alternative products
        """
        try:
            base_product = next((p for p in self.product_catalog if p['id'] == product_id), None)
            if not base_product:
                return []
            
            # Find products in same category with higher price
            upsell_candidates = [
                p for p in self.product_catalog 
                if p['category'] == base_product['category'] 
                and p['price'] > base_product['price']
                and p['id'] != product_id
            ]
            
            # Sort by price (ascending) to show reasonable upgrades first
            upsell_candidates.sort(key=lambda x: x['price'])
            
            # Add upsell reasoning
            for product in upsell_candidates:
                product['upsell_reason'] = self._generate_upsell_reason(base_product, product)
            
            return upsell_candidates[:3]  # Return top 3 upsell options
            
        except Exception as e:
            logger.error(f"Error getting upsell recommendations: {str(e)}")
            return []

    # Private methods for recommendation algorithms

    def _collaborative_filtering(self, customer_preferences: Dict, purchase_history: List, context: Dict = None) -> List[Dict]:
        """Collaborative filtering based on similar customers"""
        # Mock implementation - in real system, this would use customer similarity matrix
        similar_customers_purchases = [
            'PROD001', 'PROD003', 'PROD005', 'PROD007'
        ]
        
        recommendations = [
            p for p in self.product_catalog 
            if p['id'] in similar_customers_purchases
        ]
        
        return recommendations

    def _content_based_filtering(self, customer_preferences: Dict, purchase_history: List, context: Dict = None) -> List[Dict]:
        """Content-based filtering using customer preferences"""
        if not customer_preferences:
            return []
        
        preferred_categories = customer_preferences.get('categories', [])
        preferred_brands = customer_preferences.get('brands', [])
        price_range = customer_preferences.get('price_range', {})
        
        recommendations = []
        
        for product in self.product_catalog:
            score = 0
            
            # Category preference
            if product['category'] in preferred_categories:
                score += 3
            
            # Brand preference
            if product['brand'] in preferred_brands:
                score += 2
            
            # Price range preference
            min_price = price_range.get('min', 0)
            max_price = price_range.get('max', float('inf'))
            if min_price <= product['price'] <= max_price:
                score += 1
            
            if score > 0:
                product_copy = product.copy()
                product_copy['content_score'] = score
                recommendations.append(product_copy)
        
        recommendations.sort(key=lambda x: x['content_score'], reverse=True)
        return recommendations

    def _popularity_based(self, customer_preferences: Dict, purchase_history: List, context: Dict = None) -> List[Dict]:
        """Popularity-based recommendations"""
        # Mock popularity scores - in real system, this would be based on actual sales data
        popular_products = sorted(
            self.product_catalog, 
            key=lambda x: x.get('popularity_score', 0), 
            reverse=True
        )
        
        return popular_products[:8]

    def _hybrid_recommendations(self, customer_preferences: Dict, purchase_history: List, context: Dict = None) -> List[Dict]:
        """Hybrid approach combining multiple algorithms"""
        # Get recommendations from different algorithms
        collaborative = self._collaborative_filtering(customer_preferences, purchase_history, context)
        content_based = self._content_based_filtering(customer_preferences, purchase_history, context)
        popularity = self._popularity_based(customer_preferences, purchase_history, context)
        
        # Combine and weight the results
        all_recommendations = {}
        
        # Weight collaborative filtering results
        for i, product in enumerate(collaborative[:5]):
            score = (5 - i) * 0.4  # Higher weight for collaborative filtering
            all_recommendations[product['id']] = all_recommendations.get(product['id'], 0) + score
        
        # Weight content-based results
        for i, product in enumerate(content_based[:5]):
            score = (5 - i) * 0.3
            all_recommendations[product['id']] = all_recommendations.get(product['id'], 0) + score
        
        # Weight popularity results
        for i, product in enumerate(popularity[:5]):
            score = (5 - i) * 0.3
            all_recommendations[product['id']] = all_recommendations.get(product['id'], 0) + score
        
        # Sort by combined score and return products
        sorted_recommendations = sorted(
            all_recommendations.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        final_recommendations = []
        for product_id, score in sorted_recommendations:
            product = next((p for p in self.product_catalog if p['id'] == product_id), None)
            if product:
                product_copy = product.copy()
                product_copy['hybrid_score'] = score
                final_recommendations.append(product_copy)
        
        return final_recommendations

    def _personalize_results(self, products: List[Dict], customer_preferences: Dict, purchase_history: List) -> List[Dict]:
        """Apply personalization to search results"""
        if not customer_preferences and not purchase_history:
            return products
        
        # Boost products based on customer preferences
        for product in products:
            boost_score = 0
            
            if customer_preferences:
                # Category preference boost
                preferred_categories = customer_preferences.get('categories', [])
                if product['category'] in preferred_categories:
                    boost_score += 0.2
                
                # Brand preference boost
                preferred_brands = customer_preferences.get('brands', [])
                if product['brand'] in preferred_brands:
                    boost_score += 0.15
            
            if purchase_history:
                # Purchase history boost
                purchased_categories = [item.get('category') for item in purchase_history]
                if product['category'] in purchased_categories:
                    boost_score += 0.1
            
            product['relevance_score'] = product.get('relevance_score', 0) + boost_score
        
        # Re-sort by updated relevance score
        products.sort(key=lambda x: x['relevance_score'], reverse=True)
        return products

    def _generate_recommendation_reason(self, product: Dict, customer_preferences: Dict, purchase_history: List) -> str:
        """Generate explanation for why product is recommended"""
        reasons = []
        
        if customer_preferences:
            preferred_categories = customer_preferences.get('categories', [])
            if product['category'] in preferred_categories:
                reasons.append(f"matches your interest in {product['category']}")
            
            preferred_brands = customer_preferences.get('brands', [])
            if product['brand'] in preferred_brands:
                reasons.append(f"from your preferred brand {product['brand']}")
        
        if purchase_history:
            purchased_categories = [item.get('category') for item in purchase_history]
            if product['category'] in purchased_categories:
                reasons.append(f"similar to your previous {product['category']} purchases")
        
        if not reasons:
            reasons.append("highly rated by other customers")
        
        return f"Recommended because it {' and '.join(reasons)}"

    def _extract_category_hints(self, query: str) -> List[str]:
        """Extract category hints from search query"""
        category_keywords = {
            'electronics': ['phone', 'laptop', 'computer', 'tablet', 'headphones', 'speaker'],
            'clothing': ['shirt', 'pants', 'dress', 'shoes', 'jacket', 'wear'],
            'home': ['furniture', 'decor', 'kitchen', 'bedroom', 'living'],
            'sports': ['fitness', 'exercise', 'outdoor', 'sports', 'athletic'],
            'books': ['book', 'novel', 'read', 'literature', 'author']
        }
        
        query_lower = query.lower()
        hints = []
        
        for category, keywords in category_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                hints.append(category)
        
        return hints

    def _find_complementary_products(self, item: Dict) -> List[Dict]:
        """Find products that complement the given item"""
        # Mock complementary product logic
        complementary_rules = {
            'Electronics': ['Accessories', 'Electronics'],
            'Clothing': ['Accessories', 'Clothing'],
            'Home': ['Home', 'Kitchen'],
            'Sports': ['Sports', 'Fitness']
        }
        
        item_category = item.get('category', '')
        complementary_categories = complementary_rules.get(item_category, [])
        
        complementary_products = [
            p for p in self.product_catalog 
            if p['category'] in complementary_categories 
            and p['id'] != item['id']
            and p['price'] <= item['price'] * 0.5  # Complementary items typically cheaper
        ]
        
        return complementary_products[:3]

    def _generate_upsell_reason(self, base_product: Dict, upsell_product: Dict) -> str:
        """Generate reason for upselling"""
        price_diff = upsell_product['price'] - base_product['price']
        price_increase_percent = (price_diff / base_product['price']) * 100
        
        if price_increase_percent <= 25:
            return f"For just ${price_diff:.2f} more, get enhanced features and better quality"
        elif price_increase_percent <= 50:
            return f"Premium upgrade with significant improvements for ${price_diff:.2f} more"
        else:
            return f"Professional-grade option with advanced features"

    def _get_fallback_recommendations(self) -> List[Dict]:
        """Get fallback recommendations when other methods fail"""
        return self.product_catalog[:5]  # Return first 5 products as fallback

    def _load_product_catalog(self) -> List[Dict]:
        """Load mock product catalog"""
        return [
            {
                'id': 'PROD001',
                'name': 'Wireless Bluetooth Headphones',
                'description': 'Premium noise-canceling wireless headphones with 30-hour battery life',
                'category': 'Electronics',
                'brand': 'AudioTech',
                'price': 199.99,
                'rating': 4.5,
                'popularity_score': 95,
                'features': ['Noise Canceling', 'Wireless', 'Long Battery'],
                'image_url': '/images/headphones.jpg'
            },
            {
                'id': 'PROD002',
                'name': 'Smart Fitness Watch',
                'description': 'Advanced fitness tracking with heart rate monitor and GPS',
                'category': 'Electronics',
                'brand': 'FitTech',
                'price': 299.99,
                'rating': 4.3,
                'popularity_score': 88,
                'features': ['Heart Rate Monitor', 'GPS', 'Waterproof'],
                'image_url': '/images/fitness-watch.jpg'
            },
            {
                'id': 'PROD003',
                'name': 'Organic Cotton T-Shirt',
                'description': 'Comfortable organic cotton t-shirt in various colors',
                'category': 'Clothing',
                'brand': 'EcoWear',
                'price': 29.99,
                'rating': 4.2,
                'popularity_score': 76,
                'features': ['Organic Cotton', 'Comfortable Fit', 'Multiple Colors'],
                'image_url': '/images/tshirt.jpg'
            },
            {
                'id': 'PROD004',
                'name': 'Professional Coffee Maker',
                'description': 'Programmable coffee maker with thermal carafe',
                'category': 'Home',
                'brand': 'BrewMaster',
                'price': 149.99,
                'rating': 4.4,
                'popularity_score': 82,
                'features': ['Programmable', 'Thermal Carafe', 'Auto Shut-off'],
                'image_url': '/images/coffee-maker.jpg'
            },
            {
                'id': 'PROD005',
                'name': 'Yoga Mat Premium',
                'description': 'Non-slip yoga mat with extra cushioning',
                'category': 'Sports',
                'brand': 'ZenFit',
                'price': 59.99,
                'rating': 4.6,
                'popularity_score': 71,
                'features': ['Non-slip', 'Extra Cushioning', 'Eco-friendly'],
                'image_url': '/images/yoga-mat.jpg'
            },
            {
                'id': 'PROD006',
                'name': 'Wireless Phone Charger',
                'description': 'Fast wireless charging pad compatible with all Qi devices',
                'category': 'Electronics',
                'brand': 'ChargeTech',
                'price': 39.99,
                'rating': 4.1,
                'popularity_score': 65,
                'features': ['Fast Charging', 'Qi Compatible', 'LED Indicator'],
                'image_url': '/images/wireless-charger.jpg'
            },
            {
                'id': 'PROD007',
                'name': 'Designer Jeans',
                'description': 'Premium denim jeans with perfect fit',
                'category': 'Clothing',
                'brand': 'DenimCraft',
                'price': 89.99,
                'rating': 4.3,
                'popularity_score': 79,
                'features': ['Premium Denim', 'Perfect Fit', 'Multiple Sizes'],
                'image_url': '/images/jeans.jpg'
            },
            {
                'id': 'PROD008',
                'name': 'Smart Home Speaker',
                'description': 'Voice-controlled smart speaker with premium sound',
                'category': 'Electronics',
                'brand': 'SmartHome',
                'price': 129.99,
                'rating': 4.4,
                'popularity_score': 91,
                'features': ['Voice Control', 'Premium Sound', 'Smart Home Integration'],
                'image_url': '/images/smart-speaker.jpg'
            }
        ]
