"""
Google Gemini AI Service for Retail Sales Assistant
Replaces OpenAI with Google's Gemini Pro model
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAIService:
    """Service class for interacting with Google Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini AI service"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.is_configured = False
        
        if not self.api_key or self.api_key == 'your_actual_gemini_api_key_here':
            logger.warning("GEMINI_API_KEY not configured. AI features will use fallback responses.")
            self.model = None
            return
        
        try:
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            # Initialize the model
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Updated to Gemini 2.0 Flash
            
            # Safety settings
            self.safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
            
            self.is_configured = True
            logger.info("Gemini AI Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {e}")
            self.model = None
    
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Generate a response using Gemini 2.0 Flash
        
        Args:
            prompt: The input prompt
            context: Optional context for the conversation
            
        Returns:
            Generated response text
        """
        # If Gemini is not configured, return fallback response
        if not self.is_configured or not self.model:
            return self._get_fallback_response(prompt)
        
        try:
            # Build the full prompt with context
            full_prompt = self._build_prompt_with_context(prompt, context)
            
            # Generate response
            response = self.model.generate_content(
                full_prompt,
                safety_settings=self.safety_settings,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=1024,
                )
            )
            
            if response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response from Gemini")
                return "I apologize, but I'm having trouble generating a response right now. Please try again."
                
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            return "I'm experiencing technical difficulties. Please try again in a moment."
    
    def _get_fallback_response(self, prompt: str) -> str:
        """Generate fallback responses when Gemini is not available"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! Welcome to our store. I'm here to help you find the perfect products. How can I assist you today?"
        
        elif any(word in prompt_lower for word in ['product', 'search', 'find', 'looking']):
            return "I'd be happy to help you find products! You can browse our categories or search for specific items. What are you looking for?"
        
        elif any(word in prompt_lower for word in ['cart', 'checkout', 'buy', 'purchase']):
            return "Great! I can help you with your cart and checkout process. Let me know what you'd like to add or if you're ready to complete your purchase."
        
        elif any(word in prompt_lower for word in ['recommend', 'suggest', 'advice']):
            return "I'd love to give you personalized recommendations! Could you tell me more about what you're interested in or what you're shopping for?"
        
        elif any(word in prompt_lower for word in ['price', 'cost', 'deal', 'discount']):
            return "I can help you find great deals and pricing information. Check out our current promotions and compare prices on our products!"
        
        else:
            return "Thank you for your message! I'm here to help you with product searches, recommendations, cart management, and more. How can I assist you today?"
    
    def _build_prompt_with_context(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Build a comprehensive prompt with context"""
        
        system_prompt = """You are an expert AI sales assistant for a modern retail company. Your role is to help customers find products, make purchases, and have an excellent shopping experience.

Key responsibilities:
- Help customers discover products based on their needs
- Provide detailed product information and recommendations
- Assist with cart management and checkout process
- Answer questions about promotions, shipping, and policies
- Maintain a friendly, professional, and helpful tone
- Focus on customer satisfaction and sales conversion

Available product categories: Electronics, Clothing, Footwear, Accessories
You can help with: Product search, recommendations, cart management, promotions, customer support

Always be concise but informative, and guide customers toward making purchases when appropriate."""

        # Add context if provided
        context_str = ""
        if context:
            if context.get('customer_name'):
                context_str += f"Customer: {context['customer_name']}\n"
            if context.get('cart_items'):
                context_str += f"Current cart: {len(context['cart_items'])} items\n"
            if context.get('previous_messages'):
                context_str += "Recent conversation:\n"
                for msg in context['previous_messages'][-3:]:  # Last 3 messages
                    context_str += f"- {msg.get('sender', 'User')}: {msg.get('content', '')}\n"
        
        # Combine all parts
        full_prompt = f"{system_prompt}\n\n{context_str}\nCustomer: {prompt}\n\nAssistant:"
        
        return full_prompt
    
    def generate_product_recommendation(self, user_query: str, products: List[Dict]) -> Dict:
        """
        Generate product recommendations based on user query
        
        Args:
            user_query: User's search or preference query
            products: List of available products
            
        Returns:
            Recommendation response with products and explanation
        """
        try:
            # Build product context
            products_context = "Available products:\n"
            for product in products[:10]:  # Limit to first 10 products
                products_context += f"- {product.get('name', 'Unknown')}: ${product.get('price', 0):.2f} - {product.get('description', 'No description')}\n"
            
            prompt = f"""Based on the customer's request: "{user_query}"

{products_context}

Please recommend the most suitable products and explain why they match the customer's needs. Format your response as a helpful sales assistant would, highlighting key features and benefits.

Provide a natural, conversational response that includes:
1. Acknowledgment of their request
2. Specific product recommendations with reasons
3. Key features that match their needs
4. Encouragement to explore or purchase"""

            response = self.generate_response(prompt)
            
            return {
                'type': 'recommendation',
                'message': response,
                'recommended_products': products[:3]  # Return top 3 products
            }
            
        except Exception as e:
            logger.error(f"Error generating product recommendation: {str(e)}")
            return {
                'type': 'error',
                'message': "I'm having trouble finding the best recommendations right now. Please try browsing our products directly."
            }
    
    def generate_cart_summary(self, cart_items: List[Dict], customer_context: Optional[Dict] = None) -> str:
        """
        Generate a summary of cart items with AI insights
        
        Args:
            cart_items: List of items in cart
            customer_context: Optional customer information
            
        Returns:
            AI-generated cart summary and suggestions
        """
        try:
            if not cart_items:
                return "Your cart is empty. Would you like me to help you find some great products?"
            
            # Build cart context
            cart_context = f"Customer's cart ({len(cart_items)} items):\n"
            total_value = 0
            
            for item in cart_items:
                item_total = item.get('price', 0) * item.get('quantity', 1)
                total_value += item_total
                cart_context += f"- {item.get('name', 'Unknown')}: {item.get('quantity', 1)}x ${item.get('price', 0):.2f} = ${item_total:.2f}\n"
            
            cart_context += f"Total: ${total_value:.2f}"
            
            prompt = f"""Analyze this customer's shopping cart and provide helpful insights:

{cart_context}

Please provide:
1. A friendly summary of their cart
2. Any complementary product suggestions
3. Information about shipping or promotions if applicable
4. Encouragement to complete their purchase

Keep the tone conversational and helpful, like a knowledgeable sales associate."""

            return self.generate_response(prompt, customer_context)
            
        except Exception as e:
            logger.error(f"Error generating cart summary: {str(e)}")
            return "Here's your cart summary. You have some great items selected!"
    
    def generate_promotion_message(self, promotions: List[Dict], customer_context: Optional[Dict] = None) -> str:
        """
        Generate personalized promotion messages
        
        Args:
            promotions: List of available promotions
            customer_context: Customer information for personalization
            
        Returns:
            Personalized promotion message
        """
        try:
            if not promotions:
                return "We don't have any special promotions right now, but our products are always competitively priced!"
            
            # Build promotions context
            promo_context = "Current promotions:\n"
            for promo in promotions[:5]:  # Limit to 5 promotions
                promo_context += f"- {promo.get('name', 'Special Offer')}: {promo.get('description', 'Great savings!')}\n"
            
            prompt = f"""Create an engaging message about our current promotions for a customer:

{promo_context}

Make it:
1. Exciting and compelling
2. Clear about the benefits
3. Include a call to action
4. Personalized and friendly

Keep it concise but persuasive."""

            return self.generate_response(prompt, customer_context)
            
        except Exception as e:
            logger.error(f"Error generating promotion message: {str(e)}")
            return "We have some great deals available! Check out our current promotions."

# Global instance
gemini_service = GeminiAIService()

def get_ai_response(message: str, context: Optional[Dict] = None) -> str:
    """
    Convenience function to get AI response
    
    Args:
        message: User message
        context: Optional context
        
    Returns:
        AI response
    """
    return gemini_service.generate_response(message, context)

def get_product_recommendations(query: str, products: List[Dict]) -> Dict:
    """
    Convenience function for product recommendations
    
    Args:
        query: User query
        products: Available products
        
    Returns:
        Recommendation response
    """
    return gemini_service.generate_product_recommendation(query, products)

def get_cart_summary(cart_items: List[Dict], customer_context: Optional[Dict] = None) -> str:
    """
    Convenience function for cart summary
    
    Args:
        cart_items: Cart items
        customer_context: Customer context
        
    Returns:
        Cart summary
    """
    return gemini_service.generate_cart_summary(cart_items, customer_context)

def get_promotion_message(promotions: List[Dict], customer_context: Optional[Dict] = None) -> str:
    """
    Convenience function for promotion messages
    
    Args:
        promotions: Available promotions
        customer_context: Customer context
        
    Returns:
        Promotion message
    """
    return gemini_service.generate_promotion_message(promotions, customer_context)
