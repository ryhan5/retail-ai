import React from 'react';
import { motion } from 'framer-motion';
import { 
  ShoppingBagIcon,
  MagnifyingGlassIcon,
  HeartIcon,
  TruckIcon,
  PercentBadgeIcon,
  SparklesIcon,
  ChatBubbleLeftRightIcon
} from '@heroicons/react/24/outline';
import useStore from '../store/useStore';

const features = [
  {
    icon: MagnifyingGlassIcon,
    title: 'Smart Search',
    description: 'Find products with natural language',
    color: 'text-blue-500',
    bgColor: 'bg-blue-50'
  },
  {
    icon: HeartIcon,
    title: 'Personalized',
    description: 'Recommendations based on your preferences',
    color: 'text-pink-500',
    bgColor: 'bg-pink-50'
  },
  {
    icon: TruckIcon,
    title: 'Real-time Inventory',
    description: 'Check availability across all locations',
    color: 'text-green-500',
    bgColor: 'bg-green-50'
  },
  {
    icon: PercentBadgeIcon,
    title: 'Best Deals',
    description: 'Automatic promotion application',
    color: 'text-purple-500',
    bgColor: 'bg-purple-50'
  }
];

const quickStarters = [
  'I\'m looking for wireless headphones',
  'Show me the latest electronics',
  'What promotions do you have today?',
  'Help me find a gift under $100',
  'Check availability at downtown store',
  'I need help with my order'
];

const WelcomeScreen = () => {
  const { addMessage } = useStore();

  const handleQuickStart = (message) => {
    addMessage({
      content: message,
      sender: 'user'
    });
  };

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-4xl w-full">
        {/* Main Welcome */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <motion.div
            animate={{ 
              rotate: [0, 5, -5, 0],
              scale: [1, 1.05, 1]
            }}
            transition={{ 
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-3xl mb-6 shadow-glow"
          >
            <ShoppingBagIcon className="w-12 h-12 text-white" />
          </motion.div>
          
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="text-4xl md:text-5xl font-bold gradient-text mb-4"
          >
            Welcome to Your AI Shopping Assistant
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed"
          >
            I'm here to help you discover products, find the best deals, and make your shopping experience seamless across all channels.
          </motion.p>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.8 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
        >
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8 + index * 0.1, duration: 0.6 }}
                whileHover={{ 
                  scale: 1.05,
                  y: -5,
                  transition: { duration: 0.2 }
                }}
                className="glass-card p-6 rounded-2xl text-center group cursor-pointer"
              >
                <div className={`inline-flex items-center justify-center w-16 h-16 ${feature.bgColor} rounded-2xl mb-4 group-hover:scale-110 transition-transform duration-200`}>
                  <Icon className={`w-8 h-8 ${feature.color}`} />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-gray-600">
                  {feature.description}
                </p>
              </motion.div>
            );
          })}
        </motion.div>

        {/* Quick Starters */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2, duration: 0.8 }}
          className="text-center"
        >
          <div className="flex items-center justify-center space-x-2 mb-6">
            <ChatBubbleLeftRightIcon className="w-6 h-6 text-primary-500" />
            <h2 className="text-2xl font-bold text-gray-900">
              Try asking me something like:
            </h2>
            <SparklesIcon className="w-6 h-6 text-secondary-500" />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-w-4xl mx-auto">
            {quickStarters.map((starter, index) => (
              <motion.button
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 1.4 + index * 0.1, duration: 0.4 }}
                whileHover={{ 
                  scale: 1.05,
                  boxShadow: "0 10px 25px rgba(59, 130, 246, 0.2)"
                }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleQuickStart(starter)}
                className="p-4 bg-white/80 backdrop-blur-sm border border-white/20 rounded-xl text-left hover:bg-white/90 transition-all duration-200 group"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full group-hover:scale-150 transition-transform duration-200"></div>
                  <span className="text-gray-700 group-hover:text-gray-900 transition-colors duration-200">
                    "{starter}"
                  </span>
                </div>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2, duration: 0.8 }}
          className="text-center mt-12"
        >
          <motion.div
            animate={{ 
              y: [0, -5, 0],
            }}
            transition={{ 
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="inline-flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-primary-500 to-secondary-500 text-white rounded-full font-medium shadow-glow"
          >
            <ChatBubbleLeftRightIcon className="w-5 h-5" />
            <span>Start chatting below to begin your shopping journey!</span>
            <SparklesIcon className="w-5 h-5" />
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default WelcomeScreen;
