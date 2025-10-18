import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const chatAPI = {
  sendMessage: async (message, channel, customerId) => {
    const response = await api.post('/api/chat', {
      message,
      channel,
      customer_id: customerId
    });
    return response.data;
  },
  
  getCustomerContext: async (customerId) => {
    const response = await api.get(`/api/customer/${customerId}/context`);
    return response.data;
  }
};

export const productAPI = {
  searchProducts: async (query, filters = {}) => {
    const response = await api.post('/api/products/search', {
      query,
      filters
    });
    return response.data;
  },
  
  checkInventory: async (productId, storeLocation) => {
    const response = await api.post('/api/inventory/check', {
      product_id: productId,
      store_location: storeLocation
    });
    return response.data;
  }
};

export const promotionAPI = {
  getPromotions: async (customerId) => {
    const response = await api.get('/api/promotions', {
      params: { customer_id: customerId }
    });
    return response.data;
  }
};

export const orderAPI = {
  createOrder: async (orderData) => {
    const response = await api.post('/api/order/create', orderData);
    return response.data;
  },
  
  processPayment: async (paymentData) => {
    const response = await api.post('/api/payment/process', paymentData);
    return response.data;
  }
};

export const analyticsAPI = {
  getDashboard: async () => {
    const response = await api.get('/api/analytics/dashboard');
    return response.data;
  }
};

export default api;
