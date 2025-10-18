import React, { useEffect, useRef, useState } from 'react';
import { motion, useScroll, useTransform, useMotionValue, useSpring } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import useStore from '../store/useStore';
import { openMessagingApp } from '../config/channels';
import { 
  ShoppingBagIcon, 
  SparklesIcon, 
  ChatBubbleLeftRightIcon,
  TruckIcon,
  CreditCardIcon,
  ShieldCheckIcon,
  BoltIcon,
  HeartIcon,
  StarIcon,
  CheckCircleIcon,
  ArrowRightIcon,
  DevicePhoneMobileIcon,
  GlobeAltIcon,
  BuildingStorefrontIcon,
  MicrophoneIcon
} from '@heroicons/react/24/outline';
import { FaWhatsapp, FaTelegram } from 'react-icons/fa';

const TYPING_PHRASE = 'AI is talking to you';

const ParallaxPreviewCard = ({ preview, index }) => {
  const cardRef = useRef(null);
  const motionX = useMotionValue(0);
  const motionY = useMotionValue(0);
  const x = useSpring(motionX, { stiffness: 120, damping: 16 });
  const y = useSpring(motionY, { stiffness: 120, damping: 16 });
  const rotateX = useTransform(motionY, [-40, 40], [12, -12]);
  const rotateY = useTransform(motionX, [-40, 40], [-12, 12]);

  const handlePointerMove = (event) => {
    if (!cardRef.current) return;
    const bounds = cardRef.current.getBoundingClientRect();
    const offsetX = event.clientX - (bounds.left + bounds.width / 2);
    const offsetY = event.clientY - (bounds.top + bounds.height / 2);
    motionX.set((offsetX / bounds.width) * 160);
    motionY.set((offsetY / bounds.height) * 160);
  };

  const resetTransforms = () => {
    motionX.set(0);
    motionY.set(0);
  };

  return (
    <motion.div
      ref={cardRef}
      onPointerMove={handlePointerMove}
      onPointerLeave={resetTransforms}
      onPointerUp={resetTransforms}
      style={{ rotateX, rotateY, x, y }}
      className={`relative rounded-3xl bg-gradient-to-br ${preview.gradient} p-6 sm:p-8 shadow-2xl text-white backdrop-blur-xl border border-white/10 overflow-hidden`}
    >
      <motion.span
        className="absolute -top-6 -right-4 text-5xl drop-shadow-lg"
        animate={{ y: [0, -8, 0], rotate: [0, 4, 0, -4, 0] }}
        transition={{ duration: 6 + index, repeat: Infinity, ease: 'easeInOut' }}
      >
        {preview.floatingIcon}
      </motion.span>

      <div className="inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs uppercase tracking-widest">
        <span className="h-1.5 w-1.5 rounded-full bg-white" />
        {preview.badge}
      </div>

      <h3 className="mt-6 text-2xl sm:text-3xl font-bold leading-tight tracking-tight">
        {preview.title}
      </h3>
      <p className="mt-3 text-sm sm:text-base text-white/80 leading-relaxed">
        {preview.description}
      </p>

      <div className="mt-6 flex flex-wrap gap-3">
        {preview.highlights.map((item) => (
          <span
            key={item}
            className="rounded-full bg-white/15 px-4 py-1 text-xs font-semibold tracking-wide"
          >
            {item}
          </span>
        ))}
      </div>

      <div className="mt-8 grid grid-cols-2 gap-4 text-left">
        {preview.stats.map((stat) => (
          <div key={stat.label} className="rounded-2xl bg-white/10 px-4 py-3">
            <div className="text-2xl font-bold">{stat.value}</div>
            <div className="text-xs font-medium uppercase tracking-wider text-white/70">
              {stat.label}
            </div>
          </div>
        ))}
      </div>

      <motion.div
        className="pointer-events-none absolute inset-0 opacity-0"
        animate={{ opacity: [0.1, 0.35, 0.1] }}
        transition={{ duration: 5 + index, repeat: Infinity, ease: 'easeInOut' }}
        style={{
          background:
            'radial-gradient(circle at 20% 20%, rgba(255,255,255,0.18), transparent 55%), radial-gradient(circle at 80% 0%, rgba(255,255,255,0.12), transparent 45%)'
        }}
      />
    </motion.div>
  );
};

