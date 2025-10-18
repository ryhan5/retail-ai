"""
Agent Registry - Modular Orchestration System
Allows easy addition of new Worker Agents without modifying core code
Example: Adding a Gift Wrapping Agent, Virtual Try-On Agent, etc.
"""

import logging
from typing import Dict, List, Any, Callable, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseWorkerAgent(ABC):
    """
    Base class for all Worker Agents
    New agents should inherit from this class
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the agent's name"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        pass
    
    @abstractmethod
    def can_handle(self, intent: str, context: Dict) -> bool:
        """Determine if this agent can handle the given intent"""
        pass
    
    @abstractmethod
    def process(self, intent: str, message: str, context: Dict) -> Dict:
        """Process the request and return response"""
        pass
    
    def get_priority(self) -> int:
        """Return agent priority (higher = checked first). Default is 50"""
        return 50


class AgentRegistry:
    """
    Central registry for all Worker Agents
    Enables modular addition of new capabilities
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseWorkerAgent] = {}
        self.capabilities_map: Dict[str, List[str]] = {}  # capability -> agent_names
        self.intent_handlers: Dict[str, List[str]] = {}  # intent -> agent_names
        
        logger.info("Agent Registry initialized")
    
    def register_agent(self, agent: BaseWorkerAgent, override: bool = False) -> bool:
        """
        Register a new Worker Agent
        
        Args:
            agent: Instance of BaseWorkerAgent
            override: If True, replace existing agent with same name
        
        Returns:
            bool: True if registered successfully
        """
        agent_name = agent.get_name()
        
        if agent_name in self.agents and not override:
            logger.warning(f"Agent '{agent_name}' already registered. Use override=True to replace.")
            return False
        
        # Register agent
        self.agents[agent_name] = agent
        
        # Map capabilities
        capabilities = agent.get_capabilities()
        for capability in capabilities:
            if capability not in self.capabilities_map:
                self.capabilities_map[capability] = []
            if agent_name not in self.capabilities_map[capability]:
                self.capabilities_map[capability].append(agent_name)
        
        logger.info(f"Registered agent: {agent_name} with capabilities: {capabilities}")
        return True
    
    def unregister_agent(self, agent_name: str) -> bool:
        """Remove an agent from registry"""
        if agent_name not in self.agents:
            logger.warning(f"Agent '{agent_name}' not found in registry")
            return False
        
        # Remove from capabilities map
        agent = self.agents[agent_name]
        for capability in agent.get_capabilities():
            if capability in self.capabilities_map:
                self.capabilities_map[capability].remove(agent_name)
                if not self.capabilities_map[capability]:
                    del self.capabilities_map[capability]
        
        # Remove agent
        del self.agents[agent_name]
        
        logger.info(f"Unregistered agent: {agent_name}")
        return True
    
    def get_agent(self, agent_name: str) -> Optional[BaseWorkerAgent]:
        """Get agent by name"""
        return self.agents.get(agent_name)
    
    def get_agents_for_capability(self, capability: str) -> List[BaseWorkerAgent]:
        """Get all agents that provide a specific capability"""
        agent_names = self.capabilities_map.get(capability, [])
        return [self.agents[name] for name in agent_names if name in self.agents]
    
    def find_handler(self, intent: str, context: Dict) -> Optional[BaseWorkerAgent]:
        """
        Find the best agent to handle a specific intent
        Returns the highest priority agent that can handle the intent
        """
        capable_agents = []
        
        for agent_name, agent in self.agents.items():
            if agent.can_handle(intent, context):
                capable_agents.append((agent.get_priority(), agent))
        
        if not capable_agents:
            return None
        
        # Sort by priority (descending) and return highest
        capable_agents.sort(key=lambda x: x[0], reverse=True)
        return capable_agents[0][1]
    
    def route_request(self, intent: str, message: str, context: Dict) -> Dict:
        """
        Route request to appropriate agent
        Returns response from agent or error if no handler found
        """
        handler = self.find_handler(intent, context)
        
        if not handler:
            logger.warning(f"No agent found to handle intent: {intent}")
            return {
                'success': False,
                'message': 'I\'m not sure how to help with that. Could you rephrase?',
                'intent': intent,
                'handled_by': None
            }
        
        try:
            response = handler.process(intent, message, context)
            response['handled_by'] = handler.get_name()
            return response
        except Exception as e:
            logger.error(f"Error in agent {handler.get_name()}: {str(e)}")
            return {
                'success': False,
                'message': 'I encountered an error processing your request. Please try again.',
                'error': str(e),
                'handled_by': handler.get_name()
            }
    
    def list_agents(self) -> List[Dict]:
        """List all registered agents with their capabilities"""
        return [
            {
                'name': agent.get_name(),
                'capabilities': agent.get_capabilities(),
                'priority': agent.get_priority()
            }
            for agent in self.agents.values()
        ]
    
    def list_capabilities(self) -> Dict[str, List[str]]:
        """List all capabilities and their providers"""
        return self.capabilities_map.copy()
    
    def get_agent_stats(self) -> Dict:
        """Get registry statistics"""
        return {
            'total_agents': len(self.agents),
            'total_capabilities': len(self.capabilities_map),
            'agents': list(self.agents.keys()),
            'capabilities': list(self.capabilities_map.keys())
        }


