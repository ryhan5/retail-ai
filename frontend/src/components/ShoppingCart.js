import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShoppingCartIcon,
  TrashIcon,
  PlusIcon,
  MinusIcon,
  CreditCardIcon,
  TagIcon
} from '@heroicons/react/24/outline';
import useStore from '../store/useStore';
import { orderAPI } from '../services/api';
import toast from 'react-hot-toast';

const ShoppingCart = () => {
  const { 
    cart, 
    removeFromCart, 
    updateCartQuantity, 
    clearCart, 
    getCartTotal, 
    getCartItemCount,
    addMessage,
    customerId
  } = useStore();

  const cartTotal = getCartTotal();
  const itemCount = getCartItemCount();

  const handleQuantityChange = (productId, newQuantity) => {
    if (newQuantity === 0) {
      removeFromCart(productId);
      toast.success('Item removed from cart');
    } else {
      updateCartQuantity(productId, newQuantity);
    }
  };

  const handleCheckout = async () => {
    if (cart.length === 0) {
      toast.error('Your cart is empty');
      return;
    }

    addMessage({
      content: 'I\'d like to proceed to checkout',
      sender: 'user'
    });

    toast.success('Proceeding to checkout...');
  };

  const handleClearCart = () => {
    clearCart();
    toast.success('Cart cleared');
  };

  return (
    <div className="h-80 flex flex-col bg-white/20 backdrop-blur-sm">
      {/* Header */}
      <div className="p-4 border-b border-white/20">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <ShoppingCartIcon className="w-5 h-5 text-primary-500" />
            <h2 className="text-lg font-semibold text-gray-900">Shopping Cart</h2>
            {itemCount > 0 && (
              <span className="bg-primary-500 text-white text-xs px-2 py-1 rounded-full">
                {itemCount}
              </span>
            )}
          </div>
          
          {cart.length > 0 && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleClearCart}
              className="text-red-500 hover:text-red-700 text-sm"
            >
              Clear All
            </motion.button>
          )}
        </div>
      </div>

      {/* Cart Items */}
      <div className="flex-1 overflow-y-auto p-4 scrollbar-hide">
        <AnimatePresence>
          {cart.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="text-center py-8"
            >
              <ShoppingCartIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500 text-sm mb-2">Your cart is empty</p>
              <p className="text-gray-400 text-xs">
                Add products from recommendations or search
              </p>
            </motion.div>
          ) : (
            <div className="space-y-3">
              {cart.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-lg p-3 shadow-sm border border-gray-100"
                >
                  <div className="flex items-start space-x-3">
                    {/* Product Image Placeholder */}
                    <div className="w-12 h-12 bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg flex items-center justify-center flex-shrink-0">
                      <ShoppingCartIcon className="w-6 h-6 text-gray-400" />
                    </div>

                    {/* Product Info */}
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-gray-900 truncate">
                        {item.name}
                      </h4>
                      <p className="text-sm font-semibold text-green-600">
                        ₹{item.price}
                      </p>
                      
                      {/* Quantity Controls */}
                      <div className="flex items-center space-x-2 mt-2">
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                          className="w-6 h-6 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200 transition-colors"
                        >
                          <MinusIcon className="w-3 h-3 text-gray-600" />
                        </motion.button>
                        
                        <span className="text-sm font-medium px-2">
                          {item.quantity}
                        </span>
                        
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                          className="w-6 h-6 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200 transition-colors"
                        >
                          <PlusIcon className="w-3 h-3 text-gray-600" />
                        </motion.button>
                        
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          onClick={() => removeFromCart(item.id)}
                          className="ml-2 p-1 text-red-500 hover:text-red-700 transition-colors"
                        >
                          <TrashIcon className="w-4 h-4" />
                        </motion.button>
                      </div>
                    </div>

                    {/* Item Total */}
                    <div className="text-right">
                      <p className="text-sm font-semibold text-gray-900">
                        ₹{(item.price * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </AnimatePresence>
      </div>

      {/* Cart Footer */}
      {cart.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 border-t border-white/20 bg-white/30"
        >
          {/* Subtotal */}
          <div className="flex justify-between items-center mb-3">
            <span className="text-sm text-gray-600">Subtotal ({itemCount} items)</span>
            <span className="text-lg font-bold text-gray-900">
              ₹{cartTotal.toFixed(2)}
            </span>
          </div>

          {/* Estimated Tax & Shipping */}
          <div className="space-y-1 mb-3 text-xs text-gray-500">
            <div className="flex justify-between">
              <span>Est. Tax (8%)</span>
              <span>₹{(cartTotal * 0.08).toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span>Shipping</span>
              <span>{cartTotal > 75 ? 'FREE' : '₹9.99'}</span>
            </div>
          </div>

          {/* Total */}
          <div className="flex justify-between items-center mb-4 pt-2 border-t border-gray-200">
            <span className="font-semibold text-gray-900">Total</span>
            <span className="text-xl font-bold text-green-600">
              ₹{(cartTotal + (cartTotal * 0.08) + (cartTotal > 75 ? 0 : 9.99)).toFixed(2)}
            </span>
          </div>

          {/* Action Buttons */}
          <div className="space-y-2">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleCheckout}
              className="w-full bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-semibold py-3 px-4 rounded-lg hover:shadow-lg transition-all duration-200 flex items-center justify-center space-x-2"
            >
              <CreditCardIcon className="w-5 h-5" />
              <span>Proceed to Checkout</span>
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => addMessage({
                content: 'Apply a promo code to my cart',
                sender: 'user'
              })}
              className="w-full bg-white/50 hover:bg-white/70 border border-white/20 text-gray-700 font-medium py-2 px-4 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2"
            >
              <TagIcon className="w-4 h-4" />
              <span>Apply Promo Code</span>
            </motion.button>
          </div>

          {/* Free Shipping Banner */}
          {cartTotal < 75 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="mt-3 p-2 bg-blue-50 border border-blue-200 rounded-lg"
            >
              <p className="text-xs text-blue-700 text-center">
                Add ₹{(75 - cartTotal).toFixed(2)} more for FREE shipping! 🚚
              </p>
            </motion.div>
          )}
        </motion.div>
      )}
    </div>
  );
};

export default ShoppingCart;
