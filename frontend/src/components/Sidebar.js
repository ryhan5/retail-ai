import React from 'react';
import { motion } from 'framer-motion';
import { 
  GlobeAltIcon,
  DevicePhoneMobileIcon,
  ChatBubbleLeftRightIcon,
  BuildingStorefrontIcon,
  MicrophoneIcon,
  SparklesIcon,
  TagIcon,
  ComputerDesktopIcon,
  ShoppingCartIcon
} from '@heroicons/react/24/outline';
import useStore from '../store/useStore';

const channels = [
  { id: 'web', name: 'Web Chat', icon: GlobeAltIcon, color: 'from-blue-500 to-blue-600' },
  { id: 'mobile', name: 'Mobile App', icon: DevicePhoneMobileIcon, color: 'from-green-500 to-emerald-600' },
  { id: 'whatsapp', name: 'WhatsApp', icon: ChatBubbleLeftRightIcon, color: 'from-emerald-500 to-teal-600' },
  { id: 'instore', name: 'In-Store Kiosk', icon: BuildingStorefrontIcon, color: 'from-purple-500 to-indigo-600' },
  { id: 'voice', name: 'Voice Assistant', icon: MicrophoneIcon, color: 'from-orange-500 to-amber-600' },
];

const quickActions = [
  { id: 'new-arrivals', label: 'New Arrivals', icon: SparklesIcon, message: 'Show me new arrivals' },
  { id: 'deals', label: 'Current Deals', icon: TagIcon, message: 'What promotions do you have?' },
  { id: 'electronics', label: 'Electronics', icon: ComputerDesktopIcon, message: 'Help me find electronics' },
  { id: 'cart', label: 'My Cart', icon: ShoppingCartIcon, message: 'Check my cart' },
];

const Sidebar = () => {
  const { currentChannel, setChannel, addMessage } = useStore();

  const handleChannelChange = (channelId) => {
    setChannel(channelId);
    const channel = channels.find(c => c.id === channelId);
    addMessage({
      content: `Switched to ${channel.name} mode. How can I help you today?`,
      sender: 'assistant',
      suggestions: [
        'Show me products',
        'Check current promotions',
        'Help me find something specific',
        'What\'s new?'
      ]
    });
  };

  const handleQuickAction = (action) => {
    addMessage({
      content: action.message,
      sender: 'user'
    });
  };

  return (
    <motion.div
      initial={{ x: -280 }}
      animate={{ x: 0 }}
      className="w-80 h-full bg-gradient-to-b from-white/90 to-gray-50/90 backdrop-blur-2xl border-r border-gray-200 text-gray-800 flex flex-col shadow-xl"
    >
      {/* Header */}
      <div className="p-6 pb-4 border-b border-gray-100">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="flex items-center space-x-4"
        >
          <div className="relative">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-600 flex items-center justify-center text-white shadow-lg">
              <SparklesIcon className="w-8 h-8" />
            </div>
            <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
          </div>
          <div>
            <h2 className="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
              AI Sales Assistant
            </h2>
            <p className="text-sm text-gray-500 mt-1">Multi-channel commerce hub</p>
          </div>
        </motion.div>
      </div>

      {/* Channel Selector */}
      <div className="p-6 pt-4 border-b border-gray-100">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">
            Communication Channels
          </h3>
          <div className="space-y-2">
            {channels.map((channel, index) => {
              const Icon = channel.icon;
              const isActive = currentChannel === channel.id;
              
              return (
                <motion.button
                  key={channel.id}
                  initial={{ opacity: 0, x: -18 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4 + index * 0.08 }}
                  whileHover={{ scale: 1.01, x: 8 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => handleChannelChange(channel.id)}
                  className={`w-full flex items-center justify-between px-4 py-3.5 rounded-xl transition-all duration-200 relative group ${
                    isActive 
                      ? 'bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 shadow-sm' 
                      : 'hover:bg-gray-50 hover:border-gray-200 border border-transparent'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${
                      isActive 
                        ? 'bg-gradient-to-r ' + channel.color + ' text-white' 
                        : channel.color.split(' ')[0] + ' bg-opacity-10 text-' + channel.color.split(' ')[0].replace('from-', '')
                    }`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className={`font-medium ${isActive ? 'text-gray-900' : 'text-gray-700'}`}>
                      {channel.name}
                    </span>
                  </div>
                  {isActive && (
                    <motion.div
                      layoutId="activeChannel"
                      className="w-2 h-2 bg-purple-500 rounded-full"
                    />
                  )}
                </motion.button>
              );
            })}
          </div>
        </motion.div>
      </div>

      {/* Quick Actions */}
      <div className="flex-1 p-6 pt-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">
            Quick Actions
          </h3>
          <div className="space-y-3">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              
              return (
                <motion.button
                  key={action.id}
                  initial={{ opacity: 0, x: -16 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.9 + index * 0.08 }}
                  whileHover={{ scale: 1.02, y: -2 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => handleQuickAction(action)}
                  className="w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl bg-white text-gray-700 border border-gray-200 hover:border-purple-300 hover:shadow-md transition-all duration-200 text-left group"
                >
                  <div className="p-2 bg-purple-100 rounded-lg group-hover:bg-purple-200 transition-colors">
                    <Icon className="w-5 h-5 text-purple-600" />
                  </div>
                  <span className="text-sm font-medium">
                    {action.label}
                  </span>
                </motion.button>
              );
            })}
          </div>
        </motion.div>
      </div>

      {/* Footer */}
      <div className="p-6 pt-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2 }}
          className="bg-gradient-to-r from-purple-50/70 to-blue-50/70 border border-purple-100 rounded-2xl p-4"
        >
          <div className="flex items-center space-x-2 mb-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm font-semibold text-gray-800">AI Assistant Active</span>
          </div>
          <p className="text-xs text-gray-600 leading-relaxed">
            Ready to guide customers across web, messaging, and in-store touchpoints with seamless product discovery.
          </p>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Sidebar;