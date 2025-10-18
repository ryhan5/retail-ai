import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  ShoppingCartIcon,
  TrashIcon,
  PlusIcon,
  MinusIcon,
  ArrowLeftIcon,
  CreditCardIcon,
  TruckIcon,
  ShieldCheckIcon,
  TagIcon
} from '@heroicons/react/24/outline';
import useStore from '../store/useStore';
import toast from 'react-hot-toast';

const CartPage = () => {
  const { 
    cart, 
    removeFromCart, 
    updateCartQuantity, 
    clearCart, 
    getCartTotal, 
    getCartItemCount 
  } = useStore();
  
  const [promoCode, setPromoCode] = useState('');
  const [appliedPromo, setAppliedPromo] = useState(null);
  const [isCheckingOut, setIsCheckingOut] = useState(false);

  const cartTotal = getCartTotal();
  const itemCount = getCartItemCount();
  const tax = cartTotal * 0.08;
  const shipping = cartTotal > 75 ? 0 : 9.99;
  const discount = appliedPromo ? cartTotal * 0.1 : 0;
  const finalTotal = cartTotal + tax + shipping - discount;

  const handleQuantityChange = (productId, newQuantity) => {
    if (newQuantity === 0) {
      removeFromCart(productId);
      toast.success('Item removed from cart');
    } else {
      updateCartQuantity(productId, newQuantity);
    }
  };

  const handleApplyPromo = () => {
    if (promoCode.toUpperCase() === 'SAVE10') {
      setAppliedPromo('SAVE10');
      toast.success('Promo code applied! 10% discount');
    } else {
      toast.error('Invalid promo code');
    }
  };

  const handleCheckout = () => {
    setIsCheckingOut(true);
    setTimeout(() => {
      toast.success('Order placed successfully!');
      clearCart();
      setIsCheckingOut(false);
    }, 2000);
  };

  if (cart.length === 0 && !isCheckingOut) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
        <div className="text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200 }}
            className="w-32 h-32 bg-slate-200 rounded-full flex items-center justify-center mx-auto mb-6"
          >
            <ShoppingCartIcon className="w-16 h-16 text-slate-400" />
          </motion.div>
          <h2 className="text-3xl font-bold text-slate-900 mb-4">Your cart is empty</h2>
          <p className="text-slate-600 mb-8">Looks like you haven't added anything to your cart yet.</p>
          <Link to="/products">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-3 bg-primary-600 text-white rounded-xl font-semibold hover:bg-primary-700 transition-colors"
            >
              Start Shopping
            </motion.button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-slate-900 font-heading">
                Shopping Cart
              </h1>
              <p className="text-slate-600 mt-2">
                {itemCount} {itemCount === 1 ? 'item' : 'items'} in your cart
              </p>
            </div>
            <Link to="/products">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center gap-2 px-6 py-3 bg-white border-2 border-primary-200 text-primary-700 rounded-xl font-semibold hover:bg-primary-50 transition-colors"
              >
                <ArrowLeftIcon className="w-5 h-5" />
                Continue Shopping
              </motion.button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            <AnimatePresence>
              {cart.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-xl p-6 shadow-sm border border-slate-200/60"
                >
                  <div className="flex gap-6">
                    {/* Product Image */}
                    <div className="w-32 h-32 bg-slate-200 rounded-lg flex items-center justify-center">
                      <ShoppingCartIcon className="w-12 h-12 text-slate-400" />
                    </div>

                    {/* Product Details */}
                    <div className="flex-1">
                      <div className="flex justify-between mb-2">
                        <h3 className="text-lg font-semibold text-slate-900">
                          {item.name}
                        </h3>
                        <button
                          onClick={() => removeFromCart(item.id)}
                          className="p-2 text-slate-400 hover:text-error-500 transition-colors"
                        >
                          <TrashIcon className="w-5 h-5" />
                        </button>
                      </div>
                      
                      {item.features && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          {item.features.slice(0, 3).map((feature, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-slate-100 text-slate-600 text-xs rounded-full"
                            >
                              {feature}
                            </span>
                          ))}
                        </div>
                      )}

                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <button
                            onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                            className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center hover:bg-slate-200 transition-colors"
                          >
                            <MinusIcon className="w-4 h-4 text-slate-500" />
                          </button>
                          <span className="font-medium text-slate-900 w-12 text-center">
                            {item.quantity}
                          </span>
                          <button
                            onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                            className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center hover:bg-slate-200 transition-colors"
                          >
                            <PlusIcon className="w-4 h-4 text-slate-500" />
                          </button>
                        </div>
                        
                        <div className="text-right">
                          <div className="text-2xl font-bold text-slate-900">
                            ₹{(item.price * item.quantity).toFixed(2)}
                          </div>
                          <div className="text-sm text-slate-500">
                            ₹{item.price} each
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          {/* Order Summary Column */}
          <div className="space-y-6">
            {/* Promo Code */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <h3 className="font-semibold text-slate-900 mb-4 flex items-center gap-2">
                <TagIcon className="w-5 h-5 text-slate-500" />
                Promo Code
              </h3>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Enter code"
                  value={promoCode}
                  onChange={(e) => setPromoCode(e.target.value)}
                  className="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
                <button
                  onClick={handleApplyPromo}
                  className="px-6 py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
                >
                  Apply
                </button>
              </div>
            </div>

            {/* Order Details */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <h3 className="font-semibold text-slate-900 mb-4">Order Summary</h3>

              <div className="space-y-3 mb-6">
                <div className="flex justify-between text-slate-600">
                  <span>Subtotal ({itemCount} items)</span>
                  <span>₹{cartTotal.toFixed(2)}</span>
                </div>
                {appliedPromo && (
                  <div className="flex justify-between text-success-600">
                    <span>Discount (10%)</span>
                    <span>-₹{discount.toFixed(2)}</span>
                  </div>
                )}
                
                <div className="flex justify-between text-slate-600">
                  <span>Tax (8%)</span>
                  <span>₹{tax.toFixed(2)}</span>
                </div>
                
                <div className="flex justify-between text-slate-600">
                  <span>Shipping</span>
                  <span className={shipping === 0 ? 'text-success-600' : ''}>
                    {shipping === 0 ? 'FREE' : `₹${shipping.toFixed(2)}`}
                  </span>
                </div>
                
                {cartTotal < 75 && (
                  <div className="px-3 py-2 bg-warning-50 text-warning-700 rounded-lg text-sm">
                    Add ₹{(75 - cartTotal).toFixed(2)} more for free shipping!
                  </div>
                )}
              </div>
              
              <div className="border-t pt-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-lg font-semibold text-slate-900">Total</span>
                  <span className="text-2xl font-bold text-slate-900">
                    ₹{finalTotal.toFixed(2)}
                  </span>
                </div>
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                disabled={isCheckingOut}
                className="w-full py-4 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-xl font-semibold hover:from-primary-700 hover:to-primary-800 transition-all flex items-center justify-center gap-2"
              >
                {isCheckingOut ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    <CreditCardIcon className="w-5 h-5" />
                    Proceed to Checkout
                  </>
                )}
              </motion.button>
            </div>

            {/* Trust Badges */}
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <ShieldCheckIcon className="w-6 h-6 text-success-600" />
                  <div>
                    <div className="font-medium text-slate-900">Secure Checkout</div>
                    <div className="text-sm text-slate-600">SSL encrypted payment</div>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <TruckIcon className="w-6 h-6 text-primary-600" />
                  <div>
                    <div className="font-medium text-slate-900">Fast Delivery</div>
                    <div className="text-sm text-slate-600">2-3 business days</div>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <CreditCardIcon className="w-6 h-6 text-secondary-600" />
                  <div>
                    <div className="font-medium text-slate-900">Multiple Payment Options</div>
                    <div className="text-sm text-slate-600">Credit card, PayPal, and more</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
