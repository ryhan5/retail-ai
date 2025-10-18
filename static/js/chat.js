/**
 * Retail AI Sales Assistant - Chat Interface
 * Handles real-time conversation with the AI sales agent
 */

class RetailChatInterface {
    constructor() {
        this.currentChannel = 'web';
        this.conversationHistory = [];
        this.isTyping = false;
        this.customerId = this.generateCustomerId();
        
        this.initializeElements();
        this.bindEvents();
        this.sendWelcomeMessage();
    }

    initializeElements() {
        this.messagesContainer = document.getElementById('messages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.channelButtons = document.querySelectorAll('.channel-btn');
    }

    bindEvents() {
        // Send message on button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.autoResizeTextarea();
        });

        // Channel selection
        this.channelButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.switchChannel(btn.dataset.channel);
            });
        });

        // Suggestion button clicks
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('suggestion-btn')) {
                this.sendMessage(e.target.textContent);
            }
        });

        // Product card clicks
        document.addEventListener('click', (e) => {
            if (e.target.closest('.product-card')) {
                const productCard = e.target.closest('.product-card');
                const productName = productCard.querySelector('h4').textContent;
                this.sendMessage(`Tell me more about ${productName}`);
            }
        });
    }

    generateCustomerId() {
        // Generate or retrieve customer ID
        let customerId = localStorage.getItem('retail_customer_id');
        if (!customerId) {
            customerId = 'CUST' + Math.random().toString(36).substr(2, 9).toUpperCase();
            localStorage.setItem('retail_customer_id', customerId);
        }
        return customerId;
    }

    async sendWelcomeMessage() {
        // Send initial greeting to get personalized welcome
        setTimeout(() => {
            this.sendMessage('Hello', false); // Don't show user message for initial greeting
        }, 1000);
    }

    async sendMessage(messageText = null, showUserMessage = true) {
        const message = messageText || this.messageInput.value.trim();
        
        if (!message || this.isTyping) return;

        // Show user message
        if (showUserMessage) {
            this.addMessage(message, 'user');
        }
        
        // Clear input and disable send button
        this.messageInput.value = '';
        this.autoResizeTextarea();
        this.setSendButtonState(false);
        
        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send message to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    channel: this.currentChannel,
                    customer_id: this.customerId
                })
            });

            const data = await response.json();

            // Hide typing indicator
            this.hideTypingIndicator();

            if (data.error) {
                this.addMessage('I apologize, but I encountered an error. Please try again.', 'assistant');
            } else {
                // Add assistant response
                this.addMessage(data.message, 'assistant', {
                    suggestions: data.suggestions,
                    products: data.products,
                    promotions: data.promotions,
                    cart: data.cart
                });
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage('I\'m having trouble connecting right now. Please try again in a moment.', 'assistant');
        }

        // Re-enable send button
        this.setSendButtonState(true);
    }

    addMessage(content, sender, extras = {}) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Format message content with markdown-like formatting
        const formattedContent = this.formatMessageContent(content);
        messageContent.innerHTML = formattedContent;

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);

        // Add suggestions if provided
        if (extras.suggestions && extras.suggestions.length > 0) {
            const suggestionsDiv = document.createElement('div');
            suggestionsDiv.className = 'suggestions';
            
            extras.suggestions.forEach(suggestion => {
                const suggestionBtn = document.createElement('button');
                suggestionBtn.className = 'suggestion-btn';
                suggestionBtn.textContent = suggestion;
                suggestionsDiv.appendChild(suggestionBtn);
            });
            
            messageContent.appendChild(suggestionsDiv);
        }

        // Add products grid if provided
        if (extras.products && extras.products.length > 0) {
            const productsGrid = this.createProductsGrid(extras.products);
            messageContent.appendChild(productsGrid);
        }

        // Add promotions if provided
        if (extras.promotions && extras.promotions.length > 0) {
            const promotionsDiv = this.createPromotionsDisplay(extras.promotions);
            messageContent.appendChild(promotionsDiv);
        }

        // Add cart summary if provided
        if (extras.cart && extras.cart.length > 0) {
            const cartDiv = this.createCartDisplay(extras.cart);
            messageContent.appendChild(cartDiv);
        }

        // Remove welcome message if it exists
        const welcomeMessage = this.messagesContainer.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();

        // Store in conversation history
        this.conversationHistory.push({
            content: content,
            sender: sender,
            timestamp: new Date().toISOString(),
            extras: extras
        });
    }

    formatMessageContent(content) {
        // Simple markdown-like formatting
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
            .replace(/\n/g, '<br>') // Line breaks
            .replace(/(\$\d+\.?\d*)/g, '<span style="color: #48bb78; font-weight: 600;">$1</span>') // Price highlighting
            .replace(/(✅|❌|🎉|📱|🛍️|💰|📦)/g, '<span style="font-size: 16px;">$1</span>'); // Emoji styling
    }

    createProductsGrid(products) {
        const grid = document.createElement('div');
        grid.className = 'products-grid';

        products.forEach(product => {
            const card = document.createElement('div');
            card.className = 'product-card';
            
            card.innerHTML = `
                <h4>${product.name}</h4>
                <div class="price">$${product.price}</div>
                <div class="rating">
                    ${'★'.repeat(Math.floor(product.rating || 4))}${'☆'.repeat(5 - Math.floor(product.rating || 4))}
                    ${product.rating || 4.0}
                </div>
            `;
            
            grid.appendChild(card);
        });

        return grid;
    }

    createPromotionsDisplay(promotions) {
        const promotionsDiv = document.createElement('div');
        promotionsDiv.className = 'promotions-display';
        promotionsDiv.style.cssText = `
            margin-top: 15px;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            color: white;
        `;

        const title = document.createElement('h4');
        title.textContent = '🎉 Special Offers for You';
        title.style.cssText = 'margin-bottom: 10px; font-size: 16px;';
        promotionsDiv.appendChild(title);

        promotions.forEach(promo => {
            const promoDiv = document.createElement('div');
            promoDiv.style.cssText = `
                background: rgba(255,255,255,0.1);
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 8px;
            `;
            
            promoDiv.innerHTML = `
                <div style="font-weight: 600; margin-bottom: 4px;">${promo.title}</div>
                <div style="font-size: 12px; opacity: 0.9;">${promo.description}</div>
            `;
            
            promotionsDiv.appendChild(promoDiv);
        });

        return promotionsDiv;
    }

    createCartDisplay(cartItems) {
        const cartDiv = document.createElement('div');
        cartDiv.className = 'cart-display';
        cartDiv.style.cssText = `
            margin-top: 15px;
            padding: 15px;
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
        `;

        const title = document.createElement('h4');
        title.textContent = '🛒 Your Cart';
        title.style.cssText = 'margin-bottom: 10px; color: #2d3748;';
        cartDiv.appendChild(title);

        let total = 0;
        cartItems.forEach(item => {
            const itemDiv = document.createElement('div');
            itemDiv.style.cssText = `
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #e2e8f0;
            `;
            
            const itemPrice = item.price * (item.quantity || 1);
            total += itemPrice;
            
            itemDiv.innerHTML = `
                <span>${item.name} ${item.quantity ? `(${item.quantity})` : ''}</span>
                <span style="font-weight: 600; color: #48bb78;">$${itemPrice.toFixed(2)}</span>
            `;
            
            cartDiv.appendChild(itemDiv);
        });

        const totalDiv = document.createElement('div');
        totalDiv.style.cssText = `
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            font-weight: 700;
            font-size: 16px;
            color: #2d3748;
        `;
        totalDiv.innerHTML = `<span>Total:</span><span style="color: #48bb78;">$${total.toFixed(2)}</span>`;
        cartDiv.appendChild(totalDiv);

        return cartDiv;
    }

    showTypingIndicator() {
        this.isTyping = true;
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isTyping = false;
        this.typingIndicator.style.display = 'none';
    }

    setSendButtonState(enabled) {
        this.sendBtn.disabled = !enabled;
        this.sendBtn.style.opacity = enabled ? '1' : '0.6';
    }

    autoResizeTextarea() {
        const textarea = this.messageInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }

    switchChannel(channel) {
        // Update active channel button
        this.channelButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.channel === channel);
        });

        this.currentChannel = channel;

        // Send channel switch message
        const channelNames = {
            web: 'Web Chat',
            mobile: 'Mobile App',
            whatsapp: 'WhatsApp',
            instore: 'In-Store Kiosk',
            voice: 'Voice Assistant'
        };

        this.addMessage(`Switched to ${channelNames[channel]} mode. How can I help you today?`, 'assistant', {
            suggestions: [
                'Show me products',
                'Check current promotions',
                'Help me find something specific',
                'What\'s new?'
            ]
        });
    }
}

// Global functions for quick actions
function sendQuickMessage(message) {
    if (window.chatInterface) {
        window.chatInterface.sendMessage(message);
    }
}

// Initialize chat interface when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatInterface = new RetailChatInterface();
});

// Handle page visibility changes to manage connection
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        // Page became visible - could refresh data or reconnect
        console.log('Page visible - chat interface active');
    } else {
        // Page hidden - could pause certain activities
        console.log('Page hidden - chat interface paused');
    }
});

// Export for potential external use
window.RetailChatInterface = RetailChatInterface;
