import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  HomeIcon,
  ShoppingBagIcon,
  ShoppingCartIcon,
  ChatBubbleLeftRightIcon,
  UserCircleIcon,
  SunIcon,
  MoonIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import useStore from '../store/useStore';

const Navbar = () => {
  const location = useLocation();
  const { getCartItemCount, darkMode, toggleDarkMode } = useStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const cartItemCount = getCartItemCount();

  const navItems = [
    { path: '/', name: 'Home', icon: HomeIcon },
    { path: '/products', name: 'Products', icon: ShoppingBagIcon },
    { path: '/chat', name: 'AI Assistant', icon: ChatBubbleLeftRightIcon },
    { path: '/cart', name: 'Cart', icon: ShoppingCartIcon }
  ];

  const isActive = (path) => location.pathname === path;

  const containerClasses = darkMode
    ? 'bg-slate-950/85 border-slate-800/70 shadow-[0_25px_60px_-30px_RGBA(15,23,42,0.65)]'
    : 'bg-white/90 border-white/70 shadow-[0_25px_60px_-30px_RGBA(79,70,229,0.35)]';

  const navPillClasses = (active) =>
    active
      ? 'bg-gradient-to-r from-purple-600 via-indigo-500 to-blue-500 text-white shadow-lg shadow-purple-500/30'
      : darkMode
        ? 'text-gray-300 hover:text-white hover:bg-gray-800/70'
        : 'text-gray-700 hover:text-gray-900 hover:bg-white/70';

  const actionSurface = darkMode ? 'bg-gray-800/70 text-gray-100' : 'bg-white/80 text-gray-600';

  const mobilePanelClasses = darkMode
    ? 'bg-gray-900/95 border-gray-800 shadow-purple-500/10'
    : 'bg-white/95 border-white/70 shadow-purple-500/10';

  return (
    <nav className="sticky top-0 z-50 backdrop-blur-2xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
        <div className={`relative overflow-hidden rounded-3xl border ${containerClasses}`}>
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500/12 via-transparent to-blue-500/12" />
          <div className="absolute -top-16 -left-12 h-40 w-40 rounded-full bg-purple-400/25 blur-3xl" />
          <div className="absolute -bottom-16 -right-14 h-40 w-40 rounded-full bg-blue-400/25 blur-3xl" />
          <div className="relative flex items-center justify-between h-[84px] px-5 sm:px-8">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3 group">
              <motion.div
                whileHover={{ rotate: 360, scale: 1.1 }}
                transition={{ duration: 0.6, type: 'spring' }}
                className="w-12 h-12 bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-600 rounded-2xl flex items-center justify-center shadow-lg"
              >
                <SparklesIcon className="w-7 h-7 text-white drop-shadow-sm" />
              </motion.div>
              <div className="flex flex-col">
                <span className="text-2xl font-black font-heading tracking-tight group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-blue-600 group-hover:bg-clip-text group-hover:text-transparent transition-all">
                  Retail AI
                </span>
                <span className={`text-xs font-medium -mt-1 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                  Smart Shopping
                </span>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-2">
              {navItems.map((item) => {
                const Icon = item.icon;
                const active = isActive(item.path);
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-3 px-4 py-3.5 rounded-xl transition-all ${navPillClasses(active)}`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.name}</span>
                    {item.path === '/cart' && cartItemCount > 0 && (
                      <span className="ml-auto px-2 py-0.5 bg-gradient-to-r from-rose-500 to-pink-600 text-white text-xs rounded-full font-medium">
                        {cartItemCount}
                      </span>
                    )}
                  </Link>
                );
              })}
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center space-x-3">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-full transition-colors ${actionSurface}`}
              >
                <UserCircleIcon className="w-5 h-5" />
                <span className="font-medium">Guest User</span>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={toggleDarkMode}
                className={`ml-auto p-2 rounded-lg transition-colors ${actionSurface}`}
              >
                {darkMode ? <SunIcon className="w-4 h-4" /> : <MoonIcon className="w-4 h-4" />}
              </motion.button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className={`md:hidden mx-4 mb-4 rounded-2xl border ${mobilePanelClasses} backdrop-blur-xl`}
          >
            <div className="px-4 py-4 space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon;
                const active = isActive(item.path);
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center space-x-3 px-4 py-3.5 rounded-xl transition-all ${
                      active
                        ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                        : darkMode
                          ? 'text-gray-300 hover:bg-gray-800'
                          : 'text-neutral-600 hover:bg-neutral-100'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.name}</span>
                    {item.path === '/cart' && cartItemCount > 0 && (
                      <span className="ml-auto px-2 py-0.5 bg-gradient-to-r from-rose-500 to-pink-600 text-white text-xs rounded-full font-medium">
                        {cartItemCount}
                      </span>
                    )}
                  </Link>
                );
              })}

              <div className={`pt-4 border-t ${darkMode ? 'border-gray-800/80' : 'border-neutral-200/80'}`}>
                <div className="flex items-center space-x-3 px-4 py-3">
                  <UserCircleIcon className={`w-6 h-6 ${darkMode ? 'text-gray-400' : 'text-neutral-600'}`} />
                  <div>
                    <div className={`font-medium ${darkMode ? 'text-gray-100' : 'text-neutral-900'}`}>
                      Guest User
                    </div>
                    <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-neutral-500'}`}>
                      Not signed in
                    </div>
                  </div>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={toggleDarkMode}
                    className={`ml-auto p-2 rounded-lg transition-colors ${actionSurface}`}
                  >
                    {darkMode ? <SunIcon className="w-4 h-4" /> : <MoonIcon className="w-4 h-4" />}
                  </motion.button>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;