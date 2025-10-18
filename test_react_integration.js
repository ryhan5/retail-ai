// React Frontend Integration Test
// This JavaScript can be run in the browser console to test frontend functionality

console.log('🚀 Testing React Frontend Integration...');

// Test 1: Check if React app is loaded
function testReactApp() {
    console.log('\n📱 Testing React App Loading...');
    const root = document.getElementById('root');
    if (root && root.children.length > 0) {
        console.log('✅ React app is loaded and rendered');
        return true;
    } else {
        console.log('❌ React app not found or not rendered');
        return false;
    }
}

// Test 2: Check Zustand store
function testZustandStore() {
    console.log('\n🗄️ Testing Zustand State Management...');
    try {
        // Access the store through window if available
        if (window.useStore) {
            const store = window.useStore.getState();
            console.log('✅ Zustand store accessible');
            console.log('Store state:', Object.keys(store));
            return true;
        } else {
            console.log('⚠️ Zustand store not directly accessible from window');
            return false;
        }
    } catch (error) {
        console.log('❌ Zustand store test failed:', error.message);
        return false;
    }
}

// Test 3: Check API connectivity
async function testAPIConnectivity() {
    console.log('\n🌐 Testing API Connectivity...');
    try {
        const response = await fetch('http://localhost:5000/api/analytics/dashboard');
        if (response.ok) {
            console.log('✅ Backend API is accessible');
            const data = await response.json();
            console.log('API Response keys:', Object.keys(data));
            return true;
        } else {
            console.log('❌ Backend API returned error:', response.status);
            return false;
        }
    } catch (error) {
        console.log('❌ API connectivity test failed:', error.message);
        return false;
    }
}

// Test 4: Check routing
function testReactRouter() {
    console.log('\n🛣️ Testing React Router...');
    try {
        const currentPath = window.location.pathname;
        console.log('Current path:', currentPath);
        
        // Check if router elements exist
        const navLinks = document.querySelectorAll('[href*="/"]');
        if (navLinks.length > 0) {
            console.log('✅ React Router navigation found');
            console.log('Navigation links:', navLinks.length);
            return true;
        } else {
            console.log('⚠️ No navigation links found');
            return false;
        }
    } catch (error) {
        console.log('❌ React Router test failed:', error.message);
        return false;
    }
}

// Test 5: Check Tailwind CSS
function testTailwindCSS() {
    console.log('\n🎨 Testing Tailwind CSS...');
    try {
        const elements = document.querySelectorAll('[class*="bg-"], [class*="text-"], [class*="flex"]');
        if (elements.length > 0) {
            console.log('✅ Tailwind CSS classes found');
            console.log('Styled elements:', elements.length);
            return true;
        } else {
            console.log('❌ No Tailwind CSS classes found');
            return false;
        }
    } catch (error) {
        console.log('❌ Tailwind CSS test failed:', error.message);
        return false;
    }
}

// Test 6: Check Framer Motion animations
function testFramerMotion() {
    console.log('\n✨ Testing Framer Motion Animations...');
    try {
        const motionElements = document.querySelectorAll('[style*="transform"], [style*="opacity"]');
        if (motionElements.length > 0) {
            console.log('✅ Animated elements found');
            console.log('Motion elements:', motionElements.length);
            return true;
        } else {
            console.log('⚠️ No animated elements currently visible');
            return false;
        }
    } catch (error) {
        console.log('❌ Framer Motion test failed:', error.message);
        return false;
    }
}

// Test 7: Test chat functionality (simulation)
async function testChatFunctionality() {
    console.log('\n💬 Testing Chat Functionality...');
    try {
        const testMessage = 'Hello, I need help finding products';
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: testMessage,
                channel: 'web',
                customer_id: 'CUST001'
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Chat API working');
            console.log('AI Response:', data.message?.substring(0, 100) + '...');
            return true;
        } else {
            console.log('❌ Chat API failed:', response.status);
            return false;
        }
    } catch (error) {
        console.log('❌ Chat functionality test failed:', error.message);
        return false;
    }
}

// Test 8: Test shopping cart simulation
function testShoppingCart() {
    console.log('\n🛒 Testing Shopping Cart Functionality...');
    try {
        // Look for cart-related elements
        const cartElements = document.querySelectorAll('[class*="cart"], [data-testid*="cart"]');
        const cartCounters = document.querySelectorAll('[class*="badge"], [class*="counter"]');
        
        if (cartElements.length > 0 || cartCounters.length > 0) {
            console.log('✅ Shopping cart elements found');
            console.log('Cart elements:', cartElements.length);
            return true;
        } else {
            console.log('⚠️ Shopping cart elements not visible');
            return false;
        }
    } catch (error) {
        console.log('❌ Shopping cart test failed:', error.message);
        return false;
    }
}

// Run all tests
async function runAllTests() {
    console.log('🧪 Running Complete Frontend Integration Test Suite...');
    console.log('============================================================');
    
    const tests = [
        { name: 'React App Loading', test: testReactApp },
        { name: 'Zustand Store', test: testZustandStore },
        { name: 'API Connectivity', test: testAPIConnectivity },
        { name: 'React Router', test: testReactRouter },
        { name: 'Tailwind CSS', test: testTailwindCSS },
        { name: 'Framer Motion', test: testFramerMotion },
        { name: 'Chat Functionality', test: testChatFunctionality },
        { name: 'Shopping Cart', test: testShoppingCart }
    ];
    
    const results = [];
    
    for (const { name, test } of tests) {
        try {
            const result = await test();
            results.push({ name, success: result });
        } catch (error) {
            console.error(`Test ${name} crashed:`, error);
            results.push({ name, success: false });
        }
    }
    
    // Summary
    console.log('\n📊 FRONTEND INTEGRATION TEST SUMMARY');
    console.log('=====================================');
    
    const passed = results.filter(r => r.success).length;
    const total = results.length;
    
    results.forEach(result => {
        const status = result.success ? '✅ PASSED' : '❌ FAILED';
        console.log(`${result.name}: ${status}`);
    });
    
    console.log(`\nOverall: ${passed}/${total} tests passed`);
    
    if (passed === total) {
        console.log('\n🎉 ALL FRONTEND TESTS PASSED!');
        console.log('The React frontend is fully integrated and functional.');
    } else {
        console.log('\n⚠️ Some frontend issues detected.');
        console.log('Please check the failed tests above.');
    }
    
    return passed === total;
}

// Auto-run tests when script is loaded
runAllTests();

// Export for manual testing
window.frontendTest = {
    runAllTests,
    testReactApp,
    testZustandStore,
    testAPIConnectivity,
    testReactRouter,
    testTailwindCSS,
    testFramerMotion,
    testChatFunctionality,
    testShoppingCart
};