# Example: Gift Wrapping Agent
class GiftWrappingAgent(BaseWorkerAgent):
    """
    Example of a new modular agent that can be easily added
    Handles gift wrapping, gift messages, and gift receipts
    """
    
    def get_name(self) -> str:
        return "gift_wrapping_agent"
    
    def get_capabilities(self) -> List[str]:
        return ['gift_wrapping', 'gift_message', 'gift_receipt', 'gift_options']
    
    def can_handle(self, intent: str, context: Dict) -> bool:
        gift_keywords = ['gift', 'wrap', 'wrapping', 'present', 'gift message', 'gift receipt']
        return any(keyword in intent.lower() for keyword in gift_keywords)
    
    def process(self, intent: str, message: str, context: Dict) -> Dict:
        """Process gift-related requests"""
        
        # Check if asking about gift options
        if 'option' in message.lower() or 'available' in message.lower():
            return {
                'success': True,
                'message': "🎁 We offer several gift options:\n\n"
                          "• **Premium Gift Wrap** - $5.99\n"
                          "  Elegant wrapping with ribbon and bow\n\n"
                          "• **Standard Gift Wrap** - $2.99\n"
                          "  Classic wrapping paper\n\n"
                          "• **Gift Message Card** - Free\n"
                          "  Personalized message included\n\n"
                          "• **Gift Receipt** - Free\n"
                          "  Price hidden, easy returns\n\n"
                          "Would you like to add any of these to your order?",
                'gift_options': [
                    {'id': 'premium_wrap', 'name': 'Premium Gift Wrap', 'price': 5.99},
                    {'id': 'standard_wrap', 'name': 'Standard Gift Wrap', 'price': 2.99},
                    {'id': 'gift_message', 'name': 'Gift Message', 'price': 0},
                    {'id': 'gift_receipt', 'name': 'Gift Receipt', 'price': 0}
                ],
                'suggestions': [
                    'Add premium gift wrap',
                    'Add gift message',
                    'Add gift receipt',
                    'Skip gift options'
                ]
            }
        
        # Check if adding gift wrap
        elif 'add' in message.lower() or 'yes' in message.lower():
            return {
                'success': True,
                'message': "Perfect! I've added gift wrapping to your order. "
                          "Would you like to include a personalized gift message?",
                'gift_wrap_added': True,
                'suggestions': [
                    'Yes, add a message',
                    'No, that\'s all',
                    'Show gift message examples',
                    'Add gift receipt'
                ]
            }
        
        # Default response
        else:
            return {
                'success': True,
                'message': "I can help you with gift wrapping! We offer premium and standard wrapping options, "
                          "plus free gift messages and gift receipts. What would you like to know?",
                'suggestions': [
                    'Show gift options',
                    'Add gift wrapping',
                    'Write gift message',
                    'Skip gift options'
                ]
            }
    
    def get_priority(self) -> int:
        return 60  # Higher priority for gift-related intents


