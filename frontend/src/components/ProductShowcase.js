import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  StarIcon,
  ShoppingBagIcon,
  HeartIcon,
  EyeIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';
import useStore from '../store/useStore';
import { productAPI } from '../services/api';
import toast from 'react-hot-toast';

const ProductShowcase = () => {
  const { selectedProducts, addToCart, addMessage } = useStore();
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [wishlist, setWishlist] = useState(new Set());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadFeaturedProducts();
  }, []);

  const loadFeaturedProducts = async () => {
    setLoading(true);
    try {
      const response = await productAPI.searchProducts('featured', { limit: 6 });
      setFeaturedProducts(response.products || []);
    } catch (error) {
      console.error('Error loading featured products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = (product) => {
    addToCart(product);
    toast.success(`${product.name} added to cart!`);
  };

  const handleWishlist = (product) => {
    const newWishlist = new Set(wishlist);
    if (wishlist.has(product.id)) {
      newWishlist.delete(product.id);
      toast.success('Removed from wishlist');
    } else {
      newWishlist.add(product.id);
      toast.success('Added to wishlist');
    }
    setWishlist(newWishlist);
  };

  const handleProductClick = (product) => {
    addMessage({
      content: `Tell me more about ${product.name}`,
      sender: 'user'
    });
  };

  const productsToShow = selectedProducts.length > 0 ? selectedProducts : featuredProducts;

  return (
    <div className="h-full flex flex-col bg-white/20 backdrop-blur-sm">
      {/* Header */}
      <div className="p-4 border-b border-white/20">
        <div className="flex items-center space-x-2">
          <SparklesIcon className="w-5 h-5 text-primary-500" />
          <h2 className="text-lg font-semibold text-gray-900">
            {selectedProducts.length > 0 ? 'Recommended for You' : 'Featured Products'}
          </h2>
        </div>
        <p className="text-sm text-gray-600 mt-1">
          {selectedProducts.length > 0 
            ? 'Based on your conversation' 
            : 'Trending items you might like'
          }
        </p>
      </div>

      {/* Products Grid */}
      <div className="flex-1 overflow-y-auto p-4 scrollbar-hide">
        <AnimatePresence mode="wait">
          {loading ? (
            <div className="flex items-center justify-center h-40">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full"
              />
            </div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-4"
            >
              {productsToShow.map((product, index) => (
                <motion.div
                  key={product.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.02, y: -2 }}
                  className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-lg transition-all duration-200 cursor-pointer group"
                >
                  {/* Product Image Placeholder */}
                  <div className="w-full h-32 bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg mb-3 flex items-center justify-center group-hover:from-primary-50 group-hover:to-secondary-50 transition-all duration-200">
                    <ShoppingBagIcon className="w-12 h-12 text-gray-400 group-hover:text-primary-500 transition-colors" />
                  </div>

                  {/* Product Info */}
                  <div className="space-y-2">
                    <h3 
                      className="font-semibold text-gray-900 text-sm leading-tight group-hover:text-primary-700 transition-colors cursor-pointer"
                      onClick={() => handleProductClick(product)}
                    >
                      {product.name}
                    </h3>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-lg font-bold text-green-600">
                        ₹{product.price}
                      </span>
                      
                      {product.rating && (
                        <div className="flex items-center space-x-1">
                          <StarIcon className="w-4 h-4 text-yellow-400 fill-current" />
                          <span className="text-xs text-gray-600">{product.rating}</span>
                        </div>
                      )}
                    </div>

                    {/* Features */}
                    {product.features && (
                      <div className="flex flex-wrap gap-1">
                        {product.features.slice(0, 2).map((feature, idx) => (
                          <span 
                            key={idx}
                            className="px-2 py-1 bg-gray-100 text-xs text-gray-600 rounded-full"
                          >
                            {feature}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex items-center space-x-2 pt-2">
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => handleAddToCart(product)}
                        className="flex-1 bg-gradient-to-r from-primary-500 to-secondary-500 text-white text-xs font-medium py-2 px-3 rounded-lg hover:shadow-lg transition-all duration-200"
                      >
                        Add to Cart
                      </motion.button>
                      
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => handleWishlist(product)}
                        className="p-2 rounded-lg bg-gray-100 hover:bg-red-50 transition-colors"
                      >
                        {wishlist.has(product.id) ? (
                          <HeartSolidIcon className="w-4 h-4 text-red-500" />
                        ) : (
                          <HeartIcon className="w-4 h-4 text-gray-500 hover:text-red-500" />
                        )}
                      </motion.button>
                      
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => handleProductClick(product)}
                        className="p-2 rounded-lg bg-gray-100 hover:bg-blue-50 transition-colors"
                      >
                        <EyeIcon className="w-4 h-4 text-gray-500 hover:text-blue-500" />
                      </motion.button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Empty State */}
        {!loading && productsToShow.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center py-8"
          >
            <ShoppingBagIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500 text-sm">
              Start chatting to see personalized product recommendations!
            </p>
          </motion.div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-white/20">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => addMessage({
            content: 'Show me more products',
            sender: 'user'
          })}
          className="w-full py-2 px-4 bg-white/50 hover:bg-white/70 border border-white/20 rounded-lg text-sm font-medium text-gray-700 transition-all duration-200"
        >
          Browse More Products
        </motion.button>
      </div>
    </div>
  );
};

export default ProductShowcase;
