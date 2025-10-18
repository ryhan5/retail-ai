# 🛍️ Retail Conversational Sales Agent

An advanced AI-driven conversational sales solution powered by **Google Gemini AI** that revolutionizes the retail shopping experience across multiple channels. This system features a Master Sales Agent orchestrating specialized Worker Agents to provide seamless customer journeys from product discovery to checkout.

## 🎯 Problem Statement

Customers face fragmented experiences when moving between online browsing, mobile app shopping, messaging apps, and in-store interactions. Limited bandwidth among sales associates leads to missed up-sell and cross-sell opportunities. This solution aims to increase Average Order Value (AOV) and conversion rates by offering a unified, human-like conversational journey.

## 🏗️ System Architecture

### Master Sales Agent
- **Natural Language Understanding**: Detects customer intent and context
- **Multi-Channel Support**: Web, Mobile, WhatsApp, In-Store Kiosk, Voice Assistant
- **Conversation Orchestration**: Manages dialogue flow and coordinates Worker Agents
- **Personalization Engine**: Adapts responses based on customer history and preferences

### Worker Agents

#### 1. 📦 Inventory Agent
- Real-time stock checking across all locations
- Store availability and reservation system
- Low stock alerts and restock notifications
- Multi-location inventory management

#### 2. 🎯 Recommendation Agent
- **Collaborative Filtering**: Based on similar customer behavior
- **Content-Based Filtering**: Using customer preferences and product attributes
- **Hybrid Approach**: Combines multiple recommendation algorithms
- **Cross-sell & Upsell**: Smart product suggestions to increase AOV

#### 3. 💰 Promotion Agent
- Dynamic promotion application
- Customer-specific offers and discounts
- Promotion stacking validation
- Upsell opportunities based on cart value

#### 4. 💳 Payment Agent
- Secure payment processing
- Multiple payment method support
- Transaction validation and error handling
- Payment analytics and reporting

#### 5. 📋 Order Agent
- Order creation and management
- Delivery estimation and tracking
- Order status updates
- Post-purchase support coordination

## 🚀 Key Features

### Multi-Channel Experience
- **Web Chat**: Full-featured browser interface
- **Mobile App**: Optimized mobile experience
- **WhatsApp Integration**: Conversational commerce via messaging
- **In-Store Kiosk**: Physical store assistance
- **Voice Assistant**: Hands-free shopping experience

### Intelligent Personalization
- Customer context management
- Purchase history analysis
- Preference learning and adaptation
- Behavioral pattern recognition

### Advanced Sales Capabilities
- Natural language product search
- Smart recommendations with reasoning
- Automatic promotion discovery
- Seamless checkout process
- Real-time inventory checking

### Analytics & Insights
- Conversation analytics
- Conversion tracking
- Customer satisfaction metrics
- Performance dashboards

## 🛠️ Technical Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI/ML**: Natural Language Processing, Recommendation Algorithms
- **APIs**: RESTful services with JSON responses
- **Database**: Mock data with extensible architecture
- **UI/UX**: Responsive design with modern interface

## 📁 Project Structure

```
retail-sales-agent/
├── app.py                          # Main Flask application
├── agents/
│   ├── master_sales_agent.py       # Master orchestration agent
│   └── worker_agents/
│       ├── inventory_agent.py      # Stock and availability management
│       ├── recommendation_agent.py # Product recommendations
│       ├── promotion_agent.py      # Promotions and discounts
│       ├── payment_agent.py        # Payment processing
│       └── order_agent.py          # Order management
├── utils/
│   ├── customer_context.py         # Customer data management
│   └── mock_apis.py                # Mock external services
├── frontend/                       # 🆕 Modern React Frontend
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── Header.js          # Top navigation
│   │   │   ├── Sidebar.js         # Channel selector
│   │   │   ├── WelcomeScreen.js   # Welcome interface
│   │   │   ├── ChatInterface.js   # Main chat
│   │   │   ├── MessageBubble.js   # Message display
│   │   │   ├── ProductShowcase.js # Product recommendations
│   │   │   └── ShoppingCart.js    # Cart management
│   │   ├── services/
│   │   │   └── api.js             # API integration
│   │   ├── store/
│   │   │   └── useStore.js        # State management
│   │   ├── App.js                 # Main React app
│   │   ├── index.js               # App entry point
│   │   └── index.css              # Global styles
│   ├── package.json               # React dependencies
│   └── tailwind.config.js         # Tailwind configuration
├── templates/
│   └── index.html                  # Original HTML interface
├── static/
│   └── js/
│       └── chat.js                 # Original JavaScript
├── requirements.txt                # Python dependencies
├── start-dev.bat                   # 🆕 Development startup script
├── start-react.bat                 # 🆕 Production startup script
└── README.md                       # This file
```

