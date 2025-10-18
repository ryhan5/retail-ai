import React, { useState } from 'react';
import { Bars3Icon, ShoppingBagIcon, MagnifyingGlassIcon, UserCircleIcon } from '@heroicons/react/24/outline';
import { useNavigate, useLocation } from 'react-router-dom';
import useStore from '../store/useStore';

const Header = () => {
  const { toggleSidebar, getCartItemCount, customerContext } = useStore();
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  const cartItemCount = getCartItemCount();

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Products', path: '/products' },
    { name: 'Cart', path: '/cart' },
    { name: 'Chat', path: '/chat' }
  ];

  const handleSearch = (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    navigate(`/products?search=${encodeURIComponent(searchQuery)}`);
  };

  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-primary-900 via-primary-700 to-secondary-600 text-white shadow-[0_18px_45px_-18px_rgba(148,70,255,0.6)]">
      <div className="mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Left section */}
          <div className="flex items-center gap-6">
            <button
              onClick={toggleSidebar}
              className="lg:hidden p-2 rounded-lg hover:bg-white/10 transition"
              aria-label="Toggle navigation"
            >
              <Bars3Icon className="h-6 w-6 text-white" />
            </button>

            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-2"
            >
              <div className="bg-gradient-to-r from-primary-500 to-secondary-500 p-2 rounded-lg shadow-lg shadow-primary-500/30">
                <ShoppingBagIcon className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">
                RETAIL<span className="text-secondary-200 font-extrabold">AI</span>
              </span>
            </button>

            <nav className="hidden lg:flex items-center gap-1">
              {navLinks.map((link) => (
                <button
                  key={link.name}
                  onClick={() => navigate(link.path)}
                  className={`px-4 py-2 rounded-lg transition hover:no-underline focus-visible:no-underline ${
                    location.pathname === link.path
                      ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-semibold shadow-lg shadow-secondary-500/40'
                      : 'text-white/80 hover:bg-white/10'
                  }`}
                >
                  {link.name}
                </button>
              ))}
            </nav>
          </div>

          {/* Center search */}
          <div className="hidden md:flex flex-1 max-w-lg mx-8">
            <form onSubmit={handleSearch} className="w-full">
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search products or ask AI..."
                  className="w-full bg-white/15 border border-white/25 rounded-full py-2.5 pl-10 pr-4 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-secondary-300/60 focus:border-secondary-200/70"
                />
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-white/70" />
              </div>
            </form>
          </div>

          {/* Right section */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/cart')}
              className="relative p-2 rounded-lg hover:bg-white/10 transition"
              aria-label="Open cart"
            >
              <ShoppingBagIcon className="h-6 w-6 text-white" />
              {cartItemCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-gradient-to-r from-primary-500 to-secondary-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center shadow-md shadow-secondary-500/40">
                  {cartItemCount}
                </span>
              )}
            </button>

            <div className="flex items-center gap-2">
              <div className="hidden md:block text-right">
                <p className="text-sm font-medium text-white">{customerContext?.name || 'Guest'}</p>
                <p className="text-xs text-white/80">{customerContext?.loyaltyTier || 'Gold Member'}</p>
              </div>
              <div className="bg-gradient-to-r from-primary-500 to-secondary-500 p-0.5 rounded-full">
                <div className="bg-white/20 rounded-full p-0.5">
                  <UserCircleIcon className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Mobile search - shown only on small screens */}
        <div className="mt-3 md:hidden">
          <form onSubmit={handleSearch} className="w-full">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search products..."
                className="w-full bg-white/15 border border-white/25 rounded-full py-2.5 pl-10 pr-4 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-secondary-300/60 focus:border-secondary-200/70"
              />
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-white/70" />
            </div>
          </form>
        </div>
      </div>
    </header>
  );
};

export default Header;