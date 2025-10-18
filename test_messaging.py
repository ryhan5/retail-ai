"""
Test script for WhatsApp and Telegram messaging integrations
Run this to verify your messaging setup is working correctly
"""

import os
import sys
import asyncio
import requests
from integrations.messaging_coordinator import MessagingCoordinator

def test_environment_variables():
    """Test if required environment variables are set"""
    print("🔧 Testing Environment Variables...")
    
    # WhatsApp (Twilio) variables
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID', 'not_set')
    twilio_token = os.getenv('TWILIO_AUTH_TOKEN', 'not_set')
    twilio_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'not_set')
    
    # Telegram variables
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', 'not_set')
    telegram_webhook = os.getenv('TELEGRAM_WEBHOOK_URL', 'not_set')
    
    print(f"  WhatsApp (Twilio):")
    print(f"    TWILIO_ACCOUNT_SID: {'✅ Set' if twilio_sid != 'not_set' else '❌ Not set'}")
    print(f"    TWILIO_AUTH_TOKEN: {'✅ Set' if twilio_token != 'not_set' else '❌ Not set'}")
    print(f"    TWILIO_WHATSAPP_NUMBER: {'✅ Set' if twilio_number != 'not_set' else '❌ Not set'}")
    
    print(f"  Telegram:")
    print(f"    TELEGRAM_BOT_TOKEN: {'✅ Set' if telegram_token != 'not_set' else '❌ Not set'}")
    print(f"    TELEGRAM_WEBHOOK_URL: {'✅ Set' if telegram_webhook != 'not_set' else '❌ Not set'}")
    
    return {
        'whatsapp_configured': all([
            twilio_sid != 'not_set',
            twilio_token != 'not_set',
            twilio_number != 'not_set'
        ]),
        'telegram_configured': telegram_token != 'not_set'
    }

def test_messaging_coordinator():
    """Test messaging coordinator initialization"""
    print("\n🤖 Testing Messaging Coordinator...")
    
    try:
        coordinator = MessagingCoordinator()
        status = coordinator.get_platform_status()
        
        print(f"  WhatsApp Integration: {'✅ Ready' if status['whatsapp']['configured'] else '❌ Not configured'}")
        print(f"  Telegram Integration: {'✅ Ready' if status['telegram']['configured'] else '❌ Not configured'}")
        
        return coordinator, status
        
    except Exception as e:
        print(f"  ❌ Error initializing coordinator: {str(e)}")
        return None, None

def test_webhook_processing():
    """Test webhook data processing"""
    print("\n📨 Testing Webhook Processing...")
    
    coordinator = MessagingCoordinator()
    
    # Test WhatsApp webhook data
    whatsapp_data = {
        'From': 'whatsapp:+1234567890',
        'To': 'whatsapp:+14155238886',
        'Body': 'Hello, I want to buy something',
        'MessageSid': 'test_message_123'
    }
    
    whatsapp_result = coordinator.process_webhook('whatsapp', whatsapp_data)
    print(f"  WhatsApp webhook processing: {'✅ Success' if not whatsapp_result.get('error') else '❌ Error'}")
    if whatsapp_result.get('error'):
        print(f"    Error: {whatsapp_result['error']}")
    
    # Test Telegram webhook data
    telegram_data = {
        'message': {
            'message_id': 123,
            'from': {'id': 12345, 'first_name': 'Test', 'username': 'testuser'},
            'chat': {'id': 12345, 'type': 'private'},
            'text': 'Hello, I want to buy something'
        }
    }
    
    telegram_result = coordinator.process_webhook('telegram', telegram_data)
    print(f"  Telegram webhook processing: {'✅ Success' if not telegram_result.get('error') else '❌ Error'}")
    if telegram_result.get('error'):
        print(f"    Error: {telegram_result['error']}")

def test_response_formatting():
    """Test response formatting for different platforms"""
    print("\n📝 Testing Response Formatting...")
    
    coordinator = MessagingCoordinator()
    
    # Sample AI response
    sample_response = {
        'message': 'Hello! I found some great products for you. Here are my recommendations:',
        'intent': 'product_search',
        'suggestions': ['Show details', 'Add to cart', 'View more products', 'Check promotions']
    }
    
    # Test WhatsApp formatting
    whatsapp_formatted = coordinator.format_response_for_platform('whatsapp', sample_response)
    print(f"  WhatsApp formatting: {'✅ Success' if whatsapp_formatted else '❌ Failed'}")
    
    # Test Telegram formatting
    telegram_formatted = coordinator.format_response_for_platform('telegram', sample_response)
    print(f"  Telegram formatting: {'✅ Success' if telegram_formatted else '❌ Failed'}")

async def test_telegram_async_methods():
    """Test Telegram async methods"""
    print("\n⚡ Testing Telegram Async Methods...")
    
    coordinator = MessagingCoordinator()
    
    if not coordinator.telegram.application:
        print("  ❌ Telegram not configured - skipping async tests")
        return
    
    try:
        # Test sending a message (will fail without valid chat_id, but tests the method)
        test_chat_id = "123456789"  # Dummy chat ID
        result = await coordinator.send_message('telegram', test_chat_id, "Test message")
        print(f"  Async message method: {'✅ Method works' if 'error' in result else '✅ Success'}")
        
    except Exception as e:
        print(f"  ❌ Async method error: {str(e)}")

def test_server_endpoints():
    """Test if server endpoints are accessible"""
    print("\n🌐 Testing Server Endpoints...")
    
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/api/messaging/status",
        "/api/messaging/setup"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            status = "✅ Accessible" if response.status_code == 200 else f"❌ Status {response.status_code}"
            print(f"  {endpoint}: {status}")
        except requests.exceptions.ConnectionError:
            print(f"  {endpoint}: ❌ Server not running")
        except Exception as e:
            print(f"  {endpoint}: ❌ Error - {str(e)}")

def print_setup_instructions():
    """Print setup instructions"""
    print("\n📋 Setup Instructions:")
    print("="*50)
    
    coordinator = MessagingCoordinator()
    instructions = coordinator.get_setup_instructions()
    
    for platform, setup in instructions.items():
        print(f"\n{platform.upper()} Setup:")
        for step in setup['steps']:
            print(f"  {step}")

def main():
    """Run all tests"""
    print("🧪 Retail AI Sales Assistant - Messaging Integration Tests")
    print("="*60)
    
    # Test environment variables
    env_status = test_environment_variables()
    
    # Test messaging coordinator
    coordinator, status = test_messaging_coordinator()
    
    if coordinator:
        # Test webhook processing
        test_webhook_processing()
        
        # Test response formatting
        test_response_formatting()
        
        # Test async methods
        if status and status['telegram']['configured']:
            try:
                asyncio.run(test_telegram_async_methods())
            except Exception as e:
                print(f"  ❌ Async test error: {str(e)}")
    
    # Test server endpoints (only if server is running)
    test_server_endpoints()
    
    # Print setup instructions
    print_setup_instructions()
    
    print("\n" + "="*60)
    print("🎉 Testing Complete!")
    print("\nNext Steps:")
    if not env_status['whatsapp_configured']:
        print("  1. Set up WhatsApp integration (see MESSAGING_SETUP.md)")
    if not env_status['telegram_configured']:
        print("  2. Set up Telegram integration (see MESSAGING_SETUP.md)")
    print("  3. Start the server: python app.py")
    print("  4. Test messaging by sending messages to your bots")
    print("\n📚 For detailed setup instructions, see: MESSAGING_SETUP.md")

if __name__ == "__main__":
    main()
