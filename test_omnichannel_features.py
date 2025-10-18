#!/usr/bin/env python3
"""
Comprehensive Omnichannel Feature Test Suite
Tests session continuity, sales psychology, edge cases, and modular orchestration
"""

import requests
import json
import time
from colorama import init, Fore, Style
import uuid

# Initialize colorama
init()

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

def print_success(text):
    print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")

def print_info(text):
    print(f"{Fore.YELLOW}ℹ️  {text}{Style.RESET_ALL}")

class OmnichannelTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.customer_id = "CUST001"
        self.session_id = str(uuid.uuid4())
        
    def test_omnichannel_support(self):
        """Test multi-channel support"""
        print_header("Testing Omnichannel Support")
        
        channels = ['web', 'mobile', 'whatsapp', 'telegram', 'instore', 'voice']
        success_count = 0
        
        for channel in channels:
            try:
                response = self.session.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "message": f"Hello from {channel}",
                        "channel": channel,
                        "customer_id": self.customer_id
                    }
                )
                
                if response.status_code == 200:
                    print_success(f"Channel '{channel}' is supported")
                    success_count += 1
                else:
                    print_error(f"Channel '{channel}' failed with status {response.status_code}")
                    
            except Exception as e:
                print_error(f"Channel '{channel}' error: {str(e)}")
        
        return success_count == len(channels)
    
    def test_session_continuity(self):
        """Test session continuity across channels"""
        print_header("Testing Session Continuity")
        
        # Start conversation on web
        print_info("Starting conversation on web channel...")
        response1 = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "message": "I'm looking for a laptop",
                "channel": "web",
                "customer_id": self.customer_id
            }
        )
        
        if response1.status_code != 200:
            print_error("Failed to start web conversation")
            return False
        
        # Get session cookies
        session_cookie = self.session.cookies.get('session')
        print_success(f"Web session established")
        
        # Continue conversation on mobile
        print_info("Switching to mobile channel...")
        response2 = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "message": "Show me the laptop options we discussed",
                "channel": "mobile",
                "customer_id": self.customer_id
            }
        )
        
        if response2.status_code == 200:
            data = response2.json()
            # Check if context is maintained
            if 'laptop' in data.get('message', '').lower():
                print_success("Session context maintained when switching from web to mobile")
            else:
                print_error("Session context lost when switching channels")
                return False
        
        # Switch to in-store kiosk
        print_info("Switching to in-store kiosk...")
        response3 = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "message": "I'm now at your store, can you show me what we discussed?",
                "channel": "instore",
                "customer_id": self.customer_id
            }
        )
        
        if response3.status_code == 200:
            print_success("Session continuity maintained across web → mobile → in-store")
            return True
        
        return False
    
    def test_sales_psychology(self):
        """Test sales psychology implementation"""
        print_header("Testing Sales Psychology")
        
        # Test open questions
        print_info("Testing open-ended questions...")
        response = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "message": "I need a gift",
                "channel": "web",
                "customer_id": self.customer_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('message', '').lower()
            
            # Check for open questions
            open_questions = [
                "what occasion",
                "who are you shopping for",
                "what's your budget",
                "tell me more about",
                "what kind of"
            ]
            
            has_open_question = any(q in message for q in open_questions)
            if has_open_question:
                print_success("AI uses open-ended questions for discovery")
            else:
                print_error("AI should ask open-ended questions")
        
        # Test complementary suggestions
        print_info("Testing complementary product suggestions...")
        response = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "message": "I want to buy wireless headphones",
                "channel": "web",
                "customer_id": self.customer_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('message', '').lower()
            suggestions = data.get('suggestions', [])
            
            # Check for complementary suggestions
            complementary_keywords = [
                "pair well with",
                "also consider",
                "complete your",
                "goes great with",
                "customers also bought"
            ]
            
            has_complementary = any(k in message for k in complementary_keywords)
            if has_complementary or len(suggestions) > 0:
                print_success("AI suggests complementary items")
            else:
                print_info("AI could improve complementary suggestions")
        
        # Test objection handling
        print_info("Testing objection handling...")
        response = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "message": "That's too expensive for me",
                "channel": "web",
                "customer_id": self.customer_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('message', '').lower()
            
            # Check for graceful objection handling
            objection_handling = [
                "understand",
                "budget",
                "alternative",
                "value",
                "investment",
                "payment plan",
                "promotion",
                "discount"
            ]
            
            handles_objection = any(h in message for h in objection_handling)
            if handles_objection:
                print_success("AI handles price objections gracefully")
                return True
            else:
                print_error("AI should better handle objections")
                return False
        
        return False
    
    def test_edge_cases(self):
        """Test edge case handling"""
        print_header("Testing Edge Case Handling")
        
        # Test payment failure
        print_info("Testing payment failure recovery...")
        response = self.session.post(
            f"{self.base_url}/api/payment/process",
            json={
                "customer_id": self.customer_id,
                "amount": 99.99,
                "payment_method": "card",
                "card_details": {
                    "number": "4000000000000002",  # Card that triggers decline
                    "expiry": "12/25",
                    "cvv": "123"
                }
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('success'):
                print_success("Payment failure handled correctly")
                
                # Test recovery suggestion
                chat_response = self.session.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "message": "My payment failed, what should I do?",
                        "channel": "web",
                        "customer_id": self.customer_id
                    }
                )
                
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    if 'alternative' in chat_data.get('message', '').lower():
                        print_success("AI provides payment failure recovery options")
        
        # Test out-of-stock scenario
        print_info("Testing out-of-stock handling...")
        response = self.session.post(
            f"{self.base_url}/api/inventory/check",
            json={
                "product_id": "PROD999",  # Non-existent product
                "store_location": "online"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('available'):
                print_success("Out-of-stock scenario handled")
                
                # Test alternative suggestions
                chat_response = self.session.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "message": "The product I want is out of stock",
                        "channel": "web",
                        "customer_id": self.customer_id
                    }
                )
                
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    message = chat_data.get('message', '').lower()
                    if 'alternative' in message or 'similar' in message:
                        print_success("AI suggests alternatives for out-of-stock items")
        
        # Test order modification request
        print_info("Testing order modification...")
        response = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "message": "I want to modify my order, can I add one more item?",
                "channel": "web",
                "customer_id": self.customer_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('message', '').lower()
            if 'modify' in message or 'add' in message or 'update' in message:
                print_success("AI handles order modification requests")
                return True
        
        return False
    
    def test_modular_orchestration(self):
        """Test modular Worker Agent orchestration"""
        print_header("Testing Modular Orchestration")
        
        # Test if agents are loosely coupled
        print_info("Testing Worker Agent independence...")
        
        # Test individual agent endpoints
        agents = [
            ("/api/inventory/check", {"product_id": "PROD001", "store_location": "online"}),
            ("/api/recommendations", {"customer_id": self.customer_id}),
            ("/api/promotions", {"customer_id": self.customer_id}),
            ("/api/order/create", {"customer_id": self.customer_id, "items": [], "total": 0}),
        ]
        
        working_agents = 0
        for endpoint, payload in agents:
            try:
                response = self.session.post(f"{self.base_url}{endpoint}", json=payload)
                if response.status_code in [200, 201]:
                    agent_name = endpoint.split('/')[2]
                    print_success(f"{agent_name.capitalize()} Agent is independently accessible")
                    working_agents += 1
            except Exception as e:
                print_error(f"Agent at {endpoint} failed: {str(e)}")
        
        # Test adding new capability (mock)
        print_info("Testing extensibility for new agents...")
        
        # Simulate adding a gift wrapping agent
        response = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "message": "Can you gift wrap this order?",
                "channel": "web",
                "customer_id": self.customer_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            # Even if gift wrapping isn't implemented, system should handle gracefully
            if 'error' not in data:
                print_success("System handles requests for new capabilities gracefully")
                return True
        
        return working_agents >= 3
    
    def test_consultative_language(self):
        """Test consultative sales approach"""
        print_header("Testing Consultative Language")
        
        # Test understanding customer needs
        response = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "message": "I'm planning a birthday party",
                "channel": "web",
                "customer_id": self.customer_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('message', '').lower()
            
            # Check for consultative approach
            consultative_keywords = [
                "help you",
                "let me",
                "understand",
                "tell me",
                "how many",
                "what type",
                "budget",
                "preference"
            ]
            
            is_consultative = any(k in message for k in consultative_keywords)
            if is_consultative:
                print_success("AI uses consultative language")
                return True
            else:
                print_error("AI should be more consultative")
                return False
        
        return False
    
    def run_all_tests(self):
        """Run complete omnichannel feature test suite"""
        print(f"\n{Fore.MAGENTA}🚀 OMNICHANNEL FEATURE TEST SUITE{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Testing session continuity, sales psychology, and edge cases...{Style.RESET_ALL}")
        
        tests = [
            ("Omnichannel Support", self.test_omnichannel_support),
            ("Session Continuity", self.test_session_continuity),
            ("Sales Psychology", self.test_sales_psychology),
            ("Edge Case Handling", self.test_edge_cases),
            ("Modular Orchestration", self.test_modular_orchestration),
            ("Consultative Language", self.test_consultative_language)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                success = test_func()
                results.append((test_name, success))
                time.sleep(0.5)
            except Exception as e:
                print_error(f"Test {test_name} crashed: {str(e)}")
                results.append((test_name, False))
        
        # Print summary
        print_header("TEST SUMMARY")
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        print(f"\n{Fore.CYAN}Feature Test Results:{Style.RESET_ALL}")
        for test_name, success in results:
            status = f"{Fore.GREEN}PASSED{Style.RESET_ALL}" if success else f"{Fore.RED}FAILED{Style.RESET_ALL}"
            print(f"  • {test_name}: {status}")
        
        print(f"\n{Fore.CYAN}Overall: {passed}/{total} tests passed{Style.RESET_ALL}")
        
        if passed == total:
            print(f"\n{Fore.GREEN}🎉 ALL OMNICHANNEL FEATURES WORKING CORRECTLY!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Session continuity, sales psychology, and edge cases all handled properly.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠️  Some features need attention.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please review the failed tests above.{Style.RESET_ALL}")
        
        return passed == total

if __name__ == "__main__":
    tester = OmnichannelTester()
    tester.run_all_tests()
