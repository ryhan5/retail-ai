import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import useStore from './store/useStore';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import CartPage from './pages/CartPage';
import ChatPage from './pages/ChatPage';

function App() {
  const { initializeCustomer, darkMode } = useStore();

  useEffect(() => {
    initializeCustomer();
  }, [initializeCustomer]);

  return (
    <Router>
      <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
        <Navbar />
        
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>

        {/* Toast Notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(14px)',
              border: '1px solid rgba(168, 85, 247, 0.15)',
              borderRadius: '16px',
              color: '#1C1917',
            },
            success: {
              iconTheme: {
                primary: '#14B8A6',
                secondary: '#ffffff',
              },
            },
            error: {
              iconTheme: {
                primary: '#F43F5E',
                secondary: '#ffffff',
              },
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;
