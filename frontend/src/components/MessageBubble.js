import React from 'react';
import { motion } from 'framer-motion';
import { 
  UserIcon,
  SparklesIcon,
  ShoppingBagIcon,
  TagIcon,
  StarIcon,
  HeartIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { FaWhatsapp, FaTelegram } from 'react-icons/fa';
import useStore from '../store/useStore';
import { openMessagingApp } from '../config/channels';
import toast from 'react-hot-toast';

const MessageBubble = ({ message, onSuggestionClick, index }) => {
  const { addToCart } = useStore();
  const isUser = message.sender === 'user';

  const formatMessageContent = (content) => {
    // Format markdown-like content
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/(₹\d+\.?\d*)/g, '<span class="text-green-600 font-semibold">$1</span>')
      .replace(/(✅|❌|🎉|📱|🛍️|💰|📦)/g, '<span class="text-lg">$1</span>');
  };

  const handleProductClick = (product) => {
    addToCart(product);
    onSuggestionClick(`Tell me more about ${product.name}`);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ 
        duration: 0.4, 
        delay: index * 0.08,
        type: "spring",
        stiffness: 260,
        damping: 20
      }}
      className={`flex items-start space-x-4 ${isUser ? 'flex-row-reverse space-x-reverse' : ''} mb-4`}
    >
      {/* Enhanced Avatar */}
      <motion.div
        whileHover={{ scale: 1.15, rotate: 5 }}
        whileTap={{ scale: 0.95 }}
        className={`relative w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg ${
          isUser 
            ? 'bg-gradient-to-br from-primary-400 via-primary-500 to-primary-600 text-white' 
            : 'bg-gradient-to-br from-secondary-400 via-accent-500 to-secondary-600 text-white'
        }`}
      >
        {isUser ? (
          <UserIcon className="w-6 h-6" />
        ) : (
          <motion.div
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          >
            <SparklesIcon className="w-6 h-6" />
          </motion.div>
        )}
        
        {/* Status indicator for AI */}
        {!isUser && (
          <motion.div
            animate={{ scale: [1, 1.3, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white flex items-center justify-center"
          >
            <CheckCircleIcon className="w-2.5 h-2.5 text-white" />
          </motion.div>
        )}
      </motion.div>

      {/* Enhanced Message Content */}
      <div className={`max-w-2xl ${isUser ? 'text-right' : 'text-left'}`}>
        {/* Message timestamp */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className={`text-xs text-neutral-500 mb-1 font-medium ${isUser ? 'text-right' : 'text-left'}`}
        >
          {isUser ? 'You' : 'AI Assistant'} • just now
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.01, y: -1 }}
          className={`relative px-6 py-4 shadow-xl backdrop-blur-sm border ${
            isUser
              ? 'bg-gradient-to-br from-primary-500 to-primary-600 text-white border-primary-400 ml-auto rounded-3xl rounded-tr-lg'
              : 'bg-white/95 text-neutral-800 border-neutral-200/50 rounded-3xl rounded-tl-lg'
          }`}
        >
          {/* Message bubble tail */}
          <div className={`absolute top-0 ${
            isUser 
              ? 'right-0 w-4 h-4 bg-gradient-to-br from-primary-500 to-primary-600 transform rotate-45 translate-x-2 translate-y-2'
              : 'left-0 w-4 h-4 bg-white/95 border-l border-t border-neutral-200/50 transform rotate-45 -translate-x-2 translate-y-2'
          }`} />
          
          <div 
            className={`relative z-10 font-medium leading-relaxed ${
              isUser ? 'text-white' : 'text-neutral-800'
            }`}
            style={{
              fontFamily: 'Manrope, sans-serif',
              fontSize: '15px',
              lineHeight: '1.6'
            }}
            dangerouslySetInnerHTML={{ __html: formatMessageContent(message.content) }}
          />
          
          {/* Message actions for AI responses */}
          {!isUser && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5 }}
              className="absolute top-2 right-2 flex items-center space-x-1"
            >
              <motion.button
                whileHover={{ scale: 1.2 }}
                whileTap={{ scale: 0.9 }}
                className="p-1.5 text-neutral-400 hover:text-accent-500 transition-colors rounded-full hover:bg-neutral-100"
              >
                <HeartIcon className="w-4 h-4" />
              </motion.button>
            </motion.div>
          )}
        </motion.div>

        {/* Enhanced Suggestions */}
        {message.suggestions && message.suggestions.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className={`mt-4 flex flex-wrap gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}
          >
            {message.suggestions.map((suggestion, idx) => (
              <motion.button
                key={idx}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1 * idx }}
                whileHover={{ scale: 1.05, y: -3, boxShadow: "0 10px 30px -10px rgba(168, 85, 247, 0.3)" }}
                whileTap={{ scale: 0.98 }}
                onClick={() => onSuggestionClick(suggestion)}
                className="px-4 py-2.5 bg-gradient-to-r from-white to-neutral-50 border-2 border-primary-200 rounded-2xl text-sm font-medium text-primary-700 hover:bg-gradient-to-r hover:from-primary-50 hover:to-primary-100 hover:border-primary-300 hover:text-primary-800 transition-all duration-300 shadow-lg backdrop-blur-sm"
                style={{
                  fontFamily: 'Manrope, sans-serif'
                }}
              >
                <span className="flex items-center space-x-1">
                  <span>💭</span>
                  <span>{suggestion}</span>
                </span>
              </motion.button>
            ))}
          </motion.div>
        )}

        {/* Enhanced Products Grid */}
        {message.products && message.products.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4"
          >
            {message.products.map((product, idx) => (
              <motion.div
                key={product.id}
                initial={{ opacity: 0, scale: 0.9, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                transition={{ delay: 0.6 + idx * 0.1 }}
                whileHover={{ 
                  scale: 1.03, 
                  y: -8,
                  boxShadow: "0 20px 40px -15px rgba(168, 85, 247, 0.2)"
                }}
                onClick={() => handleProductClick(product)}
                className="group relative bg-gradient-to-br from-white via-white to-neutral-50/50 rounded-2xl p-5 border-2 border-neutral-200/50 hover:border-primary-300 shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer backdrop-blur-sm"
              >
                {/* Product Badge */}
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.8 + idx * 0.1 }}
                  className="absolute -top-2 -right-2 w-8 h-8 bg-gradient-to-br from-secondary-400 to-accent-500 rounded-full flex items-center justify-center shadow-lg"
                >
                  <ShoppingBagIcon className="w-4 h-4 text-white" />
                </motion.div>

                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h4 className="font-display font-bold text-neutral-900 group-hover:text-primary-700 transition-colors text-lg leading-tight">
                      {product.name}
                    </h4>
                    {product.description && (
                      <p className="text-sm text-neutral-600 mt-1 line-clamp-2 font-medium">
                        {product.description}
                      </p>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center justify-between mb-4">
                  <div className="flex flex-col">
                    <span className="text-2xl font-display font-bold text-gradient bg-gradient-to-r from-secondary-600 to-primary-600 bg-clip-text text-transparent">
                      ₹{product.price}
                    </span>
                    {product.originalPrice && product.originalPrice > product.price && (
                      <span className="text-sm text-neutral-500 line-through font-medium">
                        ₹{product.originalPrice}
                      </span>
                    )}
                  </div>
                  
                  {product.rating && (
                    <div className="flex items-center space-x-1 bg-amber-50 px-3 py-1.5 rounded-full border border-amber-200">
                      <StarIcon className="w-4 h-4 text-amber-500 fill-current" />
                      <span className="text-sm font-semibold text-amber-700">{product.rating}</span>
                    </div>
                  )}
                </div>
                
                {product.features && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {product.features.slice(0, 3).map((feature, featureIdx) => (
                      <motion.span 
                        key={featureIdx}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 1 + featureIdx * 0.1 }}
                        className="px-3 py-1.5 bg-gradient-to-r from-primary-50 to-secondary-50 text-xs font-semibold text-primary-700 rounded-full border border-primary-200/50"
                      >
                        ✨ {feature}
                      </motion.span>
                    ))}
                  </div>
                )}

                {/* Add to cart action */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 1.2 + idx * 0.1 }}
                  className="pt-3 border-t border-neutral-200/50"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-medium text-neutral-600">
                      {product.inStock !== false ? '✅ In Stock' : '❌ Out of Stock'}
                    </span>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      className="px-4 py-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white text-sm font-bold rounded-xl hover:shadow-lg transition-all duration-200"
                    >
                      Add to Cart
                    </motion.button>
                  </div>
                </motion.div>

                {/* Hover overlay */}
                <motion.div
                  initial={{ opacity: 0 }}
                  whileHover={{ opacity: 1 }}
                  className="absolute inset-0 bg-gradient-to-br from-primary-500/10 via-transparent to-secondary-500/10 rounded-2xl pointer-events-none"
                />
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Promotions */}
        {message.promotions && message.promotions.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="mt-4 space-y-3"
          >
            {message.promotions.map((promo, idx) => (
              <motion.div
                key={promo.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7 + idx * 0.1 }}
                className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl p-4 text-white"
              >
                <div className="flex items-center space-x-2 mb-2">
                  <TagIcon className="w-5 h-5" />
                  <h4 className="font-semibold">{promo.title}</h4>
                </div>
                <p className="text-sm opacity-90">{promo.description}</p>
                {promo.valid_until && (
                  <p className="text-xs opacity-75 mt-1">
                    Valid until: {promo.valid_until}
                  </p>
                )}
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Cart Summary */}
        {message.cart && message.cart.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="mt-4 bg-gray-50 rounded-xl p-4 border border-gray-200"
          >
            <div className="flex items-center space-x-2 mb-3">
              <ShoppingBagIcon className="w-5 h-5 text-gray-600" />
              <h4 className="font-semibold text-gray-900">Your Cart</h4>
            </div>
            
            <div className="space-y-2">
              {message.cart.map((item, idx) => (
                <div key={idx} className="flex justify-between items-center">
                  <span className="text-sm text-gray-700">
                    {item.name} {item.quantity && `(${item.quantity})`}
                  </span>
                  <span className="font-semibold text-green-600">
                    ₹{(item.price * (item.quantity || 1)).toFixed(2)}
                  </span>
                </div>
              ))}
              
              <div className="border-t pt-2 mt-2">
                <div className="flex justify-between items-center font-bold">
                  <span>Total:</span>
                  <span className="text-green-600">
                    ₹{message.cart.reduce((total, item) => 
                      total + (item.price * (item.quantity || 1)), 0
                    ).toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Quick Channel Actions for AI Messages */}
        {!isUser && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="mt-4 flex flex-wrap gap-2"
          >
            <motion.button
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                toast.success('Opening WhatsApp... Continue shopping there!', {
                  icon: '💬',
                  duration: 3000,
                });
                openMessagingApp('whatsapp');
              }}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-xl shadow-md hover:shadow-lg transition-all text-sm font-semibold"
            >
              <FaWhatsapp className="w-4 h-4" />
              <span>Shop on WhatsApp</span>
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                toast.success('Opening Telegram... Continue shopping there!', {
                  icon: '✈️',
                  duration: 3000,
                });
                openMessagingApp('telegram');
              }}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-sky-500 to-sky-600 hover:from-sky-600 hover:to-sky-700 text-white rounded-xl shadow-md hover:shadow-lg transition-all text-sm font-semibold"
            >
              <FaTelegram className="w-4 h-4" />
              <span>Shop on Telegram</span>
            </motion.button>
          </motion.div>
        )}

        {/* Timestamp */}
        <div className={`mt-2 text-xs text-gray-500 ${isUser ? 'text-right' : 'text-left'}`}>
          {new Date(message.timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </div>
      </div>
    </motion.div>
  );
};

export default MessageBubble;