const HomePage = () => {
  const navigate = useNavigate();
  const { setChannel } = useStore();
  const { scrollYProgress } = useScroll();
  const opacity = useTransform(scrollYProgress, [0, 0.2], [1, 0]);
  const scale = useTransform(scrollYProgress, [0, 0.2], [1, 0.95]);
  const [displayText, setDisplayText] = useState('');
  const [activeStep, setActiveStep] = useState(0);
  const carouselRef = useRef(null);
  const trackRef = useRef(null);
  const [dragWidth, setDragWidth] = useState(0);

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      index += 1;
      setDisplayText(TYPING_PHRASE.slice(0, index));
      if (index >= TYPING_PHRASE.length) {
        clearInterval(interval);
      }
    }, 90);

    return () => clearInterval(interval);
  }, []);

  const handleChannelClick = (channelId) => {
    if (openMessagingApp(channelId)) {
      return;
    }
    
    setChannel(channelId);
    navigate('/chat');
  };

  const features = [
    {
      icon: ChatBubbleLeftRightIcon,
      title: 'AI-Powered Assistant',
      description: 'Chat naturally with our intelligent AI that understands your needs',
      iconColor: 'text-primary-600',
      gradient: 'bg-gradient-to-br from-primary-50/80 via-primary-100/70 to-white'
    },
    {
      icon: ShoppingBagIcon,
      title: 'Smart Recommendations',
      description: 'Get personalized product suggestions based on your preferences',
      iconColor: 'text-secondary-600',
      gradient: 'bg-gradient-to-br from-secondary-50/80 via-secondary-100/70 to-white'
    },
    {
      icon: BoltIcon,
      title: 'Lightning Fast',
      description: 'Real-time inventory updates and instant order processing',
      iconColor: 'text-accent-500',
      gradient: 'bg-gradient-to-br from-accent-50/80 via-accent-100/70 to-white'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Secure & Safe',
      description: 'Bank-level encryption and secure payment processing',
      iconColor: 'text-primary-500',
      gradient: 'bg-gradient-to-br from-primary-50/80 via-primary-100/70 to-white'
    },
    {
      icon: TruckIcon,
      title: 'Fast Delivery',
      description: 'Quick shipping with real-time tracking on all orders',
      iconColor: 'text-secondary-600',
      gradient: 'bg-gradient-to-br from-secondary-50/80 via-white to-secondary-100/70'
    },
    {
      icon: HeartIcon,
      title: 'Customer First',
      description: '24/7 support and hassle-free returns within 30 days',
      iconColor: 'text-accent-500',
      gradient: 'bg-gradient-to-br from-accent-50/80 via-white to-accent-100/70'
    }
  ];

  const productPreviews = [
    {
      badge: 'Live Lookbook',
      title: 'Capsule wardrobe in seconds',
      description: 'Our AI converts your intent into ready-to-shop outfits that stay in sync with live inventory.',
      highlights: ['Real-time availability', 'Personalized fits', 'Trend aware'],
      stats: [
        { value: '12', label: 'AI outfits' },
        { value: '3x', label: 'Faster picks' },
        { value: '98%', label: 'Fit score' },
        { value: 'Live', label: 'Inventory' }
      ],
      floatingIcon: '🪄',
      gradient: 'from-primary-500/90 via-secondary-500/80 to-primary-800'
    },
    {
      badge: 'Smart Cart',
      title: 'Context-aware checkout flow',
      description: 'Bundle promos, loyalty perks, and saved preferences with a single tap—no matter the channel.',
      highlights: ['Auto promos', 'One-tap pay', 'Secure by design'],
      stats: [
        { value: '₹4.2k', label: 'Avg uplift' },
        { value: '35%', label: 'Promo use' },
        { value: '1-tap', label: 'Checkout' },
        { value: 'Shield', label: 'Security' }
      ],
      floatingIcon: '🛒',
      gradient: 'from-secondary-500/80 via-primary-600/70 to-secondary-800'
    },
    {
      badge: 'Omnichannel Sync',
      title: 'WhatsApp to in-store continuity',
      description: 'Switch devices or locations without losing context—carts, preferences, and conversations travel with you.',
      highlights: ['6-channel orchestration', 'Hands-free handoff', 'Persistent carts'],
      stats: [
        { value: '6', label: 'Channels' },
        { value: '99.9%', label: 'Uptime' },
        { value: '45+', label: 'Locales' },
        { value: '24/7', label: 'Concierge' }
      ],
      floatingIcon: '🌐',
      gradient: 'from-primary-700/80 via-slate-900/60 to-secondary-700/75'
    }
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Fashion Enthusiast',
      content: 'The AI assistant helped me find the perfect outfit in minutes! Shopping has never been this easy.',
      rating: 5,
      avatar: '👩‍💼'
    },
    {
      name: 'Michael Chen',
      role: 'Tech Professional',
      content: 'Incredible experience! The recommendations are spot-on and the checkout process is seamless.',
      rating: 5,
      avatar: '👨‍💻'
    },
    {
      name: 'Emily Rodriguez',
      role: 'Busy Mom',
      content: 'I love how I can shop through WhatsApp while multitasking. Game changer for busy parents!',
      rating: 5,
      avatar: '👩‍🦰'
    }
  ];

  const channels = [
    { icon: GlobeAltIcon, name: 'Web Chat', color: 'text-primary-500', channelId: 'web' },
    { icon: DevicePhoneMobileIcon, name: 'Mobile App', color: 'text-secondary-600', channelId: 'mobile' },
    { icon: FaWhatsapp, name: 'WhatsApp', color: 'text-secondary-500', channelId: 'whatsapp' },
    { icon: FaTelegram, name: 'Telegram', color: 'text-primary-400', channelId: 'telegram' },
    { icon: BuildingStorefrontIcon, name: 'In-Store Kiosk', color: 'text-neutral-600', channelId: 'in-store' },
    { icon: MicrophoneIcon, name: 'Voice Assistant', color: 'text-accent-500', channelId: 'voice' }
  ];

  const heroHighlights = [
    { value: '90%', label: 'Queries resolved instantly' },
    { value: '24/7', label: 'AI concierge availability' },
    { value: '₹4.2k', label: 'Avg. order value uplift' }
  ];

  const workflowSteps = [
    {
      step: '01',
      title: 'Ask anything',
      description: 'Describe your style goals through chat, voice, or messaging apps.',
      icon: ChatBubbleLeftRightIcon,
      moments: [
        'Intent detection across chat, voice & messaging',
        'Interactive style quiz captures preferences',
        'Instant sync with your existing profile'
      ]
    },
    {
      step: '02',
      title: 'Get curated looks',
      description: 'Our AI stylist compares trends, stock, and your preferences instantly.',
      icon: SparklesIcon,
      moments: [
        'AI styler assembles shoppable outfits in seconds',
        'Real-time inventory and promotions layered in',
        '3D parallax previews showcase product depth'
      ]
    },
    {
      step: '03',
      title: 'Checkout anywhere',
      description: 'Complete secure payments with saved profiles and tracked delivery.',
      icon: CreditCardIcon,
      moments: [
        'Tap-to-pay links for web, app, and messaging',
        'Digital receipts and live order tracking',
        'Smart follow-ups keep customers engaged'
      ]
    }
  ];

  const activeTimelineStep = workflowSteps[activeStep];

  useEffect(() => {
    const updateDragWidth = () => {
      if (!carouselRef.current || !trackRef.current) {
        setDragWidth(0);
        return;
      }

      const newWidth = trackRef.current.scrollWidth - carouselRef.current.offsetWidth;
      setDragWidth(newWidth > 0 ? newWidth : 0);
    };

    updateDragWidth();

    if (typeof window === 'undefined') {
      return undefined;
    }

    window.addEventListener('resize', updateDragWidth);
    return () => window.removeEventListener('resize', updateDragWidth);
  }, [testimonials.length]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 overflow-hidden">
      {/* Enhanced Background with Gradient */}
      <div className="fixed inset-0 -z-10 bg-gradient-to-br from-primary-50 via-white to-secondary-50" />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-6 py-20">
        <div className="absolute inset-0 -z-10">
          <div className="absolute -top-32 -left-24 h-96 w-96 rounded-full bg-primary-400/20 blur-3xl" />
          <div className="absolute top-32 right-12 h-80 w-80 rounded-full bg-primary-500/20 blur-3xl" />
          <div className="absolute bottom-10 left-1/3 h-60 w-60 rounded-full bg-secondary-400/20 blur-3xl" />
        </div>

        <motion.div 
          style={{ opacity, scale }}
          className="relative max-w-6xl mx-auto text-center"
        >
          {/* Enhanced Badge */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full mb-8 border border-neutral-200 shadow-sm"
          >
            <SparklesIcon className="w-4 h-4 text-primary-500" />
            <span className="text-sm font-medium text-neutral-600">AI Shopping Assistant</span>
          </motion.div>

          {/* Enhanced Main Heading */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-6xl lg:text-7xl font-bold text-neutral-900 mb-4 leading-tight tracking-tight"
          >
            Shop Smarter.
            <br />
            <span className="bg-gradient-to-r from-primary-600 to-secondary-500 bg-clip-text text-transparent">
              Powered by AI.
            </span>
          </motion.h1>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.35 }}
            className="mb-10 flex items-center justify-center gap-3 text-lg font-semibold text-primary-600"
          >
            <span className="font-semibold tracking-wide uppercase text-xs text-primary-400/80">
              Live message
            </span>
            <div className="h-5 w-px bg-primary-200" />
            <span className="font-medium tracking-tight text-primary-700">
              {displayText}
            </span>
            <motion.span
              aria-hidden="true"
              className="inline-block h-5 w-0.5 rounded-full bg-primary-500"
              animate={{ opacity: [1, 0, 1] }}
              transition={{ duration: 0.8, repeat: Infinity, ease: 'easeInOut' }}
            />
          </motion.div>

          {/* Enhanced Subheading */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-xl text-neutral-600 max-w-2xl mx-auto mb-12 leading-relaxed font-light"
          >
            Experience conversational shopping across all your favorite platforms. 
            Natural language search, personalized recommendations, and instant checkout.
          </motion.p>

          {/* Enhanced CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
          >
            <Link to="/chat">
              <motion.button
                whileHover={{ scale: 1.02, boxShadow: "0 10px 30px rgba(124, 58, 237, 0.3)" }}
                whileTap={{ scale: 0.98 }}
                className="group px-8 py-4 bg-gradient-to-r from-primary-600 to-secondary-500 text-white rounded-xl font-semibold transition-all text-base flex items-center gap-3 shadow-lg"
              >
                <ChatBubbleLeftRightIcon className="w-5 h-5" />
                Start Shopping
                <ArrowRightIcon className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </motion.button>
            </Link>
            
            <Link to="/products">
              <motion.button
                whileHover={{ scale: 1.02, borderColor: "#4f46e5" }}
                whileTap={{ scale: 0.98 }}
                className="px-8 py-4 bg-white text-neutral-700 rounded-xl font-semibold border border-neutral-300 hover:border-primary-400 transition-all text-base flex items-center gap-3 shadow-sm hover:shadow-md"
              >
                <ShoppingBagIcon className="w-5 h-5" />
                Browse Products
              </motion.button>
            </Link>
          </motion.div>

          {/* Hero highlight stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.75 }}
            className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-16"
          >
            {heroHighlights.map((item) => (
              <div
                key={item.label}
                className="rounded-2xl border border-primary-200/60 bg-white/85 px-6 py-5 shadow-sm backdrop-blur-sm"
              >
                <div className="text-3xl font-bold text-primary-700">{item.value}</div>
                <div className="mt-2 text-sm font-medium text-neutral-600">{item.label}</div>
              </div>
            ))}
          </motion.div>

          {/* Enhanced Channel Icons */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="flex flex-col items-center gap-6"
          >
            <span className="text-sm font-medium text-neutral-500">Available on 6 channels</span>
            <div className="flex flex-wrap justify-center gap-3">
              {channels.map((channel, index) => {
                const Icon = channel.icon;
                return (
                  <motion.button
                    key={channel.name}
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 1 + index * 0.1 }}
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleChannelClick(channel.channelId)}
                    className="flex items-center gap-2 px-4 py-3 bg-white/85 backdrop-blur-sm hover:bg-white rounded-xl transition-all border border-neutral-200 shadow-sm hover:shadow-md hover:border-primary-200"
                  >
                    <Icon className={`w-5 h-5 ${channel.color}`} />
                    <span className="text-sm font-medium text-neutral-700">{channel.name}</span>
                  </motion.button>
                );
              })}
            </div>
          </motion.div>
        </motion.div>

        {/* Enhanced Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5, duration: 1 }}
          className="absolute bottom-10 left-1/2 transform -translate-x-1/2"
        >
          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-6 h-10 border-2 border-slate-400 rounded-full flex justify-center pt-2"
          >
            <div className="w-1.5 h-3 bg-slate-400 rounded-full" />
          </motion.div>
        </motion.div>
      </section>

      {/* Guided shopping journey timeline */}
      <section className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
            className="flex flex-col gap-6 text-center mb-16"
          >
            <span className="mx-auto inline-flex items-center gap-2 rounded-full border border-primary-200 bg-primary-50 px-4 py-1 text-xs font-semibold uppercase tracking-widest text-primary-600">
              Seamless in three steps
            </span>
            <h2 className="text-4xl md:text-5xl font-bold text-neutral-900">Your Concierge-Led Shopping Journey</h2>
            <p className="mx-auto max-w-2xl text-neutral-600 text-lg">
              From inspiration to doorstep delivery, watch the journey unfold with an interactive, AI-orchestrated timeline.
            </p>
          </motion.div>

          <div className="relative">
            <div className="hidden md:block absolute left-[5%] right-[5%] top-[58px] h-px bg-gradient-to-r from-primary-100 via-neutral-200 to-secondary-100" />
            <div className="relative z-10 flex flex-col md:flex-row gap-6 md:gap-4">
              {workflowSteps.map((step, index) => {
                const Icon = step.icon;
                const isActive = activeStep === index;
                return (
                  <motion.button
                    key={step.title}
                    type="button"
                    onMouseEnter={() => setActiveStep(index)}
                    onFocus={() => setActiveStep(index)}
                    onClick={() => setActiveStep(index)}
                    whileHover={{ y: -6 }}
                    whileTap={{ scale: 0.98 }}
                    className={`group relative flex-1 overflow-hidden rounded-3xl border p-8 text-left backdrop-blur-lg transition-all duration-300 ${
                      isActive
                        ? 'border-primary-200 bg-white/95 shadow-2xl shadow-primary-200/40'
                        : 'border-transparent bg-white/80 shadow-md hover:border-primary-100'
                    }`}
                  >
                    <motion.div
                      layoutId={`timeline-glow-${index}`}
                      animate={{ opacity: isActive ? 1 : 0 }}
                      className="pointer-events-none absolute inset-0 bg-gradient-to-br from-primary-100/60 via-white/40 to-secondary-100/50"
                    />

                    <div className="relative z-10 flex items-center justify-between text-sm font-semibold text-primary-500">
                      <span className="flex items-center gap-3">
                        <span className={`flex h-10 w-10 items-center justify-center rounded-2xl border text-sm font-bold ${isActive ? 'border-primary-300 bg-primary-50 text-primary-600' : 'border-primary-100 bg-white text-primary-400'}`}>
                          {step.step}
                        </span>
                        <span>{step.title}</span>
                      </span>
                      <Icon className={`h-6 w-6 ${isActive ? 'text-secondary-500' : 'text-primary-300'}`} />
                    </div>

                    <p className="relative z-10 mt-4 text-sm md:text-base leading-relaxed text-neutral-600">
                      {step.description}
                    </p>

                    <div className="relative z-10 mt-6 flex flex-wrap gap-2">
                      {step.moments.slice(0, 3).map((moment) => (
                        <span
                          key={moment}
                          className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wider ${
                            isActive ? 'bg-primary-100 text-primary-700' : 'bg-neutral-100 text-neutral-500'
                          }`}
                        >
                          {moment}
                        </span>
                      ))}
                    </div>
                  </motion.button>
                );
              })}
            </div>

            <motion.div
              key={activeTimelineStep.step}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mt-12 overflow-hidden rounded-3xl border border-primary-100 bg-white/90 p-8 shadow-xl backdrop-blur-md"
            >
              <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
                <div>
                  <div className="inline-flex items-center gap-2 rounded-full bg-primary-50 px-4 py-1 text-xs font-semibold uppercase tracking-wider text-primary-600">
                    {activeTimelineStep.step} • {activeTimelineStep.title}
                  </div>
                  <h3 className="mt-4 text-2xl font-semibold text-neutral-900">{activeTimelineStep.description}</h3>
                  <p className="mt-3 text-neutral-600">
                    Your concierge keeps the pace—tap any phase to preview what the AI handles for you.
                  </p>
                </div>
                <motion.div
                  whileHover={{ scale: 1.03 }}
                  className="rounded-2xl border border-primary-100/70 bg-gradient-to-br from-primary-500/10 via-white/40 to-secondary-500/10 px-6 py-5 text-sm text-primary-700 shadow-inner"
                >
                  <div className="text-xs font-semibold uppercase tracking-widest text-primary-500/80">Quick facts</div>
                  <ul className="mt-3 space-y-2">
                    {activeTimelineStep.moments.map((moment) => (
                      <li key={moment} className="flex items-start gap-2 text-sm text-neutral-600">
                        <span className="mt-1 h-2 w-2 rounded-full bg-primary-400" />
                        <span>{moment}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Enhanced Features Section */}
      <section className="relative py-24 px-6 bg-gradient-to-b from-white via-primary-50/40 to-white">
        <div className="absolute inset-x-0 top-1/3 h-72 bg-gradient-to-r from-primary-200/30 via-secondary-200/30 to-primary-200/30 blur-[140px]" />
        <div className="relative max-w-6xl mx-auto grid items-center gap-12 lg:grid-cols-[1.1fr,0.9fr]">
          <div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="mb-12"
            >
              <h2 className="text-4xl font-bold text-neutral-900 mb-4">
                Why Choose Us?
              </h2>
              <p className="text-lg text-neutral-600 max-w-xl">
                A modern retail stack with human warmth—AI conversations, connected channels, and cinematic product previews.
              </p>
            </motion.div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {features.map((feature, index) => {
                const Icon = feature.icon;
                return (
                  <motion.div
                    key={feature.title}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1, duration: 0.6 }}
                    whileHover={{ y: -6, scale: 1.02 }}
                    className="relative overflow-hidden rounded-2xl border border-neutral-200 bg-white/85 p-7 shadow-sm backdrop-blur-sm transition-all hover:border-primary-200 hover:shadow-xl"
                  >
                    <div className={`inline-flex p-3 rounded-xl ${feature.gradient} mb-4`}>
                      <Icon className={`w-6 h-6 ${feature.iconColor}`} />
                    </div>
                    <h3 className="text-xl font-semibold text-neutral-900 mb-3">
                      {feature.title}
                    </h3>
                    <p className="text-neutral-600 leading-relaxed">
                      {feature.description}
                    </p>
                    <motion.div
                      className="pointer-events-none absolute inset-0 opacity-0"
                      whileHover={{ opacity: 0.2 }}
                      transition={{ duration: 0.4 }}
                      style={{
                        background:
                          'radial-gradient(circle at top right, rgba(168,85,247,0.2), transparent 55%)'
                      }}
                    />
                  </motion.div>
                );
              })}
            </div>
          </div>

          <div className="relative grid gap-6">
            <div className="absolute -inset-x-12 -inset-y-10 bg-gradient-to-br from-primary-400/10 via-secondary-400/10 to-primary-500/10 blur-2xl" />
            {productPreviews.map((preview, index) => (
              <ParallaxPreviewCard key={preview.title} preview={preview} index={index} />
            ))}
          </div>
        </div>
      </section>

      {/* Enhanced Stats Section */}
      <section className="py-24 px-6 bg-gradient-to-br from-slate-900 via-purple-900 to-violet-900 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjA1IiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-20" />
        
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 text-center">
            {[
              { value: '50K+', label: 'Happy Customers', icon: HeartIcon },
              { value: '10K+', label: 'Products', icon: ShoppingBagIcon },
              { value: '99.9%', label: 'Uptime', icon: BoltIcon },
              { value: '24/7', label: 'AI Support', icon: ChatBubbleLeftRightIcon }
            ].map((stat, index) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, scale: 0.5 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="text-white"
                >
                  <Icon className="w-12 h-12 mx-auto mb-4 opacity-90 text-secondary-300" />
                  <div className="text-6xl font-black mb-2 bg-gradient-to-r from-white to-secondary-200 bg-clip-text text-transparent">
                    {stat.value}
                  </div>
                  <div className="text-xl font-semibold text-secondary-200">{stat.label}</div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Enhanced Testimonials Section */}
      <section className="py-32 px-6 bg-gradient-to-b from-primary-50/80 to-white">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl lg:text-6xl font-black text-neutral-900 mb-6">
              Loved by Thousands
            </h2>
            <p className="text-xl text-neutral-600 max-w-2xl mx-auto">
              Drag through real stories from customers shopping with our AI concierge every day.
            </p>
          </motion.div>

          <div className="relative">
            <div className="pointer-events-none absolute inset-x-12 top-1/2 h-56 -translate-y-1/2 rounded-full bg-gradient-to-r from-primary-200/30 via-white/40 to-secondary-200/30 blur-3xl" />
            <div
              ref={carouselRef}
              className="relative overflow-hidden rounded-[2.5rem] border border-primary-100/60 bg-white/70 backdrop-blur-lg shadow-lg"
            >
              <motion.div
                ref={trackRef}
                drag="x"
                dragConstraints={{ left: -dragWidth, right: 0 }}
                dragElastic={0.2}
                whileTap={{ cursor: 'grabbing' }}
                className="flex cursor-grab gap-6 px-8 py-12"
              >
                {[...testimonials, ...testimonials].map((testimonial, index) => (
                  <motion.div
                    key={`${testimonial.name}-${index}`}
                    className="relative min-w-[280px] sm:min-w-[340px] lg:min-w-[360px] rounded-3xl border border-neutral-200/60 bg-white/90 p-8 shadow-xl"
                    whileHover={{ y: -8, scale: 1.03 }}
                    transition={{ type: 'spring', stiffness: 200, damping: 18 }}
                  >
                    <div className="flex items-center gap-1 mb-4">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <StarIcon key={i} className="w-5 h-5 fill-amber-400 text-amber-400" />
                      ))}
                    </div>
                    <p className="text-neutral-700 mb-6 leading-relaxed text-lg">
                      "{testimonial.content}"
                    </p>
                    <div className="flex items-center gap-4">
                      <div className="text-4xl drop-shadow-sm">{testimonial.avatar}</div>
                      <div>
                        <div className="font-bold text-neutral-900 text-lg">{testimonial.name}</div>
                        <div className="text-neutral-500">{testimonial.role}</div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* Enhanced Final CTA Section */}
      <section className="py-32 px-6 bg-gradient-to-br from-neutral-950 via-primary-900 to-secondary-800 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjAyIiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-30" />
        
        <div className="max-w-4xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <SparklesIcon className="w-20 h-20 text-secondary-200 mx-auto mb-8" />
            <h2 className="text-5xl lg:text-6xl font-black text-white mb-6">
              Ready to Experience the Future?
            </h2>
            <p className="text-xl text-secondary-100 mb-12 leading-relaxed">
              Join thousands of satisfied customers who are already shopping smarter with AI. 
              Start your journey today and discover a whole new way to shop.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/chat">
                <motion.button
                  whileHover={{ scale: 1.05, boxShadow: "0 20px 40px rgba(255, 255, 255, 0.2)" }}
                  whileTap={{ scale: 0.95 }}
                  className="group px-10 py-5 bg-white text-neutral-900 rounded-2xl font-bold shadow-2xl transition-all text-lg flex items-center gap-3 hover:bg-neutral-100"
                >
                  Get Started Free
                  <ArrowRightIcon className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </motion.button>
              </Link>
              
              <Link to="/products">
                <motion.button
                  whileHover={{ scale: 1.05, backgroundColor: "rgba(255,255,255,0.1)" }}
                  whileTap={{ scale: 0.95 }}
                  className="px-10 py-5 bg-transparent text-white rounded-2xl font-bold border-2 border-white/30 hover:border-white/50 transition-all text-lg backdrop-blur-sm"
                >
                  Explore Products
                </motion.button>
              </Link>
            </div>

            {/* Enhanced Trust Badges */}
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.4, duration: 0.8 }}
              className="mt-16 flex flex-wrap justify-center gap-8 items-center"
            >
              {[
                { icon: ShieldCheckIcon, text: 'Secure Payments' },
                { icon: TruckIcon, text: 'Free Shipping' },
                { icon: CheckCircleIcon, text: '30-Day Returns' }
              ].map((badge, index) => {
                const Icon = badge.icon;
                return (
                  <div key={badge.text} className="flex items-center gap-2 text-secondary-200">
                    <Icon className="w-5 h-5" />
                    <span className="text-sm font-semibold">{badge.text}</span>
                  </div>
                );
              })}
            </motion.div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;