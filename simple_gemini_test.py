#!/usr/bin/env python3
"""
Simple Gemini API test
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API directly"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No GEMINI_API_KEY found")
        return False
    
    print(f"🔑 Using API Key: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Test simple generation
        response = model.generate_content("Hello, how are you?")
        
        if response.text:
            print(f"✅ Success: {response.text[:100]}...")
            return True
        else:
            print("❌ Empty response")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gemini_api()
