"""
Sales Psychology Module
Implements consultative selling techniques, persuasive language,
and objection handling for better conversion rates
"""

import logging
import random
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class SalesPsychology:
    """
    Applies proven sales psychology techniques to conversations
    Uses consultative approach, open questions, and graceful objection handling
    """
    
    def __init__(self):
        # Open-ended discovery questions
        self.discovery_questions = {
            'occasion': [
                "What's the occasion you're shopping for?",
                "Is this for a special event or everyday use?",
                "What brings you in today?",
                "Are you shopping for yourself or someone special?"
            ],
            'needs': [
                "What features are most important to you?",
                "What problems are you trying to solve?",
                "What would make this purchase perfect for you?",
                "What are your must-haves?"
            ],
            'budget': [
                "What budget range are you comfortable with?",
                "Are you looking for value, premium, or luxury options?",
                "What price point works best for you?",
                "Would you like to see options in different price ranges?"
            ],
            'timeline': [
                "When do you need this by?",
                "Is this urgent or can we take time to find the perfect fit?",
                "Are you ready to buy today or still exploring?",
                "What's your timeline for making a decision?"
            ],
            'preferences': [
                "What style speaks to you?",
                "Do you have any color or design preferences?",
                "What brands do you usually love?",
                "Can you describe your ideal product?"
            ]
        }
        
        # Objection handling frameworks
        self.objection_handlers = {
            'price': self._handle_price_objection,
            'quality': self._handle_quality_objection,
            'timing': self._handle_timing_objection,
            'comparison': self._handle_comparison_objection,
            'uncertainty': self._handle_uncertainty_objection
        }
    
    def ask_discovery_question(self, category: str, context: Dict) -> str:
        """
        Ask an open-ended discovery question to understand customer needs
        """
        questions = self.discovery_questions.get(category, self.discovery_questions['needs'])
        question = random.choice(questions)
        
        # Personalize with customer name if available
        customer_name = context.get('customer_name', '')
        if customer_name:
            question = f"{customer_name}, {question.lower()}"
        
        return question
    
    def create_value_proposition(self, product: Dict, customer_context: Dict) -> str:
        """
        Create a compelling value proposition tailored to customer needs
        Uses features → benefits → value framework
        """
        product_name = product.get('name', 'this product')
        price = product.get('price', 0)
        
        # Identify customer's likely pain points from context
        pain_points = self._identify_pain_points(customer_context)
        
        # Build value proposition
        value_prop = f"Let me tell you why {product_name} could be perfect for you:\n\n"
        
        # Feature-Benefit-Value statements
        if 'quality' in pain_points:
            value_prop += "✨ **Premium Quality**: Made with top-grade materials that last years, "
            value_prop += "saving you money in the long run.\n\n"
        
        if 'time' in pain_points:
            value_prop += "⚡ **Time-Saving**: Designed for quick and easy use, "
            value_prop += "giving you more time for what matters.\n\n"
        
        if 'value' in pain_points:
            value_prop += f"💰 **Great Value**: At ${price:.2f}, you're getting premium features "
            value_prop += "typically found in products costing twice as much.\n\n"
        
        # Social proof
        rating = product.get('rating', 4.5)
        reviews = product.get('reviews', 100)
        value_prop += f"⭐ **Trusted by {reviews}+ customers** with an average {rating}/5 rating.\n\n"
        
        # Create urgency (ethical)
        stock = product.get('stock', 10)
        if stock < 5:
            value_prop += f"⚠️ **Limited Stock**: Only {stock} left at this price.\n\n"
        
        value_prop += "What questions can I answer to help you decide?"
        
        return value_prop
    
    def suggest_complementary_items(self, primary_product: Dict, 
                                   customer_context: Dict) -> Dict:
        """
        Suggest complementary items using cross-selling techniques
        "These shoes pair well with..." approach
        """
        product_name = primary_product.get('name', 'this item')
        category = primary_product.get('category', 'product')
        
        # Generate contextual suggestions
        suggestions = []
        
        if category == 'Electronics':
            suggestions = [
                {
                    'product': 'Premium Case',
                    'reason': 'Protect your investment',
                    'benefit': 'Extends product life by years'
                },
                {
                    'product': 'Extended Warranty',
                    'reason': 'Peace of mind',
                    'benefit': 'Covers repairs and replacements'
                },
                {
                    'product': 'Accessories Bundle',
                    'reason': 'Complete setup',
                    'benefit': 'Save 20% vs buying separately'
                }
            ]
        elif category == 'Fashion':
            suggestions = [
                {
                    'product': 'Matching Accessories',
                    'reason': 'Complete the look',
                    'benefit': 'Professional styling advice included'
                },
                {
                    'product': 'Care Kit',
                    'reason': 'Keep it looking new',
                    'benefit': 'Extends product life'
                }
            ]
        else:
            suggestions = [
                {
                    'product': 'Related Item',
                    'reason': 'Customers also bought',
                    'benefit': 'Popular combination'
                }
            ]
        
        message = f"Great choice on the {product_name}! 🎉\n\n"
        message += "Many customers also love these complementary items:\n\n"
        
        for i, item in enumerate(suggestions, 1):
            message += f"{i}. **{item['product']}**\n"
            message += f"   Why: {item['reason']}\n"
            message += f"   Benefit: {item['benefit']}\n\n"
        
        message += "Would you like to add any of these to complete your purchase?"
        
        return {
            'message': message,
            'suggestions': suggestions,
            'upsell_type': 'complementary',
            'quick_actions': [
                'Add accessories bundle',
                'Just the main item',
                'Tell me more',
                'Show me alternatives'
            ]
        }
    
    def handle_objection(self, objection_type: str, objection_text: str, 
                        context: Dict) -> Dict:
        """
        Handle customer objections gracefully using proven frameworks
        """
        handler = self.objection_handlers.get(objection_type, self._handle_general_objection)
        return handler(objection_text, context)
    
    def create_urgency(self, product: Dict, ethical: bool = True) -> str:
        """
        Create ethical urgency to encourage decision-making
        """
        if not ethical:
            # Non-ethical urgency (not recommended)
            return "⚠️ LAST CHANCE! Buy now or miss out forever!"
        
        # Ethical urgency based on real factors
        urgency_messages = []
        
        stock = product.get('stock', 100)
        if stock < 10:
            urgency_messages.append(f"Only {stock} left in stock")
        
        promotion_ends = product.get('promotion_ends')
        if promotion_ends:
            urgency_messages.append(f"Sale ends {promotion_ends}")
        
        trending = product.get('trending', False)
        if trending:
            urgency_messages.append("Trending item - high demand")
        
        if urgency_messages:
            return "⏰ " + " • ".join(urgency_messages)
        
        return ""
    
    def build_rapport(self, customer_context: Dict, conversation_history: List) -> str:
        """
        Build rapport through personalization and empathy
        """
        customer_name = customer_context.get('name', 'there')
        
        # Check conversation history for rapport opportunities
        if len(conversation_history) == 0:
            return f"Hi {customer_name}! I'm excited to help you find exactly what you're looking for today. 😊"
        
        # Reference past interactions
        if len(conversation_history) > 5:
            return f"I appreciate you taking the time to explore options with me, {customer_name}. Let's find your perfect match!"
        
        # Show empathy
        return f"I understand, {customer_name}. Let me help you make the best decision."
    
    def use_social_proof(self, product: Dict, customer_context: Dict) -> str:
        """
        Leverage social proof to build trust
        """
        rating = product.get('rating', 4.5)
        reviews = product.get('reviews', 100)
        bestseller = product.get('bestseller', False)
        
        proof_elements = []
        
        if bestseller:
            proof_elements.append("🏆 **Bestseller** in this category")
        
        if rating >= 4.5:
            proof_elements.append(f"⭐ **{rating}/5 stars** from {reviews}+ verified buyers")
        
        if reviews > 500:
            proof_elements.append(f"💬 **{reviews}+ reviews** - customers love it")
        
        # Customer testimonials
        testimonial = product.get('top_review')
        if testimonial:
            proof_elements.append(f'💭 "{testimonial}"')
        
        return "\n".join(proof_elements)
    
    def create_comparison(self, product_a: Dict, product_b: Dict) -> str:
        """
        Create helpful product comparisons
        """
        comparison = "Let me help you compare these options:\n\n"
        
        comparison += f"**{product_a['name']}** vs **{product_b['name']}**\n\n"
        
        # Price comparison
        comparison += f"💰 Price: ${product_a['price']} vs ${product_b['price']}\n"
        
        # Feature comparison
        comparison += f"⭐ Rating: {product_a.get('rating', 'N/A')} vs {product_b.get('rating', 'N/A')}\n"
        
        # Value recommendation
        if product_a['price'] < product_b['price']:
            comparison += f"\n💡 **Value Pick**: {product_a['name']} offers great features at a lower price.\n"
        else:
            comparison += f"\n💡 **Premium Pick**: {product_b['name']} has advanced features worth the investment.\n"
        
        comparison += "\nWhich features matter most to you?"
        
        return comparison
    
    def close_sale(self, context: Dict, soft: bool = True) -> Dict:
        """
        Close the sale using assumptive or soft close techniques
        """
        cart_items = context.get('cart', [])
        total = sum(item.get('price', 0) for item in cart_items)
        
        if soft:
            # Soft close - assumes sale, offers choices
            message = "Perfect! Let's get this wrapped up for you. 🎉\n\n"
            message += f"Your total is ${total:.2f}. "
            message += "Would you like to proceed with checkout, or is there anything else you'd like to add?"
            
            actions = [
                'Proceed to checkout',
                'Add more items',
                'Apply promo code',
                'Review cart'
            ]
        else:
            # Direct close
            message = "Are you ready to complete your purchase?"
            actions = [
                'Yes, checkout now',
                'Not yet, still browsing',
                'I have questions',
                'Save for later'
            ]
        
        return {
            'message': message,
            'close_type': 'soft' if soft else 'direct',
            'actions': actions,
            'cart_total': total
        }
    
    # Private objection handling methods
    def _handle_price_objection(self, objection: str, context: Dict) -> Dict:
        """Handle price objections using value reframing"""
        
        # Acknowledge and reframe
        message = "I completely understand - price is an important consideration. "
        message += "Let me help you see the full value:\n\n"
        
        # Break down cost
        message += "💰 **Value Breakdown**:\n"
        message += "• Premium quality that lasts 5+ years\n"
        message += "• Free shipping and returns\n"
        message += "• 2-year warranty included\n"
        message += "• Daily cost: Less than a coffee!\n\n"
        
        # Offer alternatives
        message += "I can also show you:\n"
        message += "• Payment plans (4 interest-free payments)\n"
        message += "• Similar items at different price points\n"
        message += "• Current promotions and discounts\n\n"
        
        message += "What would work best for your budget?"
        
        return {
            'message': message,
            'objection_type': 'price',
            'handled': True,
            'suggestions': [
                'Show payment plans',
                'See similar items',
                'Apply available discounts',
                'Explain value more'
            ]
        }
    
    def _handle_quality_objection(self, objection: str, context: Dict) -> Dict:
        """Handle quality concerns"""
        
        message = "Quality is absolutely crucial - I'm glad you're asking! "
        message += "Let me address your concerns:\n\n"
        
        message += "✅ **Quality Assurance**:\n"
        message += "• Premium materials and craftsmanship\n"
        message += "• Rigorous quality control process\n"
        message += "• 2-year warranty coverage\n"
        message += "• 4.8/5 star rating from 1000+ customers\n\n"
        
        message += "🔍 **Try Risk-Free**:\n"
        message += "• 30-day money-back guarantee\n"
        message += "• Free returns, no questions asked\n"
        message += "• Read verified customer reviews\n\n"
        
        message += "Would you like to see customer photos and reviews?"
        
        return {
            'message': message,
            'objection_type': 'quality',
            'handled': True,
            'suggestions': [
                'Show customer reviews',
                'View quality certifications',
                'See warranty details',
                'Compare with competitors'
            ]
        }
    
    def _handle_timing_objection(self, objection: str, context: Dict) -> Dict:
        """Handle 'not ready to buy' objections"""
        
        message = "No pressure at all! I want you to feel completely confident. "
        message += "Here's what I can do:\n\n"
        
        message += "💾 **Save for Later**:\n"
        message += "• I'll save your cart for 30 days\n"
        message += "• Get price drop alerts\n"
        message += "• Receive restock notifications\n\n"
        
        message += "📧 **Stay Informed**:\n"
        message += "• Email you product details\n"
        message += "• Notify you of sales\n"
        message += "• Send comparison guides\n\n"
        
        message += "When would be a good time to follow up?"
        
        return {
            'message': message,
            'objection_type': 'timing',
            'handled': True,
            'suggestions': [
                'Save cart for later',
                'Email me details',
                'Set price alert',
                'Continue browsing'
            ]
        }
    
    def _handle_comparison_objection(self, objection: str, context: Dict) -> Dict:
        """Handle 'need to compare' objections"""
        
        message = "Smart move! Comparing options ensures you get the best fit. "
        message += "Let me make this easier:\n\n"
        
        message += "📊 **Comparison Tools**:\n"
        message += "• Side-by-side feature comparison\n"
        message += "• Price match guarantee\n"
        message += "• Expert buying guides\n"
        message += "• Customer review summaries\n\n"
        
        message += "🎯 **Why Choose Us**:\n"
        message += "• Best price guarantee\n"
        message += "• Free shipping & returns\n"
        message += "• 24/7 customer support\n"
        message += "• Exclusive member benefits\n\n"
        
        message += "What specific features are you comparing?"
        
        return {
            'message': message,
            'objection_type': 'comparison',
            'handled': True,
            'suggestions': [
                'Compare features',
                'See price match policy',
                'View buying guide',
                'Chat with expert'
            ]
        }
    
    def _handle_uncertainty_objection(self, objection: str, context: Dict) -> Dict:
        """Handle general uncertainty"""
        
        message = "I understand - it's important to feel confident about your purchase. "
        message += "Let me help clarify:\n\n"
        
        message += "❓ **Common Questions**:\n"
        message += "• What are you most unsure about?\n"
        message += "• What would make you feel confident?\n"
        message += "• What's holding you back?\n\n"
        
        message += "🛡️ **Risk-Free Purchase**:\n"
        message += "• 30-day returns\n"
        message += "• Price match guarantee\n"
        message += "• Expert support\n"
        message += "• Secure checkout\n\n"
        
        message += "What specific concerns can I address?"
        
        return {
            'message': message,
            'objection_type': 'uncertainty',
            'handled': True,
            'suggestions': [
                'Ask specific questions',
                'See return policy',
                'Read customer reviews',
                'Chat with expert'
            ]
        }
    
    def _handle_general_objection(self, objection: str, context: Dict) -> Dict:
        """Handle any other objections"""
        
        message = "I appreciate you sharing that concern. Let me help address it. "
        message += "Can you tell me more about what's on your mind?"
        
        return {
            'message': message,
            'objection_type': 'general',
            'handled': True,
            'suggestions': [
                'Explain my concern',
                'See more details',
                'Talk to expert',
                'Browse alternatives'
            ]
        }
    
    def _identify_pain_points(self, customer_context: Dict) -> List[str]:
        """Identify customer pain points from context"""
        pain_points = []
        
        # Analyze purchase history
        history = customer_context.get('purchase_history', [])
        if history:
            # Check for quality issues
            if any(item.get('rating', 5) < 4 for item in history):
                pain_points.append('quality')
        
        # Check preferences
        preferences = customer_context.get('preferences', {})
        if preferences.get('budget_conscious'):
            pain_points.append('value')
        
        if preferences.get('busy_lifestyle'):
            pain_points.append('time')
        
        # Default pain points if none identified
        if not pain_points:
            pain_points = ['quality', 'value']
        
        return pain_points


# Global instance
sales_psychology = SalesPsychology()
