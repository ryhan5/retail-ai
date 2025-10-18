"""
Mock APIs - Simulates external retail systems and services
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random
import uuid

logger = logging.getLogger(__name__)

class MockRetailAPIs:
    def __init__(self):
        """Initialize Mock APIs with sample data"""
        self.products = self._load_product_catalog()
        self.inventory = self._load_inventory_data()
        self.customers = self._load_customer_data()
        self.orders = {}
        self.analytics_data = self._generate_analytics_data()

    def search_products(self, query: str, filters: Dict = None) -> List[Dict]:
        """Mock product search API"""
        try:
            if not query:
                return self.products[:8]  # Return first 8 products if no query
            
            query_lower = query.lower()
            matching_products = []
            
            for product in self.products:
                # Simple text matching
                searchable_text = f"{product['name']} {product['description']} {product['category']}".lower()
                if query_lower in searchable_text:
                    matching_products.append(product)
            
            # Apply filters if provided
            if filters:
                matching_products = self._apply_filters(matching_products, filters)
            
            return matching_products[:10]  # Return top 10 results
            
        except Exception as e:
            logger.error(f"Product search error: {str(e)}")
            return []

    def check_inventory(self, product_id: str, store_location: str = 'online') -> Dict:
        """Mock inventory check API"""
        try:
            inventory_info = self.inventory.get(product_id, {})
            location_inventory = inventory_info.get(store_location, {})
            
            if not location_inventory:
                return {
                    'product_id': product_id,
                    'location': store_location,
                    'available': False,
                    'stock_count': 0,
                    'status': 'out_of_stock'
                }
            
            stock_count = location_inventory.get('stock', 0)
            
            return {
                'product_id': product_id,
                'location': store_location,
                'available': stock_count > 0,
                'stock_count': stock_count,
                'status': 'in_stock' if stock_count > 0 else 'out_of_stock',
                'last_updated': location_inventory.get('last_updated', datetime.now().isoformat())
            }
            
        except Exception as e:
            logger.error(f"Inventory check error: {str(e)}")
            return {'available': False, 'error': str(e)}

    def get_promotions(self, customer_id: str = None) -> List[Dict]:
        """Mock promotions API"""
        try:
            current_promotions = [
                {
                    'id': 'PROMO001',
                    'title': 'Summer Electronics Sale',
                    'description': '30% off all electronics',
                    'discount_type': 'percentage',
                    'discount_value': 30,
                    'valid_until': '2024-08-31',
                    'applicable_categories': ['Electronics']
                },
                {
                    'id': 'PROMO002',
                    'title': 'Free Shipping Weekend',
                    'description': 'Free shipping on orders over $75',
                    'discount_type': 'shipping',
                    'minimum_order': 75,
                    'valid_until': '2024-02-29'
                },
                {
                    'id': 'PROMO003',
                    'title': 'Buy 2 Get 1 Free',
                    'description': 'Buy 2 clothing items, get 1 free',
                    'discount_type': 'bogo',
                    'applicable_categories': ['Clothing'],
                    'valid_until': '2024-03-15'
                }
            ]
            
            # Personalize promotions based on customer
            if customer_id:
                # Add customer-specific promotions
                current_promotions.append({
                    'id': 'PERSONAL001',
                    'title': 'Just for You: 15% Off',
                    'description': 'Personal discount based on your shopping history',
                    'discount_type': 'percentage',
                    'discount_value': 15,
                    'valid_until': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                    'customer_specific': True
                })
            
            return current_promotions
            
        except Exception as e:
            logger.error(f"Promotions API error: {str(e)}")
            return []

    def create_order(self, order_data: Dict) -> Dict:
        """Mock order creation API"""
        try:
            order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            order = {
                'order_id': order_id,
                'customer_id': order_data.get('customer_id'),
                'items': order_data.get('items', []),
                'subtotal': order_data.get('subtotal', 0),
                'tax': order_data.get('tax', 0),
                'shipping': order_data.get('shipping', 0),
                'total': order_data.get('total', 0),
                'status': 'confirmed',
                'created_at': datetime.now().isoformat(),
                'estimated_delivery': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                'tracking_number': f"TRK{random.randint(100000, 999999)}"
            }
            
            # Store order
            self.orders[order_id] = order
            
            return order
            
        except Exception as e:
            logger.error(f"Order creation error: {str(e)}")
            return {'error': 'Failed to create order'}

    def process_payment(self, payment_data: Dict) -> Dict:
        """Mock payment processing API"""
        try:
            # Simulate payment processing delay
            import time
            time.sleep(0.5)
            
            # Mock payment success (95% success rate)
            if random.random() < 0.95:
                payment_id = str(uuid.uuid4())
                return {
                    'success': True,
                    'payment_id': payment_id,
                    'transaction_id': f"TXN-{random.randint(100000, 999999)}",
                    'amount': payment_data.get('amount', 0),
                    'currency': 'USD',
                    'status': 'completed',
                    'processed_at': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': 'Payment declined',
                    'error_code': 'DECLINED',
                    'message': 'Your payment was declined. Please try a different payment method.'
                }
                
        except Exception as e:
            logger.error(f"Payment processing error: {str(e)}")
            return {'success': False, 'error': 'Payment processing failed'}

    def get_analytics(self) -> Dict:
        """Mock analytics API"""
        return self.analytics_data

    def get_customers(self) -> List[Dict]:
        """Get all customers (for testing)"""
        return list(self.customers.values())
    
    def get_customer_data(self, customer_id: str) -> Dict:
        """Mock customer data API"""
        try:
            # Mock customer data
            mock_customers = {
                'CUST001': {
                    'id': 'CUST001',
                    'name': 'Alice Johnson',
                    'email': 'alice@example.com',
                    'tier': 'gold',
                    'total_orders': 15,
                    'total_spent': 2450.75,
                    'favorite_categories': ['Electronics', 'Home']
                },
                'CUST002': {
                    'id': 'CUST002',
                    'name': 'Bob Smith',
                    'email': 'bob@example.com',
                    'tier': 'silver',
                    'total_orders': 8,
                    'total_spent': 890.50,
                    'favorite_categories': ['Sports', 'Clothing']
                }
            }
            
            return mock_customers.get(customer_id, {})
            
        except Exception as e:
            logger.error(f"Customer data error: {str(e)}")
            return {}

    def _apply_filters(self, products: List[Dict], filters: Dict) -> List[Dict]:
        """Apply search filters to products"""
        filtered_products = products.copy()
        
        # Category filter
        if 'category' in filters:
            filtered_products = [p for p in filtered_products if p['category'] == filters['category']]
        
        # Price range filter
        if 'min_price' in filters:
            filtered_products = [p for p in filtered_products if p['price'] >= filters['min_price']]
        
        if 'max_price' in filters:
            filtered_products = [p for p in filtered_products if p['price'] <= filters['max_price']]
        
        # Brand filter
        if 'brand' in filters:
            filtered_products = [p for p in filtered_products if p['brand'] == filters['brand']]
        
        # Rating filter
        if 'min_rating' in filters:
            filtered_products = [p for p in filtered_products if p['rating'] >= filters['min_rating']]
        
        return filtered_products

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
                'image_url': '/images/headphones.jpg',
                'features': ['Noise Canceling', 'Wireless', 'Long Battery'],
                'in_stock': True
            },
            {
                'id': 'PROD002',
                'name': 'Smart Fitness Watch',
                'description': 'Advanced fitness tracking with heart rate monitor and GPS',
                'category': 'Electronics',
                'brand': 'FitTech',
                'price': 299.99,
                'rating': 4.3,
                'image_url': '/images/fitness-watch.jpg',
                'features': ['Heart Rate Monitor', 'GPS', 'Waterproof'],
                'in_stock': True
            },
            {
                'id': 'PROD003',
                'name': 'Organic Cotton T-Shirt',
                'description': 'Comfortable organic cotton t-shirt in various colors',
                'category': 'Clothing',
                'brand': 'EcoWear',
                'price': 29.99,
                'rating': 4.2,
                'image_url': '/images/tshirt.jpg',
                'features': ['Organic Cotton', 'Comfortable Fit', 'Multiple Colors'],
                'in_stock': True
            },
            {
                'id': 'PROD004',
                'name': 'Professional Coffee Maker',
                'description': 'Programmable coffee maker with thermal carafe',
                'category': 'Home',
                'brand': 'BrewMaster',
                'price': 149.99,
                'rating': 4.4,
                'image_url': '/images/coffee-maker.jpg',
                'features': ['Programmable', 'Thermal Carafe', 'Auto Shut-off'],
                'in_stock': True
            },
            {
                'id': 'PROD005',
                'name': 'Yoga Mat Premium',
                'description': 'Non-slip yoga mat with extra cushioning',
                'category': 'Sports',
                'brand': 'ZenFit',
                'price': 59.99,
                'rating': 4.6,
                'image_url': '/images/yoga-mat.jpg',
                'features': ['Non-slip', 'Extra Cushioning', 'Eco-friendly'],
                'in_stock': True
            },
            {
                'id': 'PROD006',
                'name': 'Wireless Phone Charger',
                'description': 'Fast wireless charging pad compatible with all Qi devices',
                'category': 'Electronics',
                'brand': 'ChargeTech',
                'price': 39.99,
                'rating': 4.1,
                'image_url': '/images/wireless-charger.jpg',
                'features': ['Fast Charging', 'Qi Compatible', 'LED Indicator'],
                'in_stock': False
            },
            {
                'id': 'PROD007',
                'name': 'Designer Jeans',
                'description': 'Premium denim jeans with perfect fit',
                'category': 'Clothing',
                'brand': 'DenimCraft',
                'price': 89.99,
                'rating': 4.3,
                'image_url': '/images/jeans.jpg',
                'features': ['Premium Denim', 'Perfect Fit', 'Multiple Sizes'],
                'in_stock': True
            },
            {
                'id': 'PROD008',
                'name': 'Smart Home Speaker',
                'description': 'Voice-controlled smart speaker with premium sound',
                'category': 'Electronics',
                'brand': 'SmartHome',
                'price': 129.99,
                'rating': 4.4,
                'image_url': '/images/smart-speaker.jpg',
                'features': ['Voice Control', 'Premium Sound', 'Smart Home Integration'],
                'in_stock': True
            }
        ]

    def _load_inventory_data(self) -> Dict:
        """Load mock inventory data"""
        return {
            'PROD001': {
                'online': {'stock': 25, 'last_updated': '2024-01-15T10:30:00'},
                'downtown': {'stock': 8, 'last_updated': '2024-01-15T09:00:00'},
                'mall': {'stock': 12, 'last_updated': '2024-01-15T09:00:00'}
            },
            'PROD002': {
                'online': {'stock': 15, 'last_updated': '2024-01-15T10:30:00'},
                'downtown': {'stock': 3, 'last_updated': '2024-01-15T09:00:00'},
                'mall': {'stock': 7, 'last_updated': '2024-01-15T09:00:00'}
            },
            'PROD003': {
                'online': {'stock': 50, 'last_updated': '2024-01-15T10:30:00'},
                'downtown': {'stock': 20, 'last_updated': '2024-01-15T09:00:00'},
                'mall': {'stock': 30, 'last_updated': '2024-01-15T09:00:00'}
            },
            'PROD004': {
                'online': {'stock': 18, 'last_updated': '2024-01-15T10:30:00'},
                'downtown': {'stock': 5, 'last_updated': '2024-01-15T09:00:00'},
                'mall': {'stock': 8, 'last_updated': '2024-01-15T09:00:00'}
            },
            'PROD005': {
                'online': {'stock': 35, 'last_updated': '2024-01-15T10:30:00'},
                'downtown': {'stock': 12, 'last_updated': '2024-01-15T09:00:00'},
                'mall': {'stock': 18, 'last_updated': '2024-01-15T09:00:00'}
            },
            'PROD006': {
                'online': {'stock': 0, 'last_updated': '2024-01-15T10:30:00'},
                'downtown': {'stock': 2, 'last_updated': '2024-01-15T09:00:00'},
                'mall': {'stock': 0, 'last_updated': '2024-01-15T09:00:00'}
            },
            'PROD007': {
                'online': {'stock': 40, 'last_updated': '2024-01-15T10:30:00'},
                'downtown': {'stock': 15, 'last_updated': '2024-01-15T09:00:00'},
                'mall': {'stock': 22, 'last_updated': '2024-01-15T09:00:00'}
            },
            'PROD008': {
                'online': {'stock': 22, 'last_updated': '2024-01-15T10:30:00'},
                'downtown': {'stock': 6, 'last_updated': '2024-01-15T09:00:00'},
                'mall': {'stock': 10, 'last_updated': '2024-01-15T09:00:00'}
            }
        }

    def _generate_analytics_data(self) -> Dict:
        """Generate mock analytics data"""
        return {
            'daily_stats': {
                'total_conversations': 156,
                'successful_conversions': 23,
                'conversion_rate': 14.7,
                'average_order_value': 187.50,
                'total_revenue': 4312.50
            },
            'channel_performance': {
                'web': {'conversations': 89, 'conversions': 15, 'conversion_rate': 16.9},
                'mobile': {'conversations': 45, 'conversions': 6, 'conversion_rate': 13.3},
                'whatsapp': {'conversations': 22, 'conversions': 2, 'conversion_rate': 9.1}
            },
            'popular_products': [
                {'id': 'PROD001', 'name': 'Wireless Headphones', 'views': 234, 'purchases': 12},
                {'id': 'PROD008', 'name': 'Smart Speaker', 'views': 189, 'purchases': 8},
                {'id': 'PROD002', 'name': 'Fitness Watch', 'views': 167, 'purchases': 7}
            ],
            'customer_satisfaction': {
                'average_rating': 4.3,
                'total_reviews': 89,
                'positive_feedback_rate': 87.6
            }
        }
    
    def _load_customer_data(self) -> Dict:
        """Load mock customer data (≥10 customers as required)"""
        customers = {}
        
        # Customer profiles with demographics, purchase history, loyalty tier
        customer_data = [
            {'name': 'Alice Johnson', 'email': 'alice@example.com', 'tier': 'gold', 'points': 2500},
            {'name': 'Bob Smith', 'email': 'bob@example.com', 'tier': 'silver', 'points': 1200},
            {'name': 'Carol Williams', 'email': 'carol@example.com', 'tier': 'platinum', 'points': 5500},
            {'name': 'David Brown', 'email': 'david@example.com', 'tier': 'bronze', 'points': 300},
            {'name': 'Emma Davis', 'email': 'emma@example.com', 'tier': 'gold', 'points': 2800},
            {'name': 'Frank Miller', 'email': 'frank@example.com', 'tier': 'silver', 'points': 900},
            {'name': 'Grace Wilson', 'email': 'grace@example.com', 'tier': 'platinum', 'points': 6200},
            {'name': 'Henry Moore', 'email': 'henry@example.com', 'tier': 'bronze', 'points': 150},
            {'name': 'Isabel Taylor', 'email': 'isabel@example.com', 'tier': 'gold', 'points': 3100},
            {'name': 'Jack Anderson', 'email': 'jack@example.com', 'tier': 'silver', 'points': 1500},
            {'name': 'Karen Thomas', 'email': 'karen@example.com', 'tier': 'bronze', 'points': 450},
            {'name': 'Liam Jackson', 'email': 'liam@example.com', 'tier': 'gold', 'points': 2200}
        ]
        
        for i, data in enumerate(customer_data, 1):
            cust_id = f'CUST{i:03d}'
            customers[cust_id] = {
                'id': cust_id,
                'name': data['name'],
                'email': data['email'],
                'tier': data['tier'],
                'points': data['points'],
                'join_date': f'2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}',
                'total_orders': random.randint(1, 50),
                'total_spent': round(random.uniform(100, 5000), 2),
                'device_preferences': random.choice(['mobile', 'web', 'app']),
                'purchase_history': [
                    {
                        'product': random.choice(['Laptop', 'Headphones', 'Watch', 'Shirt', 'Shoes']),
                        'category': random.choice(['Electronics', 'Clothing', 'Footwear', 'Accessories']),
                        'total': round(random.uniform(50, 500), 2),
                        'date': f'2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
                    }
                    for _ in range(random.randint(1, 5))
                ]
            }
        
        return customers
