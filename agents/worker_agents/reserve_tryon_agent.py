"""
Reserve & Try-On Agent
Handles in-store reservations, try-on appointments, and BOPIS (Buy Online, Pick up In-Store)
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ReserveTryOnAgent:
    """
    Manages product reservations and try-on experiences
    Enables seamless online-to-offline customer journeys
    """
    
    def __init__(self):
        # Mock store locations
        self.store_locations = {
            'STORE001': {
                'name': 'Downtown Flagship',
                'address': '123 Main St, Downtown',
                'hours': '9 AM - 9 PM',
                'distance': '2.5 miles',
                'has_fitting_rooms': True,
                'has_personal_shopper': True,
                'available_slots': self._generate_time_slots()
            },
            'STORE002': {
                'name': 'Mall Location',
                'address': '456 Shopping Mall, Suite 200',
                'hours': '10 AM - 8 PM',
                'distance': '5.1 miles',
                'has_fitting_rooms': True,
                'has_personal_shopper': False,
                'available_slots': self._generate_time_slots()
            },
            'STORE003': {
                'name': 'Outlet Store',
                'address': '789 Outlet Blvd',
                'hours': '10 AM - 7 PM',
                'distance': '12.3 miles',
                'has_fitting_rooms': False,
                'has_personal_shopper': False,
                'available_slots': self._generate_time_slots()
            }
        }
        
        # Mock reservations database
        self.reservations = {}
    
    def reserve_for_tryon(self, product_id: str, customer_id: str, 
                         store_id: str, time_slot: str = None) -> Dict:
        """
        Reserve a product for in-store try-on
        """
        store = self.store_locations.get(store_id)
        
        if not store:
            return {
                'success': False,
                'message': 'Store not found. Please select a valid store location.'
            }
        
        if not store['has_fitting_rooms']:
            return {
                'success': False,
                'message': f"{store['name']} doesn't have fitting rooms. "
                          f"Would you like to reserve at a different location?",
                'alternative_stores': self._get_stores_with_fitting_rooms()
            }
        
        # Check product availability at store
        availability = self._check_store_inventory(product_id, store_id)
        
        if not availability['available']:
            return {
                'success': False,
                'message': f"This item isn't currently available at {store['name']}. "
                          f"I can check other locations or reserve it for delivery to the store.",
                'options': [
                    {
                        'action': 'check_other_stores',
                        'label': 'Check other stores',
                        'description': 'Find nearby stores with this item'
                    },
                    {
                        'action': 'ship_to_store',
                        'label': 'Ship to store',
                        'description': 'Free delivery to store in 2-3 days'
                    },
                    {
                        'action': 'home_delivery',
                        'label': 'Ship to home',
                        'description': 'Try at home with free returns'
                    }
                ]
            }
        
        # Select time slot
        if not time_slot:
            time_slot = store['available_slots'][0] if store['available_slots'] else 'Next available'
        
        # Create reservation
        reservation_id = f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}"
        reservation = {
            'reservation_id': reservation_id,
            'product_id': product_id,
            'customer_id': customer_id,
            'store_id': store_id,
            'store_name': store['name'],
            'time_slot': time_slot,
            'status': 'confirmed',
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
            'type': 'try_on'
        }
        
        self.reservations[reservation_id] = reservation
        
        # Generate confirmation message
        message = f"✅ **Reservation Confirmed!**\n\n"
        message += f"📍 **Store**: {store['name']}\n"
        message += f"📅 **Time**: {time_slot}\n"
        message += f"🎫 **Reservation ID**: {reservation_id}\n\n"
        message += f"**What to expect:**\n"
        message += f"• Your item will be ready in a fitting room\n"
        message += f"• Reservation held for 24 hours\n"
        
        if store['has_personal_shopper']:
            message += f"• Personal shopper available to assist\n"
        
        message += f"\n📍 **Directions**: {store['address']}\n"
        message += f"🕐 **Store Hours**: {store['hours']}\n\n"
        message += f"We'll send you a reminder 2 hours before your appointment!"
        
        return {
            'success': True,
            'message': message,
            'reservation': reservation,
            'store': store,
            'suggestions': [
                'Add to calendar',
                'Get directions',
                'Reserve more items',
                'Modify reservation'
            ],
            'quick_actions': [
                {
                    'action': 'add_calendar',
                    'label': 'Add to Calendar',
                    'data': reservation
                },
                {
                    'action': 'get_directions',
                    'label': 'Get Directions',
                    'data': {'address': store['address']}
                },
                {
                    'action': 'call_store',
                    'label': 'Call Store',
                    'data': {'phone': '(555) 123-4567'}
                }
            ]
        }
    
    def buy_online_pickup_instore(self, cart_items: List[Dict], customer_id: str,
                                  store_id: str, pickup_time: str = None) -> Dict:
        """
        Process BOPIS (Buy Online, Pick up In-Store) order
        """
        store = self.store_locations.get(store_id)
        
        if not store:
            return {
                'success': False,
                'message': 'Store not found. Please select a valid store location.'
            }
        
        # Check all items availability
        unavailable_items = []
        for item in cart_items:
            availability = self._check_store_inventory(item['id'], store_id)
            if not availability['available']:
                unavailable_items.append(item['name'])
        
        if unavailable_items:
            return {
                'success': False,
                'message': f"Some items aren't available at {store['name']}:\n" + 
                          "\n".join(f"• {item}" for item in unavailable_items),
                'options': [
                    {
                        'action': 'split_order',
                        'label': 'Split order',
                        'description': 'Pick up available items, ship the rest'
                    },
                    {
                        'action': 'different_store',
                        'label': 'Try different store',
                        'description': 'Find a store with all items'
                    },
                    {
                        'action': 'ship_all',
                        'label': 'Ship everything',
                        'description': 'Free home delivery'
                    }
                ]
            }
        
        # Calculate totals
        subtotal = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart_items)
        tax = subtotal * 0.08  # 8% tax
        total = subtotal + tax
        
        # Create BOPIS order
        order_id = f"BOPIS{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Estimate ready time
        ready_time = datetime.now() + timedelta(hours=2)
        if pickup_time:
            ready_time = datetime.fromisoformat(pickup_time)
        
        order = {
            'order_id': order_id,
            'type': 'BOPIS',
            'customer_id': customer_id,
            'store_id': store_id,
            'items': cart_items,
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
            'status': 'processing',
            'ready_time': ready_time.isoformat(),
            'pickup_deadline': (ready_time + timedelta(days=3)).isoformat(),
            'created_at': datetime.now().isoformat()
        }
        
        message = f"🎉 **Order Confirmed - Ready for Pickup!**\n\n"
        message += f"📦 **Order**: #{order_id}\n"
        message += f"📍 **Pickup Location**: {store['name']}\n"
        message += f"⏰ **Ready By**: {ready_time.strftime('%I:%M %p today')}\n"
        message += f"💰 **Total**: ${total:.2f}\n\n"
        
        message += f"**Your items** ({len(cart_items)}):\n"
        for item in cart_items:
            message += f"• {item['name']} x{item.get('quantity', 1)}\n"
        
        message += f"\n**Pickup Instructions:**\n"
        message += f"1. Bring your order confirmation (#{order_id})\n"
        message += f"2. Valid ID required\n"
        message += f"3. Go to pickup counter\n"
        message += f"4. Items held for 3 days\n\n"
        
        message += f"📍 {store['address']}\n"
        message += f"🕐 {store['hours']}\n\n"
        
        message += f"We'll text you when your order is ready!"
        
        return {
            'success': True,
            'message': message,
            'order': order,
            'store': store,
            'suggestions': [
                'Get directions',
                'Add to calendar',
                'View order details',
                'Modify pickup time'
            ],
            'quick_actions': [
                {
                    'action': 'track_order',
                    'label': 'Track Order',
                    'data': {'order_id': order_id}
                },
                {
                    'action': 'get_directions',
                    'label': 'Get Directions',
                    'data': {'address': store['address']}
                },
                {
                    'action': 'change_pickup_time',
                    'label': 'Change Pickup Time',
                    'data': {'order_id': order_id}
                }
            ]
        }
    
    def schedule_personal_shopping(self, customer_id: str, store_id: str,
                                   preferred_time: str, occasion: str = None) -> Dict:
        """
        Schedule a personal shopping appointment
        """
        store = self.store_locations.get(store_id)
        
        if not store:
            return {
                'success': False,
                'message': 'Store not found.'
            }
        
        if not store['has_personal_shopper']:
            return {
                'success': False,
                'message': f"{store['name']} doesn't offer personal shopping services. "
                          f"Try our Downtown Flagship location!",
                'alternative_stores': self._get_stores_with_personal_shopper()
            }
        
        # Create appointment
        appointment_id = f"APPT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        appointment = {
            'appointment_id': appointment_id,
            'customer_id': customer_id,
            'store_id': store_id,
            'type': 'personal_shopping',
            'scheduled_time': preferred_time,
            'occasion': occasion,
            'duration': '60 minutes',
            'status': 'confirmed',
            'stylist': 'Sarah Johnson',  # Mock stylist
            'created_at': datetime.now().isoformat()
        }
        
        message = f"✨ **Personal Shopping Appointment Booked!**\n\n"
        message += f"👗 **Stylist**: Sarah Johnson\n"
        message += f"📅 **Date & Time**: {preferred_time}\n"
        message += f"⏱️ **Duration**: 60 minutes\n"
        message += f"📍 **Location**: {store['name']}\n"
        message += f"🎫 **Appointment ID**: {appointment_id}\n\n"
        
        if occasion:
            message += f"**Shopping For**: {occasion}\n\n"
        
        message += f"**What's Included:**\n"
        message += f"• One-on-one styling session\n"
        message += f"• Personalized outfit curation\n"
        message += f"• Private fitting room\n"
        message += f"• Complimentary refreshments\n"
        message += f"• Expert fashion advice\n\n"
        
        message += f"**Prepare for Your Visit:**\n"
        message += f"• Bring inspiration photos\n"
        message += f"• Share your style preferences\n"
        message += f"• Set your budget range\n\n"
        
        message += f"Looking forward to styling you! 💫"
        
        return {
            'success': True,
            'message': message,
            'appointment': appointment,
            'suggestions': [
                'Add to calendar',
                'Share preferences',
                'Get directions',
                'Reschedule'
            ]
        }
    
    def get_nearby_stores(self, customer_location: str = None, 
                         product_id: str = None) -> Dict:
        """
        Find nearby stores, optionally filtering by product availability
        """
        stores = []
        
        for store_id, store in self.store_locations.items():
            store_info = {
                'store_id': store_id,
                'name': store['name'],
                'address': store['address'],
                'distance': store['distance'],
                'hours': store['hours'],
                'features': []
            }
            
            if store['has_fitting_rooms']:
                store_info['features'].append('Fitting Rooms')
            if store['has_personal_shopper']:
                store_info['features'].append('Personal Shopper')
            
            # Check product availability if specified
            if product_id:
                availability = self._check_store_inventory(product_id, store_id)
                store_info['has_product'] = availability['available']
                store_info['stock_level'] = availability.get('stock_level', 0)
            
            stores.append(store_info)
        
        # Sort by distance
        stores.sort(key=lambda x: float(x['distance'].split()[0]))
        
        message = "📍 **Nearby Stores**\n\n"
        
        for i, store in enumerate(stores, 1):
            message += f"{i}. **{store['name']}**\n"
            message += f"   📍 {store['distance']} away\n"
            message += f"   🕐 {store['hours']}\n"
            
            if store['features']:
                message += f"   ✨ {', '.join(store['features'])}\n"
            
            if product_id and 'has_product' in store:
                if store['has_product']:
                    message += f"   ✅ In stock ({store['stock_level']} available)\n"
                else:
                    message += f"   ❌ Out of stock\n"
            
            message += "\n"
        
        return {
            'success': True,
            'message': message,
            'stores': stores,
            'suggestions': [
                'Reserve at nearest store',
                'Schedule try-on',
                'Get directions',
                'Call store'
            ]
        }
    
    # Private helper methods
    def _generate_time_slots(self) -> List[str]:
        """Generate available time slots for today"""
        slots = []
        now = datetime.now()
        
        # Generate slots from current time + 2 hours
        start_time = now + timedelta(hours=2)
        start_time = start_time.replace(minute=0, second=0, microsecond=0)
        
        for i in range(8):  # 8 time slots
            slot_time = start_time + timedelta(hours=i)
            if 9 <= slot_time.hour <= 20:  # Store hours
                slots.append(slot_time.strftime('%I:%M %p'))
        
        return slots
    
    def _check_store_inventory(self, product_id: str, store_id: str) -> Dict:
        """Check if product is available at specific store"""
        # Mock implementation - in production, check real inventory
        import random
        available = random.choice([True, True, True, False])  # 75% available
        
        return {
            'available': available,
            'stock_level': random.randint(1, 10) if available else 0,
            'store_id': store_id
        }
    
    def _get_stores_with_fitting_rooms(self) -> List[Dict]:
        """Get stores that have fitting rooms"""
        return [
            {'store_id': sid, 'name': store['name'], 'distance': store['distance']}
            for sid, store in self.store_locations.items()
            if store['has_fitting_rooms']
        ]
    
    def _get_stores_with_personal_shopper(self) -> List[Dict]:
        """Get stores that offer personal shopping"""
        return [
            {'store_id': sid, 'name': store['name'], 'distance': store['distance']}
            for sid, store in self.store_locations.items()
            if store['has_personal_shopper']
        ]
