import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  PaperAirplaneIcon,
  SparklesIcon,
  MicrophoneIcon,
  PhotoIcon,
  CreditCardIcon
} from '@heroicons/react/24/outline';
import useStore from '../store/useStore';
import { chatAPI } from '../services/api';
import toast from 'react-hot-toast';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import VoiceRecorder from './VoiceRecorder';
import ImageUploader from './ImageUploader';
import PaymentModal from './PaymentModal';

const ChatInterface = () => {
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isAutoScrollEnabled, setIsAutoScrollEnabled] = useState(true);
  const [showVoiceRecorder, setShowVoiceRecorder] = useState(false);
  const [showImageUploader, setShowImageUploader] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const messagesContainerRef = useRef(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  
  const { 
    messages, 
    addMessage, 
    isTyping, 
    setTyping, 
    currentChannel, 
    customerId,
    setSelectedProducts,
    setCurrentPromotions,
    cart,
    clearCart
  } = useStore();

  const scrollToBottom = (behavior = 'smooth') => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  };

  useEffect(() => {
    if (isAutoScrollEnabled) {
      scrollToBottom(messages.length < 3 ? 'auto' : 'smooth');
    }
  }, [messages, isTyping, isAutoScrollEnabled]);

  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = container;
      const distanceFromBottom = scrollHeight - (scrollTop + clientHeight);
      const nearBottomThreshold = 160;
      const shouldEnableAutoScroll = distanceFromBottom <= nearBottomThreshold;
      setIsAutoScrollEnabled(shouldEnableAutoScroll);
    };

    container.addEventListener('scroll', handleScroll, { passive: true });
    // Run once to set initial state
    handleScroll();

    return () => container.removeEventListener('scroll', handleScroll);
  }, []);

  const handleSendMessage = async (messageText = null) => {
    const message = messageText || inputValue.trim();
    if (!message || isLoading) return;

    // Add user message
    addMessage({
      content: message,
      sender: 'user'
    });

    // Clear input
    setInputValue('');
    setIsLoading(true);
    setTyping(true);

    try {
      // Send to backend
      const response = await chatAPI.sendMessage(message, currentChannel, customerId);
      
      // Add assistant response
      addMessage({
        content: response.message,
        sender: 'assistant',
        suggestions: response.suggestions,
        products: response.products,
        promotions: response.promotions,
        cart: response.cart,
        intent: response.intent
      });

      // Update store with products and promotions if provided
      if (response.products) {
        setSelectedProducts(response.products);
      }
      if (response.promotions) {
        setCurrentPromotions(response.promotions);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      
      // Provide intelligent fallback response
      let fallbackMessage = "I apologize, but I'm having trouble connecting to my backend services right now. ";
      
      // Analyze the message to provide contextual fallback
      const lowerMessage = message.toLowerCase();
      if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
        fallbackMessage += "Hello! I'm your AI shopping assistant. Once we're reconnected, I can help you find products, check deals, and more!";
      } else if (lowerMessage.includes('product') || lowerMessage.includes('find') || lowerMessage.includes('search')) {
        fallbackMessage += "I'd love to help you find products! Please check that the backend server is running (python app.py) and try again.";
      } else if (lowerMessage.includes('cart') || lowerMessage.includes('checkout')) {
        fallbackMessage += "I can help with your cart once we're reconnected. Make sure the backend is running!";
      } else {
        fallbackMessage += "Please ensure the Flask backend is running (python app.py) and try your request again.";
      }
      
      toast.error('Backend connection failed. Is the server running?');
      
      addMessage({
        content: fallbackMessage,
        sender: 'assistant',
        suggestions: [
          'Check if backend is running',
          'Try again',
          'View products page',
          'Contact support'
        ]
      });
    } finally {
      setIsLoading(false);
      setTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    handleSendMessage(suggestion);
  };

  const handleVoiceTranscript = (transcript) => {
    setInputValue(transcript);
    setTimeout(() => handleSendMessage(transcript), 500);
  };

  const handleImageSelect = (images, previews) => {
    // In a real implementation, you would:
    // 1. Upload images to your server
    // 2. Get image URLs
    // 3. Send to AI for visual search/analysis
    
    const message = `I've shared ${images.length} image(s) with you. Can you help me find similar products?`;
    addMessage({
      content: message,
      sender: 'user',
      images: previews // Store preview URLs
    });
    
    // Simulate AI response
    setTimeout(() => {
      addMessage({
        content: `I can see your image${images.length > 1 ? 's' : ''}! Let me analyze ${images.length > 1 ? 'them' : 'it'} and find similar products for you. This is a demo - in production, I would use image recognition to search our catalog!`,
        sender: 'assistant',
        suggestions: ['Show similar products', 'Search by brand', 'Filter by price']
      });
    }, 1000);
  };

  const handlePaymentSuccess = (orderDetails) => {
    addMessage({
      content: `🎉 Payment successful! Your order ${orderDetails.orderId} has been placed. Total amount: ₹${orderDetails.amount.toFixed(2)}. You'll receive a confirmation email shortly.`,
      sender: 'assistant'
    });
    
    // Clear cart after successful payment
    clearCart();
    
    toast.success('Order placed successfully! Check your email for confirmation.');
    setShowPaymentModal(false);
  };

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-white">
      {/* Messages Area */}
      <div
        ref={messagesContainerRef}
        className="flex-1 min-h-0 overflow-y-auto px-6 py-6 space-y-4 bg-gray-50"
      >
        {messages.length === 0 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="text-center py-16 max-w-2xl mx-auto"
          >
            <div className="w-16 h-16 mx-auto bg-gray-900 rounded-xl flex items-center justify-center mb-6">
              <SparklesIcon className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">
              Welcome! How can I help you today?
            </h3>
            <p className="text-base text-gray-600 max-w-md mx-auto leading-relaxed mb-8">
              Ask me about products, check deals, or get personalized recommendations.
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {[
                'Find products',
                'Check deals', 
                'Track orders',
                'Get recommendations'
              ].map((item, idx) => (
                <span
                  key={idx}
                  className="px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm text-gray-700"
                >
                  {item}
                </span>
              ))}
            </div>
          </motion.div>
        )}

        <AnimatePresence>
          {messages.map((message, index) => (
            <MessageBubble
              key={message.id}
              message={message}
              onSuggestionClick={handleSuggestionClick}
              index={index}
            />
          ))}
        </AnimatePresence>
        
        {/* Enhanced Typing Indicator */}
        <AnimatePresence>
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.9 }}
              className="flex items-start space-x-4"
            >
              <motion.div
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="w-12 h-12 bg-gradient-to-br from-secondary-500 to-accent-500 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg"
              >
                <SparklesIcon className="w-6 h-6 text-white" />
              </motion.div>
              <div className="bg-white/90 backdrop-blur-sm border border-neutral-200/50 rounded-2xl px-6 py-4 shadow-lg">
                <div className="flex items-center space-x-2">
                  <TypingIndicator />
                  <span className="text-sm font-medium text-neutral-600 ml-2">AI is thinking...</span>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        
        <div ref={messagesEndRef} />

        {!isAutoScrollEnabled && messages.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="sticky bottom-4 flex justify-center"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                scrollToBottom('smooth');
                setIsAutoScrollEnabled(true);
              }}
              className="px-5 py-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white text-sm font-semibold rounded-full shadow-lg shadow-primary-500/30"
            >
              View latest messages
            </motion.button>
          </motion.div>
        )}
      </div>

      {/* Input Area */}
      <motion.div
        initial={{ y: 40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.25 }}
        className="px-6 py-4 bg-white border-t border-gray-200"
      >
        <div className="max-w-5xl mx-auto">
          <div className="flex items-end space-x-3">
            {/* Input Field */}
            <div className="flex-1 relative">
              <div className="relative bg-gray-50 rounded-xl border border-gray-300 focus-within:border-gray-900 transition-all">
                <textarea
                  ref={inputRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me anything..."
                  className="w-full px-4 py-3 pr-20 bg-transparent border-0 focus:ring-0 resize-none text-gray-900 placeholder-gray-500 rounded-xl"
                  rows="1"
                  style={{
                    minHeight: '48px',
                    maxHeight: '120px',
                    fontSize: '15px',
                    lineHeight: '1.5'
                  }}
                  disabled={isLoading}
                />
                
                {/* Input Actions */}
                <div className="absolute right-2 bottom-2 flex items-center space-x-1">
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => setShowVoiceRecorder(true)}
                    className="p-2 text-neutral-400 hover:text-purple-600 transition-colors rounded-full hover:bg-purple-50"
                    title="Voice message"
                  >
                    <MicrophoneIcon className="w-5 h-5" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => setShowImageUploader(true)}
                    className="p-2 text-neutral-400 hover:text-blue-600 transition-colors rounded-full hover:bg-blue-50"
                    title="Upload image"
                  >
                    <PhotoIcon className="w-5 h-5" />
                  </motion.button>
                </div>
                
                {/* Character count */}
                {inputValue.length > 0 && (
                  <div className="absolute bottom-1 left-4 text-xs text-neutral-400">
                    <span className={inputValue.length > 500 ? 'text-accent-500 font-medium' : 'text-neutral-400'}>
                      {inputValue.length}/500
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Send Button */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleSendMessage()}
              disabled={!inputValue.trim() || isLoading}
              className={`w-12 h-12 rounded-lg flex items-center justify-center transition-all ${
                inputValue.trim() && !isLoading
                  ? 'bg-gray-900 text-white hover:bg-gray-800'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
            >
              {isLoading ? (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                />
              ) : (
                <PaperAirplaneIcon className="w-5 h-5" />
              )}
            </motion.button>
          </div>
          
          {/* Quick Suggestions */}
          {!inputValue && messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 flex flex-wrap gap-2 justify-center"
            >
              {[
                'Show trending products',
                'What deals are available?',
                'Track my order'
              ].map((suggestion, idx) => (
                <motion.button
                  key={suggestion}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => handleSendMessage(suggestion)}
                  className="px-4 py-2 text-sm bg-white border border-gray-200 text-gray-700 rounded-lg hover:border-gray-900 transition-all"
                >
                  {suggestion}
                </motion.button>
              ))}
            </motion.div>
          )}

          {/* Checkout Button */}
          {cart.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4"
            >
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setShowPaymentModal(true)}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-900 text-white rounded-lg font-medium text-sm hover:bg-gray-800 transition-all"
              >
                <CreditCardIcon className="w-5 h-5" />
                Checkout ({cart.length} {cart.length === 1 ? 'item' : 'items'})
              </motion.button>
            </motion.div>
          )}
        </div>
      </motion.div>

      {/* Modals */}
      <AnimatePresence>
        {showVoiceRecorder && (
          <VoiceRecorder
            onTranscript={handleVoiceTranscript}
            onClose={() => setShowVoiceRecorder(false)}
          />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {showImageUploader && (
          <ImageUploader
            onImageSelect={handleImageSelect}
            onClose={() => setShowImageUploader(false)}
          />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {showPaymentModal && (
          <PaymentModal
            onClose={() => setShowPaymentModal(false)}
            onPaymentSuccess={handlePaymentSuccess}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default ChatInterface;
