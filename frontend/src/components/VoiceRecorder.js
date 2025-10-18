import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  MicrophoneIcon,
  StopIcon,
  CheckCircleIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const VoiceRecorder = ({ onTranscript, onClose }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setAudioBlob(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingTime(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

      toast.success('Recording started', { icon: '🎤' });
    } catch (error) {
      console.error('Error accessing microphone:', error);
      toast.error('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      toast.success('Recording stopped', { icon: '⏹️' });
    }
  };

  const handleSend = async () => {
    if (!audioBlob) return;

    // In a real implementation, you would:
    // 1. Upload the audio to your backend
    // 2. Use a speech-to-text API (Google Cloud Speech-to-Text, Azure, etc.)
    // 3. Return the transcript

    // For now, simulate transcript
    const simulatedTranscript = "I want to buy a laptop with 16GB RAM";
    
    toast.promise(
      new Promise((resolve) => setTimeout(resolve, 1500)),
      {
        loading: 'Converting speech to text...',
        success: 'Voice message processed!',
        error: 'Failed to process voice message',
      }
    ).then(() => {
      onTranscript(simulatedTranscript);
      onClose();
    });
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      onClick={onClose}
    >
      <motion.div
        initial={{ y: 50 }}
        animate={{ y: 0 }}
        className="bg-white rounded-3xl p-8 shadow-2xl max-w-md w-full mx-4"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-bold text-gray-900">Voice Message</h3>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <XMarkIcon className="w-6 h-6 text-gray-600" />
          </button>
        </div>

        {/* Recording Visualization */}
        <div className="flex flex-col items-center mb-6">
          {!isRecording && !audioBlob && (
            <motion.div
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={startRecording}
              className="relative w-32 h-32 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center cursor-pointer shadow-xl"
            >
              <MicrophoneIcon className="w-16 h-16 text-white" />
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute inset-0 border-4 border-purple-400 rounded-full opacity-50"
              />
            </motion.div>
          )}

          {isRecording && (
            <div className="flex flex-col items-center">
              <motion.div
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="relative w-32 h-32 bg-gradient-to-br from-red-500 to-pink-500 rounded-full flex items-center justify-center shadow-xl"
              >
                <MicrophoneIcon className="w-16 h-16 text-white" />
              </motion.div>
              
              {/* Recording Timer */}
              <div className="mt-4 text-3xl font-bold text-gray-900">
                {formatTime(recordingTime)}
              </div>
              
              {/* Sound Wave Animation */}
              <div className="flex items-center gap-1 mt-4">
                {[...Array(5)].map((_, i) => (
                  <motion.div
                    key={i}
                    animate={{ 
                      height: ['20px', '40px', '20px'],
                      backgroundColor: ['#8B5CF6', '#3B82F6', '#8B5CF6']
                    }}
                    transition={{ 
                      duration: 0.6, 
                      repeat: Infinity,
                      delay: i * 0.1
                    }}
                    className="w-2 rounded-full"
                  />
                ))}
              </div>
            </div>
          )}

          {audioBlob && !isRecording && (
            <div className="flex flex-col items-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="w-32 h-32 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center shadow-xl"
              >
                <CheckCircleIcon className="w-16 h-16 text-white" />
              </motion.div>
              <div className="mt-4 text-lg font-semibold text-gray-700">
                Recording Complete: {formatTime(recordingTime)}
              </div>
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="text-center mb-6">
          {!isRecording && !audioBlob && (
            <p className="text-gray-600">
              Tap the microphone to start recording your message
            </p>
          )}
          {isRecording && (
            <p className="text-gray-600">
              Speak clearly into your microphone...
            </p>
          )}
          {audioBlob && (
            <p className="text-gray-600">
              Your voice will be converted to text and sent
            </p>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          {isRecording ? (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={stopRecording}
              className="flex-1 px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2"
            >
              <StopIcon className="w-5 h-5" />
              Stop Recording
            </motion.button>
          ) : audioBlob ? (
            <>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={startRecording}
                className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition-all"
              >
                Re-record
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSend}
                className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2"
              >
                <CheckCircleIcon className="w-5 h-5" />
                Send
              </motion.button>
            </>
          ) : (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onClose}
              className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition-all"
            >
              Cancel
            </motion.button>
          )}
        </div>

        {/* Help Text */}
        <div className="mt-4 text-xs text-gray-500 text-center">
          💡 Tip: Make sure to allow microphone access in your browser
        </div>
      </motion.div>
    </motion.div>
  );
};

export default VoiceRecorder;
