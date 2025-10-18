import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  SparklesIcon,
  ShoppingBagIcon,
  XMarkIcon,
  ComputerDesktopIcon,
  DevicePhoneMobileIcon,
  BuildingStorefrontIcon,
  MicrophoneIcon,
  CheckCircleIcon,
  ArrowsRightLeftIcon
} from '@heroicons/react/24/outline';
import { FaWhatsapp, FaTelegram } from 'react-icons/fa';
import toast from 'react-hot-toast';
import useStore from '../store/useStore';
import { openMessagingApp } from '../config/channels';
import ChatInterface from '../components/ChatInterface';
import ProductShowcase from '../components/ProductShowcase';
import ShoppingCart from '../components/ShoppingCart';
import WelcomeScreen from '../components/WelcomeScreen';

const ChatPage = () => {
  const { 
    initializeCustomer,
    currentChannel,
    setChannel,
    cart,
    getCartItemCount
  } = useStore();

  const [showSidebar, setShowSidebar] = useState(false);
  const [showChannelSelector, setShowChannelSelector] = useState(false);
  const showWelcome = false; // Always show chat interface

  useEffect(() => {
    initializeCustomer();
  }, [initializeCustomer]);

  const channels = [
    { 
      id: 'web', 
      name: 'Web Chat', 
      icon: ComputerDesktopIcon,
      color: 'from-blue-500 to-blue-600',
      description: 'Desktop browser experience'
    },
    { 
      id: 'mobile', 
      name: 'Mobile App', 
      icon: DevicePhoneMobileIcon,
      color: 'from-purple-500 to-purple-600',
      description: 'On-the-go shopping'
    },
    { 
      id: 'whatsapp', 
      name: 'WhatsApp', 
      icon: FaWhatsapp,
      color: 'from-green-500 to-green-600',
      description: 'Chat on WhatsApp'
    },
    { 
      id: 'telegram', 
      name: 'Telegram', 
      icon: FaTelegram,
      color: 'from-sky-500 to-sky-600',
      description: 'Telegram messaging'
    },
    { 
      id: 'in-store', 
      name: 'In-Store Kiosk', 
      icon: BuildingStorefrontIcon,
      color: 'from-orange-500 to-orange-600',
      description: 'Physical store terminal'
    },
    { 
      id: 'voice', 
      name: 'Voice Assistant', 
      icon: MicrophoneIcon,
      color: 'from-pink-500 to-pink-600',
      description: 'Voice-enabled shopping'
    }
  ];

  const handleChannelSwitch = (channelId) => {
    const channel = channels.find(c => c.id === channelId);
    
    // Handle external app redirects for WhatsApp and Telegram
    if (channelId === 'whatsapp') {
      toast.success('Opening WhatsApp... Continue shopping there!', {
        icon: '💬',
        duration: 4000,
      });
      
      openMessagingApp(channelId);
      setShowChannelSelector(false);
      return;
    }
    
    if (channelId === 'telegram') {
      toast.success('Opening Telegram... Continue shopping there!', {
        icon: '✈️',
        duration: 4000,
      });
      
      openMessagingApp(channelId);
      setShowChannelSelector(false);
      return;
    }
    
    // For other channels, switch within the app
    setChannel(channelId);
    setShowChannelSelector(false);
    
    // Show success notification
    toast.success(`Switched to ${channel?.name || 'new channel'}! Your cart and conversation are preserved.`, {
      icon: '🔄',
      duration: 3000,
    });
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-50 via-violet-50/30 to-blue-50/30">
      {/* Modern Header */}
      <div className="absolute top-0 left-0 right-0 z-20 bg-white/80 backdrop-blur-xl border-b border-slate-200/50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                <SparklesIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900 font-heading">AI Shopping Assistant</h1>
                <p className="text-xs text-slate-500">Powered by Gemini AI • Omnichannel</p>
              </div>
            </div>
            
            {/* Channel Selector & Actions */}
            <div className="flex items-center gap-3">
              {/* Current Channel Display */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowChannelSelector(!showChannelSelector)}
                className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 rounded-xl transition-all shadow-lg text-white"
              >
                {(() => {
                  const currentCh = channels.find(c => c.id === currentChannel);
                  const Icon = currentCh?.icon || ComputerDesktopIcon;
                  return <Icon className="w-5 h-5" />;
                })()}
                <span className="text-sm font-semibold hidden sm:inline">
                  {channels.find(c => c.id === currentChannel)?.name || 'Web Chat'}
                </span>
                <ArrowsRightLeftIcon className="w-4 h-4" />
              </motion.button>
              
              {/* Cart Badge */}
              <button
                onClick={() => setShowSidebar(!showSidebar)}
                className="relative p-2 hover:bg-slate-100 rounded-lg transition-colors lg:hidden"
              >
                <ShoppingBagIcon className="w-6 h-6 text-slate-600" />
                {getCartItemCount() > 0 && (
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-bold">
                    {getCartItemCount()}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Channel Selector Modal */}
      <AnimatePresence>
        {showChannelSelector && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowChannelSelector(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full p-8"
            >
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-slate-900 font-heading">Switch Channel</h2>
                  <p className="text-sm text-slate-600 mt-1">Your cart and conversation continue seamlessly</p>
                </div>
                <button
                  onClick={() => setShowChannelSelector(false)}
                  className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                >
                  <XMarkIcon className="w-6 h-6 text-slate-600" />
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {channels.map((channel) => {
                  const Icon = channel.icon;
                  const isActive = currentChannel === channel.id;
                  
                  return (
                    <motion.button
                      key={channel.id}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => handleChannelSwitch(channel.id)}
                      className={`relative p-6 rounded-xl border-2 transition-all text-left ${
                        isActive
                          ? 'border-purple-500 bg-gradient-to-br from-purple-50 to-blue-50 shadow-lg'
                          : 'border-slate-200 hover:border-purple-300 hover:shadow-md'
                      }`}
                    >
                      {isActive && (
                        <div className="absolute top-3 right-3">
                          <CheckCircleIcon className="w-6 h-6 text-green-500" />
                        </div>
                      )}
                      
                      <div className={`w-12 h-12 bg-gradient-to-br ${channel.color} rounded-xl flex items-center justify-center mb-4 shadow-lg`}>
                        <Icon className="w-6 h-6 text-white" />
                      </div>
                      
                      <h3 className="text-lg font-bold text-slate-900 mb-1">
                        {channel.name}
                        {(channel.id === 'whatsapp' || channel.id === 'telegram') && (
                          <span className="ml-2 text-xs font-normal text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                            Opens App
                          </span>
                        )}
                      </h3>
                      <p className="text-sm text-slate-600">{channel.description}</p>
                      
                      {isActive && (
                        <div className="mt-3 text-xs font-medium text-green-600">
                          ✓ Currently Active
                        </div>
                      )}
                    </motion.button>
                  );
                })}
              </div>

              <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <div className="flex items-start gap-3">
                  <SparklesIcon className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-semibold text-blue-900 mb-1">Session Continuity</h4>
                    <p className="text-xs text-blue-700">
                      Your shopping cart, conversation history, and preferences are automatically preserved when you switch channels. 
                      Start on web, continue on mobile, or complete your purchase in-store!
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden pt-20">
        {/* Chat Section */}
        <div className="flex-1 flex flex-col min-h-0 relative">
          {/* Background Decoration */}
          <div className="absolute inset-0 overflow-hidden pointer-events-none">
            <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300/20 rounded-full blur-3xl animate-blob"></div>
            <div className="absolute bottom-20 right-10 w-72 h-72 bg-blue-300/20 rounded-full blur-3xl animate-blob animation-delay-2000"></div>
          </div>

          {/* Quick Channel Selector Bar */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="relative z-10 px-6 py-3 bg-white/60 backdrop-blur-md border-b border-slate-200/50"
          >
            <div className="flex items-center gap-2 overflow-x-auto scrollbar-hide">
              <span className="text-xs font-semibold text-slate-600 whitespace-nowrap mr-2">Quick Switch:</span>
              {channels.map((channel) => {
                const Icon = channel.icon;
                const isActive = currentChannel === channel.id;
                return (
                  <motion.button
                    key={channel.id}
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleChannelSwitch(channel.id)}
                    className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-all whitespace-nowrap text-sm font-medium ${
                      isActive
                        ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg'
                        : 'bg-white/80 text-slate-700 hover:bg-slate-100 border border-slate-200'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="hidden sm:inline">{channel.name}</span>
                  </motion.button>
                );
              })}
            </div>
          </motion.div>

          {/* Chat Content */}
          <div className="relative z-10 flex-1 flex flex-col min-h-0">
            <AnimatePresence mode="wait">
              {showWelcome ? (
                <motion.div
                  key="welcome"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{ duration: 0.4 }}
                  className="flex-1 min-h-0"
                >
                  <WelcomeScreen />
                </motion.div>
              ) : (
                <motion.div
                  key="chat"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.4 }}
                  className="flex-1 flex flex-col min-h-0"
                >
                  <ChatInterface />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Right Sidebar - Product Showcase & Cart */}
        <AnimatePresence>
          {(showSidebar || window.innerWidth >= 1024) && (
            <motion.div
              initial={{ x: 400, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 400, opacity: 0 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className="w-full lg:w-96 bg-white border-l border-slate-200 shadow-2xl flex flex-col fixed lg:relative right-0 top-0 h-full z-30"
            >
              {/* Sidebar Header */}
              <div className="p-6 border-b border-slate-200 bg-gradient-to-r from-purple-50 to-blue-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <ShoppingBagIcon className="w-5 h-5 text-purple-600" />
                    <h2 className="text-lg font-bold text-slate-900 font-heading">Shopping</h2>
                  </div>
                  <button
                    onClick={() => setShowSidebar(false)}
                    className="lg:hidden p-2 hover:bg-white rounded-lg transition-colors"
                  >
                    <XMarkIcon className="w-5 h-5 text-slate-600" />
                  </button>
                </div>
              </div>

              {/* Product Showcase */}
              <div className="flex-1 overflow-y-auto">
                <ProductShowcase />
              </div>

              {/* Shopping Cart */}
              <div className="border-t border-slate-200 bg-slate-50/50">
                <ShoppingCart />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default ChatPage;
