import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

const useStore = create(
  devtools(
    (set, get) => ({
      // Chat state
      messages: [],
      isTyping: false,
      customerId: localStorage.getItem('retail_customer_id') || `CUST${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      currentChannel: 'web', // Default channel
      
      // UI state
      sidebarOpen: true,
      darkMode: false,
      
      // Shopping state
      cart: [],
      selectedProducts: [],
      currentPromotions: [],
      
      // Customer state
      customerContext: null,
      
      // Actions
      addMessage: (message) => set((state) => ({
        messages: [...state.messages, {
          ...message,
          id: Date.now() + Math.random(),
          timestamp: new Date().toISOString()
        }]
      })),
      
      setTyping: (typing) => set({ isTyping: typing }),
      
      setChannel: (channel) => set({ currentChannel: channel }),
      
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      
      toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
      
      addToCart: (product) => set((state) => {
        const existingItem = state.cart.find(item => item.id === product.id);
        if (existingItem) {
          return {
            cart: state.cart.map(item =>
              item.id === product.id
                ? { ...item, quantity: item.quantity + 1 }
                : item
            )
          };
        }
        return {
          cart: [...state.cart, { ...product, quantity: 1 }]
        };
      }),
      
      removeFromCart: (productId) => set((state) => ({
        cart: state.cart.filter(item => item.id !== productId)
      })),
      
      updateCartQuantity: (productId, quantity) => set((state) => ({
        cart: state.cart.map(item =>
          item.id === productId
            ? { ...item, quantity: Math.max(0, quantity) }
            : item
        ).filter(item => item.quantity > 0)
      })),
      
      clearCart: () => set({ cart: [] }),
      
      setSelectedProducts: (products) => set({ selectedProducts: products }),
      
      setCurrentPromotions: (promotions) => set({ currentPromotions: promotions }),
      
      setCustomerContext: (context) => set({ customerContext: context }),
      
      // Computed values
      getCartTotal: () => {
        const { cart } = get();
        return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
      },
      
      getCartItemCount: () => {
        const { cart } = get();
        return cart.reduce((count, item) => count + item.quantity, 0);
      },
      
      // Initialize customer ID
      initializeCustomer: () => {
        const { customerId } = get();
        if (!localStorage.getItem('retail_customer_id')) {
          localStorage.setItem('retail_customer_id', customerId);
        }
      }
    }),
    {
      name: 'retail-ai-store',
    }
  )
);

export default useStore;
