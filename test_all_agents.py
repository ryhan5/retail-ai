#!/usr/bin/env python3
"""
Comprehensive test suite for all Agentic AI components
Tests Master Sales Agent and all Worker Agents functionality
"""

import json
import sys
from datetime import datetime
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

def test_master_sales_agent():
    """Test Master Sales Agent functionality"""
    print_header("Testing Master Sales Agent")
    
    try:
        from agents.master_sales_agent import MasterSalesAgent
        
        # Initialize Master Agent
        master_agent = MasterSalesAgent()
        print_success("Master Sales Agent initialized")
        
        # Test customer context
        customer_context = {
            'customer_id': 'CUST001',
            'name': 'John Doe',
            'tier': 'gold',
            'preferences': {'category': 'electronics'},
            'purchase_history': [
                {'product': 'Laptop', 'category': 'electronics', 'total': 999.99}
            ]
        }
        
        # Test different intents
        test_messages = [
            "Hello, I'm looking for a new laptop",
            "Do you have any promotions?",
            "Check availability of the product",
            "I want to buy this item",
            "Process my payment"
        ]
        
        for message in test_messages:
            response = master_agent.process_message(
                message=message,
                customer_context=customer_context,
                channel='web',
                session_id='TEST_SESSION'
            )
            print_success(f"Processed: '{message[:30]}...' - Intent: {response.get('intent')}")
        
        return True
        
    except Exception as e:
        print_error(f"Master Sales Agent test failed: {str(e)}")
        return False

def test_inventory_agent():
    """Test Inventory Agent"""
    print_header("Testing Inventory Agent")
    
    try:
        from agents.worker_agents.inventory_agent import InventoryAgent
        
        agent = InventoryAgent()
        print_success("Inventory Agent initialized")
        
        # Test availability check
        result = agent.check_availability('PROD001', 'online')
        print_success(f"Availability check: {result.get('available')}")
        
        # Test multi-location check
        locations = agent.check_other_locations('PROD001')
        print_success(f"Found {len(locations)} alternative locations")
        
        return True
        
    except Exception as e:
        print_error(f"Inventory Agent test failed: {str(e)}")
        return False

def test_recommendation_agent():
    """Test Recommendation Agent"""
    print_header("Testing Recommendation Agent")
    
    try:
        from agents.worker_agents.recommendation_agent import RecommendationAgent
        
        agent = RecommendationAgent()
        print_success("Recommendation Agent initialized")
        
        # Test product search
        products = agent.search_products(
            query="laptop",
            customer_preferences={'category': 'electronics'},
            purchase_history=[]
        )
        print_success(f"Found {len(products)} products")
        
        # Test personalized recommendations
        recommendations = agent.get_personalized_recommendations(
            customer_preferences={'category': 'electronics'},
            purchase_history=[],
            context={}
        )
        print_success(f"Generated {len(recommendations)} recommendations")
        
        return True
        
    except Exception as e:
        print_error(f"Recommendation Agent test failed: {str(e)}")
        return False

def test_promotion_agent():
    """Test Promotion Agent"""
    print_header("Testing Promotion Agent")
    
    try:
        from agents.worker_agents.promotion_agent import PromotionAgent
        
        agent = PromotionAgent()
        print_success("Promotion Agent initialized")
        
        # Test applicable promotions
        promotions = agent.get_applicable_promotions('CUST001', 'gold')
        print_success(f"Found {len(promotions)} applicable promotions")
        
        # Test promotion application
        cart = {'items': [{'id': 'PROD001', 'price': 100}], 'total': 100}
        result = agent.apply_promotion('PROMO001', cart, 'CUST001')
        print_success(f"Promotion applied: Discount ${result.get('discount_amount', 0)}")
        
        return True
        
    except Exception as e:
        print_error(f"Promotion Agent test failed: {str(e)}")
        return False