## 🚀 Quick Start

### Option 1: Modern React Frontend (Recommended)

```bash
# Development Mode (React + Flask)
.\start-dev.bat

# Production Mode (Built React served by Flask)
.\start-react.bat
```

**React Development Server**: http://localhost:3001  
**Flask API Server**: http://localhost:5000

### Option 2: Original HTML Interface

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

**Flask Server with HTML Interface**: http://localhost:5000

### 🎨 React Frontend Features

- **Modern UI**: Glass morphism design with smooth animations
- **Multi-Channel**: Web, Mobile, WhatsApp, In-store, Voice support
- **Real-time Chat**: Interactive messaging with rich content
- **Smart Shopping**: Product showcase, cart management, checkout
- **Responsive**: Optimized for all devices and screen sizes

## 💬 Usage Examples

### Product Discovery
- "I'm looking for wireless headphones under $200"
- "Show me the latest smartphones"
- "Find me a gift for my tech-savvy friend"

### Inventory & Availability
- "Is this item available in the downtown store?"
- "Can I reserve this for pickup?"
- "When will this be back in stock?"

### Promotions & Deals
- "What promotions do you have today?"
- "Do I qualify for any discounts?"
- "Apply coupon code SAVE20"

### Shopping & Checkout
- "Add this to my cart"
- "I'm ready to checkout"
- "What payment methods do you accept?"

## 🎯 Business Impact

### Increased Conversion Rates
- Personalized product recommendations
- Proactive promotion application
- Reduced cart abandonment through assistance

### Higher Average Order Value
- Smart cross-sell and upsell suggestions
- Bundle recommendations
- Threshold-based promotions

### Enhanced Customer Experience
- 24/7 availability across all channels
- Consistent experience across touchpoints
- Instant responses to customer queries

### Operational Efficiency
- Reduced load on human sales associates
- Automated inventory management
- Streamlined order processing

## 🚀 Quick Start

### 1. Get Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in and create an API key
3. Copy your API key

### 2. Setup Environment
```bash
# Copy environment template
cp .env.example .env

# Add your Gemini API key to .env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Install & Run
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run setup script
python setup_gemini.py

# Start backend
python app.py

# Start frontend (in new terminal)
cd frontend
npm install
npm start
```

### 4. Test the Application
- Open `http://localhost:3001`
- Try: "Hello! Show me some laptops under $1000"
- Experience the AI-powered shopping assistant!

📖 **Detailed setup guide**: See [GEMINI_MIGRATION.md](GEMINI_MIGRATION.md)

## 🔧 Customization & Extension

### Adding New Channels
1. Update `master_sales_agent.py` to handle new channel types
2. Implement channel-specific message formatting
3. Add channel selection in the frontend

### Custom Recommendation Algorithms
1. Extend `recommendation_agent.py` with new algorithms
2. Implement custom scoring mechanisms
3. Add A/B testing capabilities

### Integration with External Systems
1. Replace mock APIs in `mock_apis.py` with real integrations
2. Implement proper authentication and security
3. Add error handling and retry mechanisms

## 📊 Analytics & Monitoring

The system provides comprehensive analytics including:
- Conversation success rates
- Customer satisfaction scores
- Product recommendation effectiveness
- Channel performance metrics
- Revenue attribution

## 🔒 Security Considerations

- Input validation and sanitization
- Secure payment processing
- Customer data protection
- API rate limiting
- Session management

## 🚀 Future Enhancements

### Advanced AI Capabilities
- Sentiment analysis for customer mood detection
- Predictive analytics for inventory management
- Advanced NLP for better intent recognition

### Extended Channel Support
- Social media integration (Facebook, Instagram)
- Email marketing automation
- SMS/Text message support

### Enhanced Personalization
- Machine learning-based customer segmentation
- Dynamic pricing based on customer behavior
- Predictive product recommendations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation wiki

---

**Built with ❤️ for the future of retail commerce**
