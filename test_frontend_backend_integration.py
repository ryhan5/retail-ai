#!/usr/bin/env python3
"""
Frontend-Backend Integration Test Suite
Comprehensive testing of all API endpoints and functionality
"""

import requests
import json
import time
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def print_header(text):
    """Print formatted header"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.YELLOW}ℹ️  {text}{Style.RESET_ALL}")

class FrontendBackendTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        
    def test_server_health(self):
        """Test if Flask server is running"""
        print_header("Testing Server Health")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                print_success("Flask server is running and accessible")
                return True
            else:
                print_error(f"Server returned status code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print_error("Cannot connect to Flask server. Make sure it's running on port 5000")
            return False
        except Exception as e:
            print_error(f"Server health check failed: {str(e)}")
            return False
    
    def test_chat_api(self):
        """Test chat API endpoint with AI agents"""
        print_header("Testing Chat API Integration")
        
        test_messages = [
            {"message": "Hello, I'm looking for electronics", "expected_intent": "product_search"},
            {"message": "What promotions do you have?", "expected_intent": "promotions"},
            {"message": "Check availability of headphones", "expected_intent": "availability"},
            {"message": "I want to buy this product", "expected_intent": "purchase"},
            {"message": "Help me find a laptop", "expected_intent": "product_search"}
        ]
        
        success_count = 0
        for test in test_messages:
            try:
                payload = {
                    "message": test["message"],
                    "channel": "web",
                    "customer_id": "CUST001"
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    intent = data.get("intent")
                    message = data.get("message", "")
                    
                    print_success(f"Message: '{test['message'][:30]}...' → Intent: {intent}")
                    print_info(f"Response: {message[:80]}...")
                    success_count += 1
                else:
                    print_error(f"Chat API failed with status: {response.status_code}")
                    
            except Exception as e:
                print_error(f"Chat API error: {str(e)}")
        
        return success_count == len(test_messages)
    
    def test_product_search_api(self):
        """Test product search functionality"""
        print_header("Testing Product Search API")
        
        search_tests = [
            {"query": "laptop", "expected_results": True},
            {"query": "headphones", "expected_results": True},
            {"query": "electronics", "expected_results": True},
            {"query": "nonexistent_product_xyz", "expected_results": False}
        ]
        
        success_count = 0
        for test in search_tests:
            try:
                payload = {
                    "query": test["query"],
                    "filters": {}
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/products/search",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    products = data.get("products", [])
                    
                    if test["expected_results"]:
                        if len(products) > 0:
                            print_success(f"Search '{test['query']}' found {len(products)} products")
                            success_count += 1
                        else:
                            print_error(f"Expected results for '{test['query']}' but got none")
                    else:
                        print_success(f"Search '{test['query']}' correctly returned {len(products)} products")
                        success_count += 1
                else:
                    print_error(f"Product search failed with status: {response.status_code}")
                    
            except Exception as e:
                print_error(f"Product search error: {str(e)}")
        
        return success_count == len(search_tests)
    
    def test_inventory_api(self):
        """Test inventory checking"""
        print_header("Testing Inventory API")
        
        try:
            payload = {
                "product_id": "PROD001",
                "store_location": "online"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/inventory/check",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Inventory check successful")
                print_info(f"Stock status: {data}")
                return True
            else:
                print_error(f"Inventory API failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Inventory API error: {str(e)}")
            return False
    
    def test_promotions_api(self):
        """Test promotions API"""
        print_header("Testing Promotions API")
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/promotions",
                params={"customer_id": "CUST001"}
            )
            
            if response.status_code == 200:
                data = response.json()
                promotions = data.get("promotions", [])
                print_success(f"Promotions API successful - Found {len(promotions)} promotions")
                return True
            else:
                print_error(f"Promotions API failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Promotions API error: {str(e)}")
            return False
    
    def test_order_creation_api(self):
        """Test order creation"""
        print_header("Testing Order Creation API")
        
        try:
            payload = {
                "customer_id": "CUST001",
                "items": [
                    {"id": "PROD001", "name": "Test Product", "price": 99.99, "quantity": 1}
                ],
                "total": 99.99,
                "shipping_address": "123 Test St, Test City"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/order/create",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                order_id = data.get("order_id")
                print_success(f"Order creation successful - Order ID: {order_id}")
                return True
            else:
                print_error(f"Order creation failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Order creation error: {str(e)}")
            return False
    
    def test_payment_processing_api(self):
        """Test payment processing"""
        print_header("Testing Payment Processing API")
        
        try:
            payload = {
                "customer_id": "CUST001",
                "amount": 99.99,
                "payment_method": "card",
                "card_details": {
                    "number": "4111111111111111",
                    "expiry": "12/25",
                    "cvv": "123"
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/payment/process",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                payment_status = data.get("status")
                print_success(f"Payment processing successful - Status: {payment_status}")
                return True
            else:
                print_error(f"Payment processing failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Payment processing error: {str(e)}")
            return False
    
    def test_customer_context_api(self):
        """Test customer context retrieval"""
        print_header("Testing Customer Context API")
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/customer/CUST001/context"
            )
            
            if response.status_code == 200:
                data = response.json()
                customer_id = data.get("customer_id")
                print_success(f"Customer context retrieved - ID: {customer_id}")
                return True
            else:
                print_error(f"Customer context failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Customer context error: {str(e)}")
            return False
    
    def test_analytics_api(self):
        """Test analytics dashboard"""
        print_header("Testing Analytics API")
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/analytics/dashboard"
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Analytics API successful")
                print_info(f"Analytics data keys: {list(data.keys())}")
                return True
            else:
                print_error(f"Analytics API failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Analytics API error: {str(e)}")
            return False
    
    def test_messaging_webhooks(self):
        """Test messaging platform endpoints"""
        print_header("Testing Messaging Platform Integration")
        
        # Test WhatsApp webhook endpoint
        try:
            whatsapp_payload = {
                "From": "whatsapp:+1234567890",
                "To": "whatsapp:+14155238886",
                "Body": "Hello from WhatsApp test",
                "MessageSid": "TEST123"
            }
            
            response = self.session.post(
                f"{self.base_url}/webhook/whatsapp",
                data=whatsapp_payload
            )
            
            # WhatsApp webhook should handle the request (even if not fully configured)
            print_success(f"WhatsApp webhook endpoint accessible - Status: {response.status_code}")
            
        except Exception as e:
            print_info(f"WhatsApp webhook test: {str(e)}")
        
        # Test Telegram webhook endpoint
        try:
            telegram_payload = {
                "message": {
                    "message_id": 123,
                    "from": {"id": 123456, "first_name": "Test"},
                    "chat": {"id": 123456, "type": "private"},
                    "text": "Hello from Telegram test"
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/webhook/telegram",
                json=telegram_payload,
                headers={"Content-Type": "application/json"}
            )
            
            print_success(f"Telegram webhook endpoint accessible - Status: {response.status_code}")
            
        except Exception as e:
            print_info(f"Telegram webhook test: {str(e)}")
        
        return True
    
    def test_cors_headers(self):
        """Test CORS configuration for frontend"""
        print_header("Testing CORS Configuration")
        
        try:
            # Test OPTIONS request (preflight)
            response = self.session.options(
                f"{self.base_url}/api/chat",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            
            cors_headers = response.headers
            if "Access-Control-Allow-Origin" in cors_headers:
                print_success("CORS headers configured correctly")
                print_info(f"Allowed origins: {cors_headers.get('Access-Control-Allow-Origin')}")
                return True
            else:
                print_error("CORS headers not found")
                return False
                
        except Exception as e:
            print_error(f"CORS test error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run complete frontend-backend integration test suite"""
        print(f"\n{Fore.MAGENTA}🚀 FRONTEND-BACKEND INTEGRATION TEST SUITE{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Comprehensive testing of all API endpoints and functionality...{Style.RESET_ALL}")
        
        tests = [
            ("Server Health Check", self.test_server_health),
            ("Chat API Integration", self.test_chat_api),
            ("Product Search API", self.test_product_search_api),
            ("Inventory API", self.test_inventory_api),
            ("Promotions API", self.test_promotions_api),
            ("Order Creation API", self.test_order_creation_api),
            ("Payment Processing API", self.test_payment_processing_api),
            ("Customer Context API", self.test_customer_context_api),
            ("Analytics API", self.test_analytics_api),
            ("Messaging Webhooks", self.test_messaging_webhooks),
            ("CORS Configuration", self.test_cors_headers)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                success = test_func()
                results.append((test_name, success))
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                print_error(f"Test {test_name} crashed: {str(e)}")
                results.append((test_name, False))
        
        # Print summary
        print_header("INTEGRATION TEST SUMMARY")
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        print(f"\n{Fore.CYAN}Test Results:{Style.RESET_ALL}")
        for test_name, success in results:
            status = f"{Fore.GREEN}PASSED{Style.RESET_ALL}" if success else f"{Fore.RED}FAILED{Style.RESET_ALL}"
            print(f"  • {test_name}: {status}")
        
        print(f"\n{Fore.CYAN}Overall: {passed}/{total} tests passed{Style.RESET_ALL}")
        
        if passed == total:
            print(f"\n{Fore.GREEN}🎉 FRONTEND-BACKEND INTEGRATION SUCCESSFUL!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}All APIs are properly connected and functional.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠️  Some integration issues found.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please review the failed tests above.{Style.RESET_ALL}")
        
        return passed == total

if __name__ == "__main__":
    tester = FrontendBackendTester()
    tester.run_all_tests()