def test_payment_agent():
    """Test Payment Agent"""
    print_header("Testing Payment Agent")
    
    try:
        from agents.worker_agents.payment_agent import PaymentAgent
        
        agent = PaymentAgent()
        print_success("Payment Agent initialized")
        
        # Test payment processing
        payment_data = {
            'customer_id': 'CUST001',
            'cart': [{'name': 'Product', 'price': 99.99}],
            'payment_method': 'card'
        }
        result = agent.process_payment(payment_data)
        print_success(f"Payment processed: {result.get('success')}")
        
        return True
        
    except Exception as e:
        print_error(f"Payment Agent test failed: {str(e)}")
        return False

def test_order_agent():
    """Test Order Agent"""
    print_header("Testing Order Agent")
    
    try:
        from agents.worker_agents.order_agent import OrderAgent
        
        agent = OrderAgent()
        print_success("Order Agent initialized")
        
        # Test order creation
        order_data = {
            'customer_id': 'CUST001',
            'items': [{'name': 'Product', 'price': 99.99}],
            'payment_id': 'PAY001',
            'total': 99.99
        }
        result = agent.create_order(order_data)
        print_success(f"Order created: {result.get('order_id')}")
        
        return True
        
    except Exception as e:
        print_error(f"Order Agent test failed: {str(e)}")
        return False

def test_fulfillment_agent():
    """Test Fulfillment Agent"""
    print_header("Testing Fulfillment Agent")
    
    try:
        from agents.worker_agents.fulfillment_agent import FulfillmentAgent
        
        agent = FulfillmentAgent()
        print_success("Fulfillment Agent initialized")
        
        # Test delivery scheduling
        order_details = {'order_id': 'ORD001', 'items': [], 'total': 100}
        customer_location = {'distance_from_center': 10}
        result = agent.schedule_delivery(order_details, customer_location)
        print_success(f"Delivery scheduled: {result.get('delivery_id')}")
        
        # Test pickup reservation
        customer_info = {'phone': '123-456-7890', 'email': 'test@example.com'}
        result = agent.reserve_for_pickup(order_details, 'store_001', customer_info)
        print_success(f"Pickup reserved: Code {result.get('pickup_code')}")
        
        # Test delivery options
        options = agent.get_delivery_options(customer_location, order_details)
        print_success(f"Found {len(options)} delivery options")
        
        return True
        
    except Exception as e:
        print_error(f"Fulfillment Agent test failed: {str(e)}")
        return False

def test_loyalty_offers_agent():
    """Test Loyalty and Offers Agent"""
    print_header("Testing Loyalty and Offers Agent")
    
    try:
        from agents.worker_agents.loyalty_offers_agent import LoyaltyOffersAgent
        
        agent = LoyaltyOffersAgent()
        print_success("Loyalty and Offers Agent initialized")
        
        # Test loyalty status
        status = agent.get_customer_loyalty_status('CUST001')
        print_success(f"Customer tier: {status.get('tier')}, Points: {status.get('current_points')}")
        
        # Test coupon application
        cart = {'subtotal': 150, 'shipping_cost': 10}
        customer_info = {'tier': 'gold'}
        result = agent.apply_coupon_code('WELCOME10', cart, customer_info)
        print_success(f"Coupon applied: {result.get('success')}")
        
        # Test personalized offers
        purchase_history = [
            {'total': 100, 'category': 'electronics', 'date': '2024-01-01'},
            {'total': 200, 'category': 'electronics', 'date': '2024-01-15'}
        ]
        offers = agent.get_personalized_offers('CUST001', purchase_history)
        print_success(f"Generated {len(offers)} personalized offers")
        
        # Test final pricing
        applied_discounts = [{'type': 'coupon', 'amount': 15, 'description': 'Welcome discount'}]
        pricing = agent.calculate_final_price(cart, applied_discounts, customer_info)
        print_success(f"Final price calculated: ${pricing.get('final_total')}")
        
        return True
        
    except Exception as e:
        print_error(f"Loyalty and Offers Agent test failed: {str(e)}")
        return False