# Example: Virtual Try-On Agent
class VirtualTryOnAgent(BaseWorkerAgent):
    """
    Example agent for virtual try-on capabilities
    Could integrate with AR/VR technology
    """
    
    def get_name(self) -> str:
        return "virtual_tryon_agent"
    
    def get_capabilities(self) -> List[str]:
        return ['virtual_tryon', 'ar_preview', 'size_recommendation', 'fit_guide']
    
    def can_handle(self, intent: str, context: Dict) -> bool:
        tryon_keywords = ['try on', 'try-on', 'tryon', 'see on me', 'how it looks', 'fit', 'size']
        return any(keyword in intent.lower() for keyword in tryon_keywords)
    
    def process(self, intent: str, message: str, context: Dict) -> Dict:
        """Process virtual try-on requests"""
        
        product = context.get('current_product', {})
        product_name = product.get('name', 'this item')
        
        return {
            'success': True,
            'message': f"🔍 Great idea! You can virtually try on {product_name}. "
                      f"I'll launch our AR try-on experience for you. "
                      f"Make sure to allow camera access when prompted.",
            'action': 'launch_ar_tryon',
            'product': product,
            'features': [
                '360° view of the product',
                'See how it looks on you',
                'Try different colors',
                'Get size recommendations'
            ],
            'suggestions': [
                'Launch AR try-on',
                'See size guide',
                'View customer photos',
                'Add to cart'
            ]
        }
    
    def get_priority(self) -> int:
        return 70  # High priority for try-on requests


# Example: Personal Shopper Agent
class PersonalShopperAgent(BaseWorkerAgent):
    """
    High-touch personal shopping experience
    Provides curated recommendations and styling advice
    """
    
    def get_name(self) -> str:
        return "personal_shopper_agent"
    
    def get_capabilities(self) -> List[str]:
        return ['personal_shopping', 'style_advice', 'outfit_building', 'occasion_shopping']
    
    def can_handle(self, intent: str, context: Dict) -> bool:
        shopper_keywords = ['personal shopper', 'help me shop', 'what should i buy', 
                           'occasion', 'outfit', 'style', 'look good']
        return any(keyword in intent.lower() for keyword in shopper_keywords)
    
    def process(self, intent: str, message: str, context: Dict) -> Dict:
        """Process personal shopping requests"""
        
        customer_name = context.get('customer_name', 'there')
        
        return {
            'success': True,
            'message': f"Hi {customer_name}! I'd love to be your personal shopper today! 👗✨\n\n"
                      f"To give you the best recommendations, tell me:\n"
                      f"• What's the occasion? (work, party, casual, etc.)\n"
                      f"• What's your style? (classic, trendy, casual, formal)\n"
                      f"• Any color preferences?\n"
                      f"• What's your budget?\n\n"
                      f"Or just tell me what you're looking for and I'll curate options for you!",
            'personal_shopper_mode': True,
            'questions': [
                {'question': 'What\'s the occasion?', 'type': 'occasion'},
                {'question': 'What\'s your style?', 'type': 'style'},
                {'question': 'Color preferences?', 'type': 'color'},
                {'question': 'Budget range?', 'type': 'budget'}
            ],
            'suggestions': [
                'Shopping for a wedding',
                'Need work clothes',
                'Casual weekend outfit',
                'Special date night'
            ]
        }
    
    def get_priority(self) -> int:
        return 80  # Very high priority for personal shopping


# Global registry instance
agent_registry = AgentRegistry()


# Helper function to initialize default agents
def initialize_default_agents():
    """Initialize and register default modular agents"""
    
    # Register example agents
    agent_registry.register_agent(GiftWrappingAgent())
    agent_registry.register_agent(VirtualTryOnAgent())
    agent_registry.register_agent(PersonalShopperAgent())
    
    logger.info(f"Initialized {len(agent_registry.agents)} default agents")
    return agent_registry
