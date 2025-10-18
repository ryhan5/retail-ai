"""
Inventory Agent - Handles stock checks, availability, and store locations
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class InventoryAgent:
    def __init__(self):
        """Initialize Inventory Agent with mock inventory data"""
        self.inventory_data = self._load_mock_inventory()
        self.store_locations = self._load_store_locations()

    def check_availability(self, product_id: str, location: str = 'online') -> Dict:
        """
        Check product availability at specific location
        
        Args:
            product_id: Product identifier
            location: Store location or 'online'
            
        Returns:
            Dict with availability status and stock information
        """
        try:
            if location == 'online':
                inventory = self.inventory_data.get(product_id, {}).get('online', {})
            else:
                inventory = self.inventory_data.get(product_id, {}).get('stores', {}).get(location, {})
            
            if not inventory:
                return {
                    'available': False,
                    'stock_level': 'Out of stock',
                    'location': location,
                    'last_updated': datetime.now().isoformat()
                }
            
            stock_count = inventory.get('stock', 0)
            
            if stock_count > 10:
                stock_level = 'In stock'
            elif stock_count > 0:
                stock_level = f'Limited stock ({stock_count} left)'
            else:
                stock_level = 'Out of stock'
            
            return {
                'available': stock_count > 0,
                'stock_level': stock_level,
                'stock_count': stock_count,
                'location': location,
                'last_updated': inventory.get('last_updated', datetime.now().isoformat()),
                'estimated_restock': inventory.get('estimated_restock'),
                'can_backorder': inventory.get('can_backorder', False)
            }
            
        except Exception as e:
            logger.error(f"Error checking availability for {product_id}: {str(e)}")
            return {
                'available': False,
                'stock_level': 'Unable to check stock',
                'error': str(e)
            }

    def check_other_locations(self, product_id: str) -> List[str]:
        """
        Check availability at other store locations
        
        Args:
            product_id: Product identifier
            
        Returns:
            List of store locations where product is available
        """
        try:
            available_locations = []
            product_inventory = self.inventory_data.get(product_id, {})
            
            for location, inventory in product_inventory.get('stores', {}).items():
                if inventory.get('stock', 0) > 0:
                    available_locations.append(location)
            
            return available_locations
            
        except Exception as e:
            logger.error(f"Error checking other locations for {product_id}: {str(e)}")
            return []

    def reserve_product(self, product_id: str, location: str, customer_id: str, quantity: int = 1) -> Dict:
        """
        Reserve product for customer pickup
        
        Args:
            product_id: Product identifier
            location: Store location
            customer_id: Customer identifier
            quantity: Quantity to reserve
            
        Returns:
            Dict with reservation details
        """
        try:
            availability = self.check_availability(product_id, location)
            
            if not availability['available'] or availability['stock_count'] < quantity:
                return {
                    'success': False,
                    'message': 'Insufficient stock for reservation',
                    'available_quantity': availability.get('stock_count', 0)
                }
            
            # Generate reservation ID
            reservation_id = f"RES-{datetime.now().strftime('%Y%m%d%H%M%S')}-{customer_id[:6]}"
            
            # Calculate hold expiry (24 hours from now)
            hold_until = (datetime.now() + timedelta(hours=24)).isoformat()
            
            # In real implementation, this would update the database
            reservation = {
                'reservation_id': reservation_id,
                'product_id': product_id,
                'customer_id': customer_id,
                'location': location,
                'quantity': quantity,
                'hold_until': hold_until,
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'reservation': reservation,
                'message': f'Product reserved until {hold_until[:16]} at {location} store'
            }
            
        except Exception as e:
            logger.error(f"Error reserving product {product_id}: {str(e)}")
            return {
                'success': False,
                'message': 'Failed to create reservation',
                'error': str(e)
            }

    def get_low_stock_alerts(self, threshold: int = 5) -> List[Dict]:
        """
        Get products with low stock levels
        
        Args:
            threshold: Stock level threshold for alerts
            
        Returns:
            List of products with low stock
        """
        try:
            low_stock_products = []
            
            for product_id, inventory in self.inventory_data.items():
                # Check online stock
                online_stock = inventory.get('online', {}).get('stock', 0)
                if 0 < online_stock <= threshold:
                    low_stock_products.append({
                        'product_id': product_id,
                        'location': 'online',
                        'stock_count': online_stock,
                        'alert_level': 'low' if online_stock > 2 else 'critical'
                    })
                
                # Check store stock
                for location, store_inventory in inventory.get('stores', {}).items():
                    store_stock = store_inventory.get('stock', 0)
                    if 0 < store_stock <= threshold:
                        low_stock_products.append({
                            'product_id': product_id,
                            'location': location,
                            'stock_count': store_stock,
                            'alert_level': 'low' if store_stock > 2 else 'critical'
                        })
            
            return low_stock_products
            
        except Exception as e:
            logger.error(f"Error getting low stock alerts: {str(e)}")
            return []

    def get_store_locations(self) -> List[Dict]:
        """Get all store locations with details"""
        return self.store_locations

    def find_nearest_store(self, customer_location: str) -> Dict:
        """
        Find nearest store to customer location
        
        Args:
            customer_location: Customer's location (city, zip, etc.)
            
        Returns:
            Dict with nearest store information
        """
        try:
            # In real implementation, this would use geolocation services
            # For now, return a mock nearest store
            return {
                'store_id': 'STORE001',
                'name': 'Downtown Store',
                'address': '123 Main St, Downtown',
                'distance': '2.3 miles',
                'phone': '(555) 123-4567',
                'hours': 'Mon-Sat: 9AM-9PM, Sun: 10AM-7PM',
                'services': ['Pickup', 'Returns', 'Customer Service']
            }
            
        except Exception as e:
            logger.error(f"Error finding nearest store: {str(e)}")
            return {}

    def _load_mock_inventory(self) -> Dict:
        """Load mock inventory data"""
        return {
            'PROD001': {
                'online': {
                    'stock': 25,
                    'last_updated': '2024-01-15T10:30:00',
                    'can_backorder': True,
                    'estimated_restock': '2024-01-20'
                },
                'stores': {
                    'downtown': {'stock': 8, 'last_updated': '2024-01-15T09:00:00'},
                    'mall': {'stock': 12, 'last_updated': '2024-01-15T09:00:00'},
                    'outlet': {'stock': 3, 'last_updated': '2024-01-15T09:00:00'}
                }
            },
            'PROD002': {
                'online': {
                    'stock': 0,
                    'last_updated': '2024-01-15T10:30:00',
                    'can_backorder': True,
                    'estimated_restock': '2024-01-25'
                },
                'stores': {
                    'downtown': {'stock': 2, 'last_updated': '2024-01-15T09:00:00'},
                    'mall': {'stock': 0, 'last_updated': '2024-01-15T09:00:00'},
                    'outlet': {'stock': 1, 'last_updated': '2024-01-15T09:00:00'}
                }
            },
            'PROD003': {
                'online': {
                    'stock': 50,
                    'last_updated': '2024-01-15T10:30:00',
                    'can_backorder': False
                },
                'stores': {
                    'downtown': {'stock': 15, 'last_updated': '2024-01-15T09:00:00'},
                    'mall': {'stock': 20, 'last_updated': '2024-01-15T09:00:00'},
                    'outlet': {'stock': 8, 'last_updated': '2024-01-15T09:00:00'}
                }
            }
        }

    def _load_store_locations(self) -> List[Dict]:
        """Load store location data"""
        return [
            {
                'store_id': 'STORE001',
                'name': 'Downtown Store',
                'address': '123 Main St, Downtown, NY 10001',
                'phone': '(555) 123-4567',
                'hours': 'Mon-Sat: 9AM-9PM, Sun: 10AM-7PM',
                'services': ['Pickup', 'Returns', 'Customer Service', 'Personal Shopping'],
                'coordinates': {'lat': 40.7128, 'lng': -74.0060}
            },
            {
                'store_id': 'STORE002',
                'name': 'Mall Location',
                'address': '456 Shopping Center Dr, Mall Plaza, NY 10002',
                'phone': '(555) 234-5678',
                'hours': 'Mon-Sat: 10AM-10PM, Sun: 11AM-8PM',
                'services': ['Pickup', 'Returns', 'Customer Service'],
                'coordinates': {'lat': 40.7589, 'lng': -73.9851}
            },
            {
                'store_id': 'STORE003',
                'name': 'Outlet Store',
                'address': '789 Outlet Blvd, Outlet Center, NY 10003',
                'phone': '(555) 345-6789',
                'hours': 'Mon-Sat: 9AM-8PM, Sun: 10AM-6PM',
                'services': ['Pickup', 'Returns', 'Clearance Items'],
                'coordinates': {'lat': 40.6892, 'lng': -74.0445}
            }
        ]
