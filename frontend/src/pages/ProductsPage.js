import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  HeartIcon,
  ShoppingCartIcon,
  StarIcon,
  ChevronDownIcon,
  Squares2X2Icon,
  ListBulletIcon,
  SparklesIcon,
  ArrowRightIcon,
  BoltIcon,
  TagIcon,
  TruckIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';
import { HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';
import useStore from '../store/useStore';
import toast from 'react-hot-toast';

const ProductsPage = () => {
  const { addToCart } = useStore();
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [priceRange, setPriceRange] = useState([0, 1000]);
  const [sortBy, setSortBy] = useState('featured');
  const [viewMode, setViewMode] = useState('grid');
  const [wishlist, setWishlist] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [activeQuickFilter, setActiveQuickFilter] = useState('all');

  // Expanded product data with more items and categories
  const mockProducts = useMemo(() => ([
    {
      id: 1,
      name: 'Premium Wireless Headphones',
      category: 'electronics',
      price: 299.99,
      rating: 4.5,
      reviews: 234,
      image: 'https://placehold.co/300x300/9333EA/ffffff?text=Headphones',
      description: 'High-quality wireless headphones with noise cancellation',
      features: ['Noise Cancellation', 'Wireless', '30hr Battery'],
      inStock: true
    },
    {
      id: 2,
      name: 'Smart Watch Pro',
      category: 'electronics',
      price: 399.99,
      rating: 4.8,
      reviews: 567,
      image: 'https://placehold.co/300x300/7E22CE/ffffff?text=SmartWatch',
      description: 'Advanced fitness tracking and health monitoring',
      features: ['Heart Rate', 'GPS', 'Water Resistant'],
      inStock: true
    },
    {
      id: 3,
      name: 'Organic Cotton T-Shirt',
      category: 'clothing',
      price: 29.99,
      rating: 4.3,
      reviews: 89,
      image: 'https://placehold.co/300x300/8B5CF6/ffffff?text=T-Shirt',
      description: 'Comfortable and sustainable organic cotton t-shirt',
      features: ['100% Organic', 'Soft Fabric', 'Eco-Friendly'],
      inStock: true
    },
    {
      id: 4,
      name: 'Bluetooth Speaker',
      category: 'electronics',
      price: 79.99,
      rating: 4.6,
      reviews: 445,
      image: 'https://placehold.co/300x300/9333EA/ffffff?text=Speaker',
      description: 'Portable speaker with amazing sound quality',
      features: ['Waterproof', '12hr Battery', 'Bass Boost'],
      inStock: true
    },
    {
      id: 5,
      name: 'Running Shoes',
      category: 'footwear',
      price: 129.99,
      rating: 4.7,
      reviews: 892,
      image: 'https://placehold.co/300x300/7C3AED/ffffff?text=Shoes',
      description: 'Professional running shoes for maximum comfort',
      features: ['Cushioned', 'Breathable', 'Lightweight'],
      inStock: true
    },
    {
      id: 6,
      name: 'Laptop Backpack',
      category: 'accessories',
      price: 59.99,
      rating: 4.4,
      reviews: 156,
      image: 'https://placehold.co/300x300/8B5CF6/ffffff?text=Backpack',
      description: 'Spacious backpack with laptop compartment',
      features: ['Water Resistant', 'USB Port', 'Anti-Theft'],
      inStock: false
    },
    {
      id: 7,
      name: 'Wireless Earbuds',
      category: 'electronics',
      price: 149.99,
      rating: 4.6,
      reviews: 321,
      image: 'https://placehold.co/300x300/9333EA/ffffff?text=Earbuds',
      description: 'True wireless earbuds with premium sound quality',
      features: ['Active Noise Cancellation', 'IPX7 Waterproof', '8hr Battery'],
      inStock: true
    },
    {
      id: 8,
      name: 'Designer Sunglasses',
      category: 'accessories',
      price: 89.99,
      rating: 4.2,
      reviews: 178,
      image: 'https://placehold.co/300x300/7E22CE/ffffff?text=Sunglasses',
      description: 'UV protection with stylish design',
      features: ['UV400 Protection', 'Polarized Lenses', 'Lightweight Frame'],
      inStock: true
    },
    {
      id: 9,
      name: 'Premium Yoga Mat',
      category: 'fitness',
      price: 45.99,
      rating: 4.7,
      reviews: 203,
      image: 'https://placehold.co/300x300/8B5CF6/ffffff?text=Yoga+Mat',
      description: 'Non-slip, eco-friendly yoga mat for all levels',
      features: ['Eco-Friendly', 'Non-Slip', 'Extra Thick'],
      inStock: true
    },
    {
      id: 10,
      name: 'Smart Home Hub',
      category: 'electronics',
      price: 199.99,
      rating: 4.5,
      reviews: 412,
      image: 'https://placehold.co/300x300/9333EA/ffffff?text=Smart+Hub',
      description: 'Control all your smart devices from one place',
      features: ['Voice Control', 'Works with Alexa', 'Easy Setup'],
      inStock: true
    },
    {
      id: 11,
      name: 'Leather Wallet',
      category: 'accessories',
      price: 39.99,
      rating: 4.3,
      reviews: 98,
      image: 'https://placehold.co/300x300/7C3AED/ffffff?text=Wallet',
      description: 'Genuine leather wallet with RFID protection',
      features: ['RFID Blocking', 'Slim Design', 'Multiple Card Slots'],
      inStock: true
    },
    {
      id: 12,
      name: 'Wireless Charging Pad',
      category: 'electronics',
      price: 34.99,
      rating: 4.4,
      reviews: 267,
      image: 'https://placehold.co/300x300/8B5CF6/ffffff?text=Charger',
      description: 'Fast wireless charging for all Qi-enabled devices',
      features: ['15W Fast Charging', 'LED Indicator', 'Non-Slip Surface'],
      inStock: true
    }
  ]), []);

  const categories = [
    { id: 'all', name: 'All Products' },
    { id: 'electronics', name: 'Electronics' },
    { id: 'clothing', name: 'Clothing' },
    { id: 'footwear', name: 'Footwear' },
    { id: 'accessories', name: 'Accessories' },
    { id: 'fitness', name: 'Fitness' }
  ];

  const sortOptions = [
    { id: 'featured', name: 'Featured' },
    { id: 'price-low', name: 'Price: Low to High' },
    { id: 'price-high', name: 'Price: High to Low' },
    { id: 'rating', name: 'Highest Rated' },
    { id: 'newest', name: 'Newest First' }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setProducts(mockProducts);
      setFilteredProducts(mockProducts);
      setLoading(false);
    }, 800);
  }, [mockProducts]);

  const filterAndSortProducts = useCallback(() => {
    let filtered = [...products];

    // Search filter
    if (searchQuery) {
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Category filter
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(product => product.category === selectedCategory);
    }

    // Price filter
    filtered = filtered.filter(product => 
      product.price >= priceRange[0] && product.price <= priceRange[1]
    );

    // Quick filters
    if (activeQuickFilter === 'top-rated') {
      filtered = filtered.filter(product => product.rating >= 4.5);
    }

    if (activeQuickFilter === 'budget') {
      filtered = filtered.filter(product => product.price <= 150);
    }

    if (activeQuickFilter === 'new') {
      filtered = filtered.slice().sort((a, b) => b.id - a.id);
    }

    // Sorting
    switch (sortBy) {
      case 'price-low':
        filtered.sort((a, b) => a.price - b.price);
        break;
      case 'price-high':
        filtered.sort((a, b) => b.price - a.price);
        break;
      case 'rating':
        filtered.sort((a, b) => b.rating - a.rating);
        break;
      default:
        break;
    }

    setFilteredProducts(filtered);
  }, [products, searchQuery, selectedCategory, priceRange, sortBy, activeQuickFilter]);

  useEffect(() => {
    filterAndSortProducts();
  }, [filterAndSortProducts]);

  const handleAddToCart = (product) => {
    addToCart(product);
    toast.success(`${product.name} added to cart!`);
  };

  const toggleWishlist = (productId) => {
    const newWishlist = new Set(wishlist);
    if (wishlist.has(productId)) {
      newWishlist.delete(productId);
      toast.success('Removed from wishlist');
    } else {
      newWishlist.add(productId);
      toast.success('Added to wishlist');
    }
    setWishlist(newWishlist);
  };

  const quickFilters = [
    { id: 'all', label: 'All Collections', icon: SparklesIcon },
    { id: 'top-rated', label: 'Top Rated', icon: StarIcon },
    { id: 'budget', label: 'Under ₹150', icon: FunnelIcon },
    { id: 'new', label: 'New Arrivals', icon: BoltIcon }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-purple-50">
      {/* Hero / Intro */}
      <div className="relative pb-16">
        <div className="absolute inset-0 h-96 bg-gradient-to-br from-purple-500/10 via-transparent to-teal-400/10" />
        <div className="absolute inset-x-0 top-0 h-80 bg-[radial-gradient(circle_at_top,_rgba(168,85,247,0.2)_0,_rgba(255,255,255,0)_70%)] blur-3xl" />
        <div className="relative max-w-7xl mx-auto px-6 pt-12">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="overflow-hidden rounded-3xl border border-white/60 bg-white/75 shadow-[0_35px_120px_-60px_rgba(79,70,229,0.55)] backdrop-blur-2xl"
          >
            <div className="absolute -top-20 -left-24 h-64 w-64 rounded-full bg-purple-400/30 blur-3xl" />
            <div className="absolute -bottom-16 -right-24 h-60 w-60 rounded-full bg-emerald-300/30 blur-3xl" />

            <div className="relative px-8 py-10 lg:px-12 lg:py-12 flex flex-col gap-10">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">
                <div className="max-w-2xl space-y-4">
                  <span className="inline-flex items-center gap-2 rounded-full bg-slate-900 text-white px-4 py-1 text-xs font-semibold uppercase tracking-wider">
                    <SparklesIcon className="w-4 h-4" />
                    Curated by Gemini AI
                  </span>
                  <h1 className="text-4xl lg:text-5xl font-bold font-heading text-slate-900">
                    Premium Products, Handpicked for You
                  </h1>
                  <p className="text-base lg:text-lg text-slate-600 leading-relaxed">
                    Discover immersive collections, real-time availability, and stylist-approved pairings crafted for every channel of your shopping journey.
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4 min-w-[220px]">
                  {[
                    { label: 'Avg. rating', value: '4.7/5', helper: 'Across 10+ categories' },
                    { label: 'Same-day dispatch', value: '84%', helper: 'Orders before 4 PM' },
                    { label: 'Members savings', value: '₹12k', helper: 'Annual average' },
                    { label: 'Active collections', value: '36', helper: 'Updated hourly' }
                  ].map((stat) => (
                    <div
                      key={stat.label}
                      className="rounded-2xl border border-white/70 bg-white/80 px-4 py-3 shadow-sm backdrop-blur-xl"
                    >
                      <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                        {stat.label}
                      </span>
                      <div className="mt-1 text-xl font-semibold text-slate-900">
                        {stat.value}
                      </div>
                      <p className="text-[11px] text-slate-500">{stat.helper}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                  {
                    title: 'Personalized picks',
                    description: 'AI curates looks based on behaviour and trends',
                    icon: SparklesIcon
                  },
                  {
                    title: 'Express delivery',
                    description: 'Same-day options in 60+ metro cities',
                    icon: TruckIcon
                  },
                  {
                    title: 'Member exclusives',
                    description: 'Unlock drops and private sale previews',
                    icon: TagIcon
                  },
                  {
                    title: 'Trusted checkout',
                    description: 'Bank-grade security with assurance badges',
                    icon: ShieldCheckIcon
                  }
                ].map((card, index) => (
                  <motion.div
                    key={card.title}
                    initial={{ opacity: 0, y: 16 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.08 * index }}
                    className="rounded-2xl border border-white/70 bg-white/65 p-5 shadow-sm backdrop-blur-xl transition-all hover:-translate-y-1"
                  >
                    <div className="flex items-center gap-3">
                      <card.icon className="w-5 h-5 text-purple-500" />
                      <span className="text-sm font-semibold text-slate-900">{card.title}</span>
                    </div>
                    <p className="mt-3 text-sm text-slate-600 leading-relaxed">
                      {card.description}
                    </p>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-10">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filters Sidebar */}
          <aside className="lg:w-64 space-y-6">
            {/* Search */}
            <div className="rounded-2xl border border-white/60 bg-white/70 p-6 shadow-sm backdrop-blur-xl">
              <h3 className="font-semibold text-slate-900 mb-4">Search</h3>
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-purple-500" />
                <input
                  type="text"
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 rounded-xl border border-white/60 bg-white/70 text-slate-700 placeholder:text-slate-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-300"
                />
              </div>
            </div>

            {/* Categories */}
            <div className="rounded-2xl border border-white/60 bg-white/70 p-6 shadow-sm backdrop-blur-xl">
              <h3 className="font-semibold text-slate-900 mb-4">Categories</h3>
              <div className="space-y-2">
                {categories.map(category => (
                  <button
                    key={category.id}
                    onClick={() => setSelectedCategory(category.id)}
                    className={`w-full text-left px-4 py-2 rounded-xl transition-all ${
                      selectedCategory === category.id
                        ? 'bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-purple-700 font-semibold shadow-sm'
                        : 'bg-white/60 text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    {category.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Price Range */}
            <div className="rounded-2xl border border-white/60 bg-white/70 p-6 shadow-sm backdrop-blur-xl">
              <h3 className="font-semibold text-slate-900 mb-4">Price Range</h3>
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <input
                    type="number"
                    placeholder="Min"
                    value={priceRange[0]}
                    onChange={(e) => setPriceRange([Number(e.target.value), priceRange[1]])}
                    className="w-full px-3 py-2 rounded-xl border border-white/60 bg-white/70 text-slate-700 focus:border-purple-500 focus:ring-2 focus:ring-purple-300"
                  />
                  <span className="text-neutral-500">-</span>
                  <input
                    type="number"
                    placeholder="Max"
                    value={priceRange[1]}
                    onChange={(e) => setPriceRange([priceRange[0], Number(e.target.value)])}
                    className="w-full px-3 py-2 rounded-xl border border-white/60 bg-white/70 text-slate-700 focus:border-purple-500 focus:ring-2 focus:ring-purple-300"
                  />
                </div>
                <div className="h-2 bg-slate-200/70 rounded-full">
                  <div 
                    className="h-full bg-gradient-to-r from-purple-500 via-indigo-500 to-teal-400 rounded-full" 
                    style={{ width: `${(priceRange[1] / 1000) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </aside>

          {/* Products Grid */}
          <div className="flex-1">
            {/* Enhanced Toolbar */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-3xl border border-white/60 bg-white/75 p-6 shadow-lg backdrop-blur-2xl mb-8"
            >
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="flex items-center gap-6">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl font-bold text-slate-900">
                      {filteredProducts.length}
                    </span>
                    <span className="text-slate-500">
                      {filteredProducts.length === 1 ? 'product' : 'products'} found
                    </span>
                  </div>
                  {selectedCategory !== 'all' && (
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-slate-500">in</span>
                      <span className="px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-purple-700">
                        {categories.find(c => c.id === selectedCategory)?.name}
                      </span>
                    </div>
                  )}
                </div>
                
                <div className="flex items-center gap-4">
                  {/* Enhanced Sort */}
                  <div className="relative">
                    <select
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value)}
                      className="appearance-none rounded-xl border border-white/60 bg-white/70 px-4 py-2.5 pr-10 text-sm font-medium text-slate-700 shadow-sm focus:border-purple-500 focus:ring-2 focus:ring-purple-300"
                    >
                      {sortOptions.map(option => (
                        <option key={option.id} value={option.id}>
                          {option.name}
                        </option>
                      ))}
                    </select>
                    <ChevronDownIcon className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-purple-500 pointer-events-none" />
                  </div>

                  {/* Enhanced View Mode */}
                  <div className="flex items-center rounded-xl border border-white/60 bg-white/70 p-1 shadow-sm">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setViewMode('grid')}
                      className={`p-2 rounded-lg transition-all ${
                        viewMode === 'grid' 
                          ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-md' 
                          : 'text-slate-500 hover:text-purple-500'
                      }`}
                    >
                      <Squares2X2Icon className="w-5 h-5" />
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setViewMode('list')}
                      className={`p-2 rounded-lg transition-all ${
                        viewMode === 'list' 
                          ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-md' 
                          : 'text-slate-500 hover:text-purple-500'
                      }`}
                    >
                      <ListBulletIcon className="w-5 h-5" />
                    </motion.button>
                  </div>
                </div>
                <div className="flex flex-wrap items-center gap-3">
                  {quickFilters.map(filter => {
                    const Icon = filter.icon;
                    const isActive = activeQuickFilter === filter.id;
                    return (
                      <motion.button
                        key={filter.id}
                        whileHover={{ y: -2 }}
                        whileTap={{ scale: 0.97 }}
                        onClick={() => setActiveQuickFilter(filter.id)}
                        className={`flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-medium transition-all ${
                          isActive
                            ? 'border-purple-400 bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-purple-700 shadow-sm'
                            : 'border-white/60 bg-white/70 text-slate-600 hover:border-purple-300 hover:text-purple-600'
                        }`}
                      >
                        <Icon className={`w-4 h-4 ${isActive ? 'text-purple-600' : 'text-slate-400'}`} />
                        {filter.label}
                      </motion.button>
                    );
                  })}
                </div>
              </div>
            </motion.div>

            {/* Products */}
            {loading ? (
              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {[...Array(9)].map((_, index) => (
                  <div
                    key={index}
                    className="animate-pulse rounded-2xl border border-white/60 bg-white/70 p-6 shadow-sm backdrop-blur-xl"
                  >
                    <div className="mb-4 h-48 w-full rounded-xl bg-slate-200/60" />
                    <div className="mb-2 h-4 w-3/4 rounded bg-slate-200/60" />
                    <div className="mb-4 h-3 w-1/2 rounded bg-slate-100/70" />
                    <div className="h-10 w-full rounded-lg bg-slate-200/60" />
                  </div>
                ))}
              </div>
            ) : (
              <AnimatePresence>
                <motion.div
                  layout
                  className={`grid gap-6 ${
                    viewMode === 'grid'
                      ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
                      : 'grid-cols-1'
                  }`}
                >
                  {filteredProducts.map((product, index) => (
                    <motion.div
                      key={product.id}
                      layout
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ delay: index * 0.05 }}
                      className={`group relative overflow-hidden rounded-3xl border border-white/60 bg-white/75 shadow-lg backdrop-blur-2xl transition-all hover:-translate-y-1 hover:shadow-[0_35px_90px_-40px_rgba(79,70,229,0.45)] ${
                        viewMode === 'list' ? 'flex gap-6' : ''
                      }`}
                    >
                      {/* Purple gradient top bar */}
                      <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-purple-500 via-indigo-500 to-teal-400" />

                      {/* Product Image */}
                      <div className={`relative ${viewMode === 'list' ? 'w-48' : ''}`}>
                        <img
                          src={product.image}
                          alt={product.name}
                          className={
                            viewMode === 'list'
                              ? 'h-full w-full rounded-l-2xl object-cover'
                              : 'h-64 w-full rounded-t-2xl object-cover'
                          }
                        />
                        {!product.inStock && (
                          <div className="absolute inset-0 flex items-center justify-center rounded-t-2xl bg-neutral-900/70">
                            <span className="text-sm font-semibold uppercase tracking-widest text-white">Waitlist</span>
                          </div>
                        )}
                        <button
                          onClick={() => toggleWishlist(product.id)}
                          className="absolute right-4 top-4 rounded-full bg-white/90 p-2 text-slate-500 shadow-md transition-all hover:bg-white hover:text-rose-500"
                        >
                          {wishlist.has(product.id) ? (
                            <HeartSolidIcon className="w-5 h-5 text-rose-500" />
                          ) : (
                            <HeartIcon className="w-5 h-5" />
                          )}
                        </button>
                      </div>

                      {/* Product Info */}
                      <div className={`flex flex-1 flex-col p-6 ${viewMode === 'list' ? '' : ''}`}>
                        <div className="mb-3 flex items-start justify-between gap-3">
                          <div>
                            <span className="inline-flex items-center rounded-full bg-purple-500/15 px-3 py-1 text-xs font-semibold text-purple-600">
                              {product.category}
                            </span>
                            <h3 className="mt-3 text-lg font-semibold text-neutral-900">
                              {product.name}
                            </h3>
                          </div>
                          <div className="rounded-lg bg-emerald-500/15 px-3 py-1 text-xs font-semibold text-emerald-600">
                            {product.inStock ? 'In Stock' : 'Back Soon'}
                          </div>
                        </div>

                        <p className="mb-4 text-sm leading-relaxed text-neutral-600">
                          {product.description}
                        </p>

                        <div className="mb-4 flex flex-wrap gap-2">
                          {product.features.map((feature, idx) => (
                            <span
                              key={idx}
                              className="rounded-full bg-slate-100/70 px-3 py-1 text-xs font-medium text-slate-600"
                            >
                              {feature}
                            </span>
                          ))}
                        </div>
                        <div className="mb-6 flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <div className="flex items-center">
                              {[...Array(5)].map((_, i) => (
                                <StarIcon
                                  key={i}
                                  className={
                                    i < Math.floor(product.rating)
                                      ? 'h-4 w-4 text-yellow-500 fill-current'
                                      : 'h-4 w-4 text-neutral-200'
                                  }
                                />
                              ))}
                            </div>
                            <span className="text-xs font-medium text-neutral-500">
                              {product.rating} • {product.reviews} reviews
                            </span>
                          </div>
                          <span className="text-lg font-bold text-slate-900">
                            ₹{product.price.toFixed(2)}
                          </span>
                        </div>

                        <div className="mt-auto flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                          <button className="flex items-center gap-2 text-sm font-semibold text-primary-600 transition-all hover:text-primary-700">
                            View details
                            <ArrowRightIcon className="h-4 w-4" />
                          </button>
                          <motion.button
                            whileHover={{ scale: 1.03 }}
                            whileTap={{ scale: 0.97 }}
                            onClick={() => handleAddToCart(product)}
                            disabled={!product.inStock}
                            className={`flex items-center justify-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold transition-colors ${
                              product.inStock
                                ? 'bg-gradient-to-r from-purple-600 via-indigo-500 to-blue-500 text-white shadow-md hover:from-purple-700 hover:via-indigo-600 hover:to-blue-600'
                                : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                            }`}
                          >
                            <ShoppingCartIcon className="h-4 w-4" />
                            {product.inStock ? 'Add to cart' : 'Notify me'}
                          </motion.button>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              </AnimatePresence>
            )}

            {filteredProducts.length === 0 && !loading && (
              <div className="text-center py-12">
                <div className="inline-block p-4 rounded-full mb-4 bg-white/70 border border-white/60 backdrop-blur-xl">
                  <FunnelIcon className="h-8 w-8 text-purple-600" />
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-2">No products found</h3>
                <p className="text-slate-500">Try adjusting your filters or search terms</p>
                <button 
                  onClick={() => {
                    setSearchQuery('');
                    setSelectedCategory('all');
                    setPriceRange([0, 1000]);
                    setActiveQuickFilter('all');
                  }}
                  className="mt-4 px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 via-indigo-500 to-blue-500 text-white hover:from-purple-700 hover:via-indigo-600 hover:to-blue-600 transition-colors shadow-md"
                >
                  Reset Filters
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductsPage;