import React from 'react';
import { motion } from 'framer-motion';

const TypingIndicator = () => {
  return (
    <div className="flex items-center space-x-1">
      <span className="text-sm text-gray-600 mr-2">AI Assistant is thinking</span>
      <div className="flex space-x-1">
        {[0, 1, 2].map((index) => (
          <motion.div
            key={index}
            className="w-2 h-2 bg-primary-400 rounded-full"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 1,
              repeat: Infinity,
              delay: index * 0.2,
              ease: "easeInOut",
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default TypingIndicator;
