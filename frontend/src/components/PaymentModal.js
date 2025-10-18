import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  CreditCardIcon,
  XMarkIcon,
  CheckCircleIcon,
  ShieldCheckIcon,
  LockClosedIcon
} from '@heroicons/react/24/outline';
import { FaCcVisa, FaCcMastercard, FaCcAmex, FaCcDiscover, FaPaypal, FaGooglePay } from 'react-icons/fa';
import toast from 'react-hot-toast';
import useStore from '../store/useStore';

const PaymentModal = ({ onClose, onPaymentSuccess }) => {
  const { cart, getCartTotal, customerId } = useStore();
  const [paymentMethod, setPaymentMethod] = useState('card');
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentComplete, setPaymentComplete] = useState(false);
  
  const [cardDetails, setCardDetails] = useState({
    cardNumber: '',
    cardName: '',
    expiryDate: '',
    cvv: '',
    saveCard: false
  });

  const formatCardNumber = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = (matches && matches[0]) || '';
    const parts = [];

    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }

    if (parts.length) {
      return parts.join(' ');
    } else {
      return value;
    }
  };

  const formatExpiryDate = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    if (v.length >= 2) {
      return v.slice(0, 2) + '/' + v.slice(2, 4);
    }
    return v;
  };

  const handleCardInputChange = (field, value) => {
    let formattedValue = value;
    
    if (field === 'cardNumber') {
      formattedValue = formatCardNumber(value);
      if (formattedValue.replace(/\s/g, '').length > 16) return;
    } else if (field === 'expiryDate') {
      formattedValue = formatExpiryDate(value);
      if (formattedValue.replace(/\//g, '').length > 4) return;
    } else if (field === 'cvv') {
      formattedValue = value.replace(/[^0-9]/g, '');
      if (formattedValue.length > 4) return;
    }
    
    setCardDetails(prev => ({ ...prev, [field]: formattedValue }));
  };

  const getCardType = (cardNumber) => {
    const number = cardNumber.replace(/\s/g, '');
    if (/^4/.test(number)) return { name: 'Visa', icon: FaCcVisa };
    if (/^5[1-5]/.test(number)) return { name: 'Mastercard', icon: FaCcMastercard };
    if (/^3[47]/.test(number)) return { name: 'Amex', icon: FaCcAmex };
    if (/^6(?:011|5)/.test(number)) return { name: 'Discover', icon: FaCcDiscover };
    return { name: 'Card', icon: CreditCardIcon };
  };

  const handlePayment = async () => {
    // Validation
    if (paymentMethod === 'card') {
      if (!cardDetails.cardNumber || !cardDetails.cardName || !cardDetails.expiryDate || !cardDetails.cvv) {
        toast.error('Please fill in all card details');
        return;
      }
      
      const cardNum = cardDetails.cardNumber.replace(/\s/g, '');
      if (cardNum.length < 13 || cardNum.length > 19) {
        toast.error('Invalid card number');
        return;
      }
      
      if (cardDetails.cvv.length < 3) {
        toast.error('Invalid CVV');
        return;
      }
    }

    setIsProcessing(true);

    // Simulate payment processing
    toast.promise(
      new Promise((resolve) => setTimeout(resolve, 2500)),
      {
        loading: 'Processing payment...',
        success: 'Payment successful!',
        error: 'Payment failed',
      }
    ).then(() => {
      setIsProcessing(false);
      setPaymentComplete(true);
      
      // Call success callback after showing success animation
      setTimeout(() => {
        onPaymentSuccess({
          orderId: `ORD-${Date.now()}`,
          amount: getCartTotal(),
          paymentMethod,
          customerId,
          items: cart
        });
      }, 2000);
    });
  };

  if (paymentComplete) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="bg-white rounded-3xl p-12 shadow-2xl max-w-md w-full mx-4 text-center"
          onClick={(e) => e.stopPropagation()}
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1, rotate: 360 }}
            transition={{ type: "spring", stiffness: 200, damping: 15 }}
            className="w-24 h-24 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6"
          >
            <CheckCircleIcon className="w-16 h-16 text-white" />
          </motion.div>
          
          <h3 className="text-3xl font-bold text-gray-900 mb-3">
            Payment Successful!
          </h3>
          <p className="text-gray-600 mb-6">
            Your order has been placed successfully. You'll receive a confirmation email shortly.
          </p>
          
          <div className="bg-gray-50 rounded-xl p-4 mb-6">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">Amount Paid</span>
              <span className="font-bold text-gray-900">₹{getCartTotal().toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Order ID</span>
              <span className="font-mono text-gray-900">ORD-{Date.now()}</span>
            </div>
          </div>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onClose}
            className="w-full px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-xl font-semibold shadow-lg"
          >
            Done
          </motion.button>
        </motion.div>
      </motion.div>
    );
  }

  const CardIcon = getCardType(cardDetails.cardNumber).icon;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, y: 50 }}
        animate={{ scale: 1, y: 0 }}
        className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 bg-gradient-to-r from-purple-50 to-blue-50">
          <div>
            <h3 className="text-2xl font-bold text-gray-900">Secure Checkout</h3>
            <div className="flex items-center gap-2 mt-1">
              <LockClosedIcon className="w-4 h-4 text-green-600" />
              <span className="text-sm text-gray-600">Encrypted & Secure</span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white rounded-full transition-colors"
          >
            <XMarkIcon className="w-6 h-6 text-gray-600" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 max-h-[calc(90vh-100px)] overflow-y-auto">
          {/* Left Side - Payment Form */}
          <div className="p-6 border-r border-gray-200">
            {/* Payment Method Selection */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                Payment Method
              </label>
              <div className="grid grid-cols-3 gap-3">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setPaymentMethod('card')}
                  className={`p-3 rounded-xl border-2 transition-all ${
                    paymentMethod === 'card'
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <CreditCardIcon className="w-6 h-6 mx-auto mb-1 text-gray-700" />
                  <span className="text-xs font-medium">Card</span>
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setPaymentMethod('paypal')}
                  className={`p-3 rounded-xl border-2 transition-all ${
                    paymentMethod === 'paypal'
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <FaPaypal className="w-6 h-6 mx-auto mb-1 text-blue-600" />
                  <span className="text-xs font-medium">PayPal</span>
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setPaymentMethod('gpay')}
                  className={`p-3 rounded-xl border-2 transition-all ${
                    paymentMethod === 'gpay'
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <FaGooglePay className="w-6 h-6 mx-auto mb-1 text-gray-700" />
                  <span className="text-xs font-medium">GPay</span>
                </motion.button>
              </div>
            </div>

            {/* Card Details Form */}
            {paymentMethod === 'card' && (
              <div className="space-y-4">
                {/* Card Number */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Card Number
                  </label>
                  <div className="relative">
                    <input
                      type="text"
                      value={cardDetails.cardNumber}
                      onChange={(e) => handleCardInputChange('cardNumber', e.target.value)}
                      placeholder="1234 5678 9012 3456"
                      className="w-full px-4 py-3 pr-12 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-0 transition-colors"
                    />
                    <CardIcon className="absolute right-4 top-1/2 -translate-y-1/2 w-8 h-8 text-gray-400" />
                  </div>
                </div>

                {/* Card Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Cardholder Name
                  </label>
                  <input
                    type="text"
                    value={cardDetails.cardName}
                    onChange={(e) => handleCardInputChange('cardName', e.target.value)}
                    placeholder="John Doe"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-0 transition-colors uppercase"
                  />
                </div>

                {/* Expiry & CVV */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Expiry Date
                    </label>
                    <input
                      type="text"
                      value={cardDetails.expiryDate}
                      onChange={(e) => handleCardInputChange('expiryDate', e.target.value)}
                      placeholder="MM/YY"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-0 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      CVV
                    </label>
                    <input
                      type="password"
                      value={cardDetails.cvv}
                      onChange={(e) => handleCardInputChange('cvv', e.target.value)}
                      placeholder="123"
                      maxLength="4"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-0 transition-colors"
                    />
                  </div>
                </div>

                {/* Save Card */}
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={cardDetails.saveCard}
                    onChange={(e) => setCardDetails(prev => ({ ...prev, saveCard: e.target.checked }))}
                    className="w-4 h-4 text-purple-600 rounded focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-700">Save card for future purchases</span>
                </label>
              </div>
            )}

            {/* PayPal */}
            {paymentMethod === 'paypal' && (
              <div className="text-center py-8">
                <FaPaypal className="w-20 h-20 mx-auto mb-4 text-blue-600" />
                <p className="text-gray-600 mb-4">You'll be redirected to PayPal to complete your payment</p>
                <div className="flex items-center justify-center gap-2 text-sm text-gray-500">
                  <ShieldCheckIcon className="w-4 h-4" />
                  <span>Secure payment via PayPal</span>
                </div>
              </div>
            )}

            {/* Google Pay */}
            {paymentMethod === 'gpay' && (
              <div className="text-center py-8">
                <FaGooglePay className="w-20 h-20 mx-auto mb-4 text-gray-700" />
                <p className="text-gray-600 mb-4">Pay quickly with your Google account</p>
                <div className="flex items-center justify-center gap-2 text-sm text-gray-500">
                  <ShieldCheckIcon className="w-4 h-4" />
                  <span>Secure payment via Google Pay</span>
                </div>
              </div>
            )}
          </div>

          {/* Right Side - Order Summary */}
          <div className="p-6 bg-gray-50">
            <h4 className="font-semibold text-gray-900 mb-4">Order Summary</h4>
            
            {/* Cart Items */}
            <div className="space-y-3 mb-6 max-h-48 overflow-y-auto">
              {cart.map((item, index) => (
                <div key={index} className="flex justify-between text-sm">
                  <span className="text-gray-700">
                    {item.name} <span className="text-gray-500">×{item.quantity}</span>
                  </span>
                  <span className="font-semibold text-gray-900">
                    ₹{(item.price * item.quantity).toFixed(2)}
                  </span>
                </div>
              ))}
            </div>

            {/* Pricing Details */}
            <div className="border-t border-gray-200 pt-4 space-y-2 mb-6">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Subtotal</span>
                <span className="font-medium text-gray-900">₹{getCartTotal().toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Shipping</span>
                <span className="font-medium text-green-600">Free</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Tax</span>
                <span className="font-medium text-gray-900">₹{(getCartTotal() * 0.1).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-lg font-bold pt-2 border-t border-gray-200">
                <span className="text-gray-900">Total</span>
                <span className="text-gradient bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                  ₹{(getCartTotal() * 1.1).toFixed(2)}
                </span>
              </div>
            </div>

            {/* Trust Badges */}
            <div className="grid grid-cols-2 gap-2 mb-4">
              <div className="flex items-center gap-2 text-xs text-gray-600">
                <ShieldCheckIcon className="w-4 h-4 text-green-600" />
                <span>Secure Checkout</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-600">
                <LockClosedIcon className="w-4 h-4 text-blue-600" />
                <span>SSL Encrypted</span>
              </div>
            </div>

            {/* Accepted Cards */}
            <div className="flex items-center gap-2 justify-center mb-4">
              <FaCcVisa className="w-8 h-8 text-gray-400" />
              <FaCcMastercard className="w-8 h-8 text-gray-400" />
              <FaCcAmex className="w-8 h-8 text-gray-400" />
              <FaCcDiscover className="w-8 h-8 text-gray-400" />
            </div>

            {/* Pay Button */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handlePayment}
              disabled={isProcessing}
              className={`w-full px-6 py-4 rounded-xl font-bold text-lg transition-all flex items-center justify-center gap-2 ${
                isProcessing
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg hover:shadow-xl'
              }`}
            >
              {isProcessing ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                  />
                  Processing...
                </>
              ) : (
                <>
                  <LockClosedIcon className="w-5 h-5" />
                  Pay ₹{(getCartTotal() * 1.1).toFixed(2)}
                </>
              )}
            </motion.button>
            
            <p className="text-xs text-center text-gray-500 mt-3">
              By completing your purchase you agree to our Terms of Service
            </p>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default PaymentModal;