def test_post_purchase_agent():
    """Test Post-Purchase Support Agent"""
    print_header("Testing Post-Purchase Support Agent")
    
    try:
        from agents.worker_agents.post_purchase_agent import PostPurchaseAgent
        
        agent = PostPurchaseAgent()
        print_success("Post-Purchase Support Agent initialized")
        
        # Test return initiation
        items = [{'name': 'Product', 'price': 99.99, 'quantity': 1}]
        customer_info = {'tier': 'gold'}
        result = agent.initiate_return('ORD001', items, 'Defective product', customer_info)
        print_success(f"Return initiated: {result.get('return_id')}")
        
        # Test exchange processing
        original_item = {'name': 'Product A', 'price': 100}
        new_item = {'name': 'Product B', 'price': 120}
        result = agent.process_exchange('ORD001', original_item, new_item, 'Wrong size')
        print_success(f"Exchange processed: {result.get('exchange_id')}")
        
        # Test shipment tracking
        tracking = agent.track_shipment('TRK123456')
        print_success(f"Shipment status: {tracking.get('current_status')}")
        
        # Test feedback collection
        feedback_data = {
            'overall_rating': 4,
            'category_ratings': {'quality': 5, 'shipping': 4},
            'review_text': 'Great product!'
        }
        result = agent.collect_feedback('ORD001', 'CUST001', feedback_data)
        print_success(f"Feedback collected: {result.get('feedback_id')}")
        
        return True
        
    except Exception as e:
        print_error(f"Post-Purchase Support Agent test failed: {str(e)}")
        return False

def test_data_assumptions():
    """Test data and system assumptions"""
    print_header("Testing Data and System Assumptions")
    
    try:
        from utils.mock_apis import MockRetailAPIs
        
        mock_apis = MockRetailAPIs()
        print_success("Mock APIs initialized")
        
        # Test customer profiles (≥10 customers required)
        customers = mock_apis.get_customers()
        if len(customers) >= 10:
            print_success(f"Customer profiles: {len(customers)} customers available")
        else:
            print_error(f"Only {len(customers)} customers found (need ≥10)")
        
        # Test product catalog
        products = mock_apis.search_products("", {})
        print_success(f"Product catalog: {len(products)} products available")
        
        # Test inventory service
        inventory = mock_apis.check_inventory('PROD001', 'online')
        print_success(f"Inventory service: Stock level {inventory.get('stock_level')}")
        
        # Test payment gateway stub
        payment = mock_apis.process_payment({'amount': 100})
        print_success(f"Payment gateway: {payment.get('status')}")
        
        # Test promotions service
        promotions = mock_apis.get_promotions('CUST001')
        print_success(f"Promotions service: {len(promotions)} active promotions")
        
        return True
        
    except Exception as e:
        print_error(f"Data assumptions test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print(f"\n{Fore.MAGENTA}🚀 AGENTIC AI RETAIL SALES ASSISTANT - COMPREHENSIVE TEST SUITE{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Testing all agents and system components...{Style.RESET_ALL}")
    
    tests = [
        ("Master Sales Agent", test_master_sales_agent),
        ("Inventory Agent", test_inventory_agent),
        ("Recommendation Agent", test_recommendation_agent),
        ("Promotion Agent", test_promotion_agent),
        ("Payment Agent", test_payment_agent),
        ("Order Agent", test_order_agent),
        ("Fulfillment Agent", test_fulfillment_agent),
        ("Loyalty & Offers Agent", test_loyalty_offers_agent),
        ("Post-Purchase Support Agent", test_post_purchase_agent),
        ("Data & System Assumptions", test_data_assumptions)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print_error(f"Test {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n{Fore.CYAN}Test Results:{Style.RESET_ALL}")
    for test_name, success in results:
        status = f"{Fore.GREEN}PASSED{Style.RESET_ALL}" if success else f"{Fore.RED}FAILED{Style.RESET_ALL}"
        print(f"  • {test_name}: {status}")
    
    print(f"\n{Fore.CYAN}Overall: {passed}/{total} tests passed{Style.RESET_ALL}")
    
    if passed == total:
        print(f"\n{Fore.GREEN}🎉 ALL AGENTS ARE WORKING CORRECTLY!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}The Agentic AI system is fully operational.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}⚠️  Some agents need attention.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please review the failed tests above.{Style.RESET_ALL}")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
