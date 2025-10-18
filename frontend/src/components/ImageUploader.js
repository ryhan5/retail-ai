import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  PhotoIcon,
  XMarkIcon,
  PaperAirplaneIcon,
  ArrowUpTrayIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const ImageUploader = ({ onImageSelect, onClose }) => {
  const [selectedImages, setSelectedImages] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files);
    processFiles(files);
  };

  const processFiles = (files) => {
    const imageFiles = files.filter(file => file.type.startsWith('image/'));
    
    if (imageFiles.length === 0) {
      toast.error('Please select valid image files');
      return;
    }

    if (imageFiles.length + selectedImages.length > 5) {
      toast.error('Maximum 5 images allowed');
      return;
    }

    const newImages = [...selectedImages, ...imageFiles];
    setSelectedImages(newImages);

    // Create preview URLs
    const newPreviews = imageFiles.map(file => URL.createObjectURL(file));
    setPreviewUrls(prev => [...prev, ...newPreviews]);

    toast.success(`${imageFiles.length} image(s) added`);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files);
    processFiles(files);
  };

  const removeImage = (index) => {
    URL.revokeObjectURL(previewUrls[index]);
    setSelectedImages(prev => prev.filter((_, i) => i !== index));
    setPreviewUrls(prev => prev.filter((_, i) => i !== index));
    toast.success('Image removed');
  };

  const handleSend = () => {
    if (selectedImages.length === 0) {
      toast.error('Please select at least one image');
      return;
    }

    onImageSelect(selectedImages, previewUrls);
    
    // Clean up
    previewUrls.forEach(url => URL.revokeObjectURL(url));
    onClose();
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ y: 50 }}
        animate={{ y: 0 }}
        className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 className="text-2xl font-bold text-gray-900">Upload Images</h3>
            <p className="text-sm text-gray-600 mt-1">Share product images or screenshots</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <XMarkIcon className="w-6 h-6 text-gray-600" />
          </button>
        </div>

        {/* Upload Area */}
        <div className="flex-1 overflow-y-auto p-6">
          {selectedImages.length === 0 ? (
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-3 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all ${
                isDragging
                  ? 'border-purple-500 bg-purple-50'
                  : 'border-gray-300 hover:border-purple-400 hover:bg-gray-50'
              }`}
            >
              <motion.div
                animate={{ y: isDragging ? -10 : 0 }}
                className="flex flex-col items-center"
              >
                <ArrowUpTrayIcon className={`w-20 h-20 mb-4 ${isDragging ? 'text-purple-500' : 'text-gray-400'}`} />
                <h4 className="text-xl font-semibold text-gray-900 mb-2">
                  {isDragging ? 'Drop images here' : 'Upload Images'}
                </h4>
                <p className="text-gray-600 mb-4">
                  Drag and drop or click to browse
                </p>
                <div className="flex flex-wrap gap-2 justify-center">
                  <span className="px-3 py-1 bg-gray-100 rounded-full text-xs font-medium text-gray-700">
                    JPG
                  </span>
                  <span className="px-3 py-1 bg-gray-100 rounded-full text-xs font-medium text-gray-700">
                    PNG
                  </span>
                  <span className="px-3 py-1 bg-gray-100 rounded-full text-xs font-medium text-gray-700">
                    GIF
                  </span>
                  <span className="px-3 py-1 bg-gray-100 rounded-full text-xs font-medium text-gray-700">
                    WEBP
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-4">
                  Maximum 5 images, up to 10MB each
                </p>
              </motion.div>
            </div>
          ) : (
            <div>
              {/* Image Previews */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
                {previewUrls.map((url, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    className="relative group aspect-square rounded-xl overflow-hidden border-2 border-gray-200"
                  >
                    <img
                      src={url}
                      alt={`Preview ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                    
                    {/* Remove Button */}
                    <motion.button
                      initial={{ opacity: 0 }}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => removeImage(index)}
                      className="absolute top-2 right-2 p-1.5 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"
                    >
                      <XMarkIcon className="w-4 h-4" />
                    </motion.button>

                    {/* Image Info */}
                    <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <p className="text-white text-xs font-medium truncate">
                        {selectedImages[index].name}
                      </p>
                      <p className="text-white text-xs opacity-75">
                        {(selectedImages[index].size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Add More Button */}
              {selectedImages.length < 5 && (
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => fileInputRef.current?.click()}
                  className="w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-xl text-gray-600 hover:border-purple-400 hover:text-purple-600 transition-all flex items-center justify-center gap-2 font-medium"
                >
                  <PhotoIcon className="w-5 h-5" />
                  Add More Images ({5 - selectedImages.length} remaining)
                </motion.button>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 bg-gray-50">
          <div className="flex gap-3">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={onClose}
              className="flex-1 px-6 py-3 bg-white border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition-all"
            >
              Cancel
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleSend}
              disabled={selectedImages.length === 0}
              className={`flex-1 px-6 py-3 rounded-xl font-semibold transition-all flex items-center justify-center gap-2 ${
                selectedImages.length > 0
                  ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg hover:shadow-xl'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              <PaperAirplaneIcon className="w-5 h-5" />
              Send {selectedImages.length > 0 && `(${selectedImages.length})`}
            </motion.button>
          </div>
        </div>

        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          onChange={handleFileSelect}
          className="hidden"
        />
      </motion.div>
    </motion.div>
  );
};

export default ImageUploader;
