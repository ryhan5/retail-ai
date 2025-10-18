// Channel Configuration for Omnichannel Integration

export const channelConfig = {
  whatsapp: {
    // Twilio WhatsApp Sandbox Number (for testing)
    // Replace with your production WhatsApp Business number
    phoneNumber: '14155238886',
    defaultMessage: 'Hi! I want to shop with your AI assistant.',
    
    // Generate WhatsApp URL
    getUrl: (customMessage) => {
      const message = encodeURIComponent(customMessage || channelConfig.whatsapp.defaultMessage);
      return `https://wa.me/${channelConfig.whatsapp.phoneNumber}?text=${message}`;
    }
  },
  
  telegram: {
    // Your Telegram Bot Username (without @)
    // Create a bot via @BotFather on Telegram
    botUsername: 'YourRetailAIBot', // TODO: Update with actual bot username
    
    // Generate Telegram URL
    getUrl: () => {
      return `https://t.me/${channelConfig.telegram.botUsername}`;
    }
  },
  
  // Instructions for setup
  setup: {
    whatsapp: {
      sandbox: 'Join Twilio WhatsApp Sandbox: https://www.twilio.com/console/sms/whatsapp/sandbox',
      production: 'Apply for WhatsApp Business API: https://www.twilio.com/whatsapp',
      steps: [
        '1. Create a Twilio account',
        '2. Go to WhatsApp Sandbox',
        '3. Send "join <your-sandbox-code>" to the sandbox number',
        '4. Update phoneNumber in this config file'
      ]
    },
    telegram: {
      createBot: 'Message @BotFather on Telegram',
      steps: [
        '1. Open Telegram and search for @BotFather',
        '2. Send /newbot command',
        '3. Follow instructions to create your bot',
        '4. Copy the bot username',
        '5. Update botUsername in this config file',
        '6. Set webhook URL in backend .env file'
      ]
    }
  }
};

// Helper function to open external messaging app
export const openMessagingApp = (channelId, customMessage = null) => {
  if (channelId === 'whatsapp') {
    const url = channelConfig.whatsapp.getUrl(customMessage);
    window.open(url, '_blank');
    return true;
  }
  
  if (channelId === 'telegram') {
    const url = channelConfig.telegram.getUrl();
    window.open(url, '_blank');
    return true;
  }
  
  return false;
};

export default channelConfig;
