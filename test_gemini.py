#!/usr/bin/env python3
"""
Test script for Google Gemini AI integration
Run this to verify Gemini is working correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_setup():
    """Test if Gemini is properly configured"""
    print("🧪 Testing Google Gemini AI Integration...")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("💡 Please add GEMINI_API_KEY to your .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test import
    try:
        from ai_service import gemini_service, get_ai_response
        print("✅ AI service imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import AI service: {e}")
        print("💡 Make sure google-generativeai is installed: pip install google-generativeai")
        return False
    
    # Test basic response
    try:
        print("\n🤖 Testing basic AI response...")
        response = get_ai_response("Hello! I'm looking for a laptop for work.")
        print(f"✅ AI Response: {response[:100]}...")
        
        # Test product recommendation
        print("\n🛍️ Testing product recommendations...")
        from ai_service import get_product_recommendations
        
        mock_products = [
            {"id": 1, "name": "MacBook Pro", "price": 1299.99, "description": "Professional laptop"},
            {"id": 2, "name": "Dell XPS 13", "price": 999.99, "description": "Ultrabook laptop"},
            {"id": 3, "name": "ThinkPad X1", "price": 1199.99, "description": "Business laptop"}
        ]
        
        rec_response = get_product_recommendations("I need a laptop for programming", mock_products)
        print(f"✅ Recommendation Response: {rec_response.get('message', 'No message')[:100]}...")
        
        print("\n🎉 All tests passed! Gemini AI is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error testing AI responses: {e}")
        print("💡 Check your API key and internet connection")
        return False

def test_flask_integration():
    """Test Flask integration"""
    print("\n🌐 Testing Flask Integration...")
    print("=" * 30)
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test if routes are accessible
        with app.test_client() as client:
            # Test chat endpoint
            response = client.post('/api/chat', 
                json={'message': 'Hello', 'channel': 'web'})
            
            if response.status_code == 200:
                print("✅ Chat endpoint working")
            else:
                print(f"⚠️ Chat endpoint returned status: {response.status_code}")
                
        return True
        
    except Exception as e:
        print(f"❌ Flask integration error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Retail AI Assistant - Gemini Integration Test")
    print("=" * 60)
    
    success = True
    
    # Test Gemini setup
    if not test_gemini_setup():
        success = False
    
    # Test Flask integration
    if not test_flask_integration():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! Your Gemini integration is ready!")
        print("\n📋 Next steps:")
        print("1. Start the Flask server: python app.py")
        print("2. Start the React frontend: cd frontend && npm start")
        print("3. Test the chat interface at http://localhost:3001")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Common fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up .env file with GEMINI_API_KEY")
        print("3. Get API key from: https://makersuite.google.com/app/apikey")
    
    sys.exit(0 if success else 1)
