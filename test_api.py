#!/usr/bin/env python3
"""
Test API endpoints to verify they're working
"""

import requests
import json

def test_api_endpoints():
    """Test the main API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing API Endpoints...")
    print("=" * 40)
    
    # Test chat endpoint
    try:
        response = requests.post(f"{base_url}/api/chat", 
                               json={"message": "Hello", "channel": "web"},
                               timeout=5)
        if response.status_code == 200:
            print("✅ Chat API working")
            data = response.json()
            print(f"   Response: {data.get('message', 'No message')[:50]}...")
        else:
            print(f"❌ Chat API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat API error: {e}")
    
    # Test product search
    try:
        response = requests.post(f"{base_url}/api/products/search",
                               json={"query": "laptop", "filters": {}},
                               timeout=5)
        if response.status_code == 200:
            print("✅ Product Search API working")
            data = response.json()
            print(f"   Found {len(data.get('products', []))} products")
        else:
            print(f"❌ Product Search API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Product Search API error: {e}")
    
    # Test promotions
    try:
        response = requests.get(f"{base_url}/api/promotions", timeout=5)
        if response.status_code == 200:
            print("✅ Promotions API working")
        else:
            print(f"❌ Promotions API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Promotions API error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
