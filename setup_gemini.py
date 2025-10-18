#!/usr/bin/env python3
"""
Setup script for Google Gemini AI integration
Helps users configure their API key and test the setup
"""

import os
import sys
from pathlib import Path

def setup_gemini_api():
    """Interactive setup for Gemini API"""
    print("🚀 Google Gemini AI Setup for Retail Assistant")
    print("=" * 55)
    
    # Check if .env exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found!")
        print("💡 Please copy .env.example to .env first")
        return False
    
    # Read current .env
    with open('.env', 'r') as f:
        env_content = f.read()
    
    # Check if API key is set
    if 'GEMINI_API_KEY=your_gemini_api_key_here' in env_content:
        print("⚠️  Gemini API key not configured yet")
        print("\n📋 To get your Gemini API key:")
        print("1. Go to: https://makersuite.google.com/app/apikey")
        print("2. Sign in with your Google account")
        print("3. Click 'Create API Key'")
        print("4. Copy the generated key")
        print("\n🔧 Then update your .env file:")
        print("Replace 'your_gemini_api_key_here' with your actual API key")
        
        # Ask if user wants to enter key now
        print("\n" + "="*50)
        response = input("Do you have your API key ready? (y/n): ").lower().strip()
        
        if response == 'y':
            api_key = input("Enter your Gemini API key: ").strip()
            if api_key and len(api_key) > 10:
                # Update .env file
                updated_content = env_content.replace(
                    'GEMINI_API_KEY=your_gemini_api_key_here',
                    f'GEMINI_API_KEY={api_key}'
                )
                
                with open('.env', 'w') as f:
                    f.write(updated_content)
                
                print("✅ API key updated in .env file!")
                return True
            else:
                print("❌ Invalid API key. Please try again.")
                return False
        else:
            print("💡 Please update your .env file manually and run this script again.")
            return False
    
    else:
        print("✅ Gemini API key appears to be configured")
        return True

def test_basic_functionality():
    """Test basic Gemini functionality"""
    print("\n🧪 Testing Gemini Integration...")
    print("=" * 35)
    
    try:
        # Test import
        from ai_service import get_ai_response
        print("✅ AI service imported successfully")
        
        # Test basic response (this will fail without real API key)
        print("⏳ Testing AI response (this may take a moment)...")
        response = get_ai_response("Hello! Can you help me with shopping?")
        
        if response and len(response) > 10:
            print("✅ AI response received!")
            print(f"📝 Sample response: {response[:100]}...")
            return True
        else:
            print("⚠️  AI response seems empty or invalid")
            return False
            
    except Exception as e:
        print(f"❌ Error testing AI: {str(e)}")
        if "API_KEY" in str(e):
            print("💡 This looks like an API key issue")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎯 Next Steps:")
    print("=" * 20)
    print("1. 🌐 Start the Flask backend:")
    print("   python app.py")
    print("\n2. 🎨 Start the React frontend:")
    print("   cd frontend")
    print("   npm start")
    print("\n3. 🧪 Test the chat interface:")
    print("   Open http://localhost:3001")
    print("   Try asking: 'Show me some laptops'")
    print("\n4. 📱 Optional - Set up messaging:")
    print("   Follow MESSAGING_SETUP.md for WhatsApp/Telegram")

def main():
    """Main setup function"""
    print("🛍️ Retail AI Assistant - Gemini Setup")
    print("=" * 45)
    
    # Setup API key
    if not setup_gemini_api():
        print("\n❌ Setup incomplete. Please configure your API key first.")
        sys.exit(1)
    
    # Test functionality
    if test_basic_functionality():
        print("\n🎉 SUCCESS! Gemini AI is working correctly!")
        show_next_steps()
    else:
        print("\n⚠️  Setup completed but testing failed.")
        print("💡 This might be due to:")
        print("   - Invalid API key")
        print("   - Network connectivity issues")
        print("   - API quota limits")
        print("\n🔧 Try running the app anyway - it might work!")
        show_next_steps()

if __name__ == "__main__":
    main()
