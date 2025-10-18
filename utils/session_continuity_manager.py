"""
Session Continuity Manager
Maintains session state and context when customers move between channels
(e.g., web chat → WhatsApp → in-store kiosk)
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class SessionContinuityManager:
    """
    Manages cross-channel session continuity
    Ensures customers can seamlessly transition between channels without losing context
    """
    
    def __init__(self):
        # In-memory storage (in production, use Redis or database)
        self.sessions = {}
        self.customer_sessions = {}  # Map customer_id to session_id
        self.session_timeout = timedelta(hours=24)
    
    def create_session(self, customer_id: str, channel: str, initial_context: Dict = None) -> str:
        """Create a new session or retrieve existing one"""
        session_id = self._get_or_create_session_id(customer_id)
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'session_id': session_id,
                'customer_id': customer_id,
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'channels_used': [channel],
                'current_channel': channel,
                'context': initial_context or {},
                'conversation_history': [],
                'cart': [],
                'current_step': 'greeting',
                'intent_history': [],
                'channel_transitions': []
            }
        else:
            # Update existing session with new channel
            self._transition_channel(session_id, channel)
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve session data"""
        session = self.sessions.get(session_id)
        
        if session:
            # Check if session has expired
            last_updated = datetime.fromisoformat(session['last_updated'])
            if datetime.now() - last_updated > self.session_timeout:
                logger.info(f"Session {session_id} has expired")
                return None
            
            # Update last accessed time
            session['last_updated'] = datetime.now().isoformat()
            return session
        
        return None
    
    def update_session(self, session_id: str, updates: Dict) -> bool:
        """Update session data"""
        if session_id not in self.sessions:
            logger.warning(f"Session {session_id} not found")
            return False
        
        session = self.sessions[session_id]
        
        # Update specific fields
        if 'cart' in updates:
            session['cart'] = updates['cart']
        
        if 'context' in updates:
            session['context'].update(updates['context'])
        
        if 'conversation_history' in updates:
            session['conversation_history'].extend(updates['conversation_history'])
        
        if 'current_step' in updates:
            session['current_step'] = updates['current_step']
        
        if 'intent_history' in updates:
            session['intent_history'].append(updates['intent_history'])
        
        session['last_updated'] = datetime.now().isoformat()
        
        return True
    
    def transition_channel(self, session_id: str, from_channel: str, to_channel: str, 
                          transition_context: Dict = None) -> Dict:
        """
        Handle channel transition with context preservation
        Returns a transition summary for the customer
        """
        session = self.get_session(session_id)
        
        if not session:
            logger.error(f"Cannot transition - session {session_id} not found")
            return {
                'success': False,
                'message': 'Session not found. Please start a new conversation.'
            }
        
        # Record transition
        transition = {
            'from_channel': from_channel,
            'to_channel': to_channel,
            'timestamp': datetime.now().isoformat(),
            'context': transition_context or {}
        }
        
        session['channel_transitions'].append(transition)
        session['current_channel'] = to_channel
        
        if to_channel not in session['channels_used']:
            session['channels_used'].append(to_channel)
        
        session['last_updated'] = datetime.now().isoformat()
        
        # Generate transition message
        transition_message = self._generate_transition_message(session, from_channel, to_channel)
        
        return {
            'success': True,
            'message': transition_message,
            'session': session,
            'cart_items': len(session['cart']),
            'context_preserved': True
        }
    
    def get_session_summary(self, session_id: str) -> Dict:
        """Get a summary of the session for display"""
        session = self.get_session(session_id)
        
        if not session:
            return None
        
        return {
            'session_id': session_id,
            'customer_id': session['customer_id'],
            'current_channel': session['current_channel'],
            'channels_used': session['channels_used'],
            'cart_items': len(session['cart']),
            'cart_total': sum(item.get('price', 0) for item in session['cart']),
            'conversation_length': len(session['conversation_history']),
            'current_step': session['current_step'],
            'session_duration': self._calculate_session_duration(session),
            'last_updated': session['last_updated']
        }
    
    def merge_sessions(self, old_session_id: str, new_session_id: str) -> bool:
        """Merge two sessions (e.g., when anonymous user logs in)"""
        old_session = self.get_session(old_session_id)
        new_session = self.get_session(new_session_id)
        
        if not old_session or not new_session:
            return False
        
        # Merge cart
        new_session['cart'].extend(old_session['cart'])
        
        # Merge conversation history
        new_session['conversation_history'].extend(old_session['conversation_history'])
        
        # Merge context
        new_session['context'].update(old_session['context'])
        
        # Merge channels used
        for channel in old_session['channels_used']:
            if channel not in new_session['channels_used']:
                new_session['channels_used'].append(channel)
        
        # Delete old session
        del self.sessions[old_session_id]
        
        logger.info(f"Merged session {old_session_id} into {new_session_id}")
        return True
    
    def save_cart_for_later(self, session_id: str) -> Dict:
        """Save cart items for later retrieval"""
        session = self.get_session(session_id)
        
        if not session:
            return {'success': False, 'message': 'Session not found'}
        
        if not session['cart']:
            return {'success': False, 'message': 'Cart is empty'}
        
        # In production, save to database
        saved_cart = {
            'customer_id': session['customer_id'],
            'items': session['cart'],
            'saved_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        # Store in context
        session['context']['saved_cart'] = saved_cart
        
        return {
            'success': True,
            'message': f"Saved {len(session['cart'])} items for later",
            'cart': saved_cart
        }
    
    def restore_saved_cart(self, session_id: str) -> Dict:
        """Restore previously saved cart"""
        session = self.get_session(session_id)
        
        if not session:
            return {'success': False, 'message': 'Session not found'}
        
        saved_cart = session['context'].get('saved_cart')
        
        if not saved_cart:
            return {'success': False, 'message': 'No saved cart found'}
        
        # Check if cart has expired
        expires_at = datetime.fromisoformat(saved_cart['expires_at'])
        if datetime.now() > expires_at:
            return {'success': False, 'message': 'Saved cart has expired'}
        
        # Restore items to current cart
        session['cart'] = saved_cart['items']
        
        return {
            'success': True,
            'message': f"Restored {len(saved_cart['items'])} items to your cart",
            'cart': session['cart']
        }
    
    def get_channel_specific_context(self, session_id: str, channel: str) -> Dict:
        """Get context optimized for specific channel"""
        session = self.get_session(session_id)
        
        if not session:
            return {}
        
        # Base context
        context = {
            'cart_items': len(session['cart']),
            'current_step': session['current_step'],
            'customer_id': session['customer_id']
        }
        
        # Channel-specific optimizations
        if channel == 'whatsapp':
            # WhatsApp: Concise messages, emoji-friendly
            context['format'] = 'concise'
            context['use_emojis'] = True
            context['max_message_length'] = 1000
        
        elif channel == 'voice':
            # Voice: Spoken language, no visual elements
            context['format'] = 'spoken'
            context['use_emojis'] = False
            context['avoid_urls'] = True
        
        elif channel == 'instore':
            # In-store kiosk: Large buttons, simple navigation
            context['format'] = 'visual'
            context['large_buttons'] = True
            context['show_images'] = True
        
        elif channel == 'mobile':
            # Mobile: Touch-friendly, vertical layout
            context['format'] = 'mobile_optimized'
            context['touch_friendly'] = True
        
        else:  # web
            # Web: Full features, rich media
            context['format'] = 'full'
            context['rich_media'] = True
        
        return context
    
    # Private helper methods
    def _get_or_create_session_id(self, customer_id: str) -> str:
        """Get existing session ID or create new one"""
        if customer_id in self.customer_sessions:
            return self.customer_sessions[customer_id]
        
        session_id = f"session_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.customer_sessions[customer_id] = session_id
        return session_id
    
    def _transition_channel(self, session_id: str, new_channel: str):
        """Internal method to handle channel transition"""
        session = self.sessions[session_id]
        
        old_channel = session['current_channel']
        session['current_channel'] = new_channel
        
        if new_channel not in session['channels_used']:
            session['channels_used'].append(new_channel)
        
        session['channel_transitions'].append({
            'from': old_channel,
            'to': new_channel,
            'timestamp': datetime.now().isoformat()
        })
    
    def _generate_transition_message(self, session: Dict, from_channel: str, 
                                    to_channel: str) -> str:
        """Generate a friendly message for channel transitions"""
        channel_names = {
            'web': 'web chat',
            'mobile': 'mobile app',
            'whatsapp': 'WhatsApp',
            'telegram': 'Telegram',
            'instore': 'in-store kiosk',
            'voice': 'voice assistant'
        }
        
        from_name = channel_names.get(from_channel, from_channel)
        to_name = channel_names.get(to_channel, to_channel)
        
        cart_count = len(session['cart'])
        
        message = f"Welcome back! I see you were chatting with me on {from_name}. "
        message += f"I've brought everything over to {to_name} for you. "
        
        if cart_count > 0:
            message += f"You have {cart_count} item(s) in your cart. "
        
        message += "Let's continue where we left off! How can I help you?"
        
        return message
    
    def _calculate_session_duration(self, session: Dict) -> str:
        """Calculate how long the session has been active"""
        created = datetime.fromisoformat(session['created_at'])
        duration = datetime.now() - created
        
        if duration.seconds < 60:
            return f"{duration.seconds} seconds"
        elif duration.seconds < 3600:
            return f"{duration.seconds // 60} minutes"
        else:
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            return f"{hours}h {minutes}m"


# Global instance
session_continuity_manager = SessionContinuityManager()
