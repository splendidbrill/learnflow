'use client';

import { signInWithGoogle } from '@/lib/supabase';
import { Sparkles, BookOpen, Brain, Trophy } from 'lucide-react';

export default function LandingPage() {
  const handleSignIn = async () => {
    try {
      await signInWithGoogle();
    } catch (error) {
      console.error('Error signing in:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center text-white">
          {/* Logo */}
          <div className="mb-8">
            <div className="inline-flex items-center gap-3 bg-white/10 backdrop-blur-lg px-6 py-3 rounded-2xl">
              <Sparkles className="w-8 h-8" />
              <h1 className="text-3xl font-bold">LearnAI</h1>
            </div>
          </div>

          {/* Hero Text */}
          <h2 className="text-5xl md:text-6xl font-bold mb-6">
            Transform Any Textbook Into Your Perfect Learning Experience
          </h2>
          <p className="text-xl md:text-2xl mb-12 text-white/90">
            AI-powered personalized explanations using your interests. Learn faster, remember longer.
          </p>

          {/* CTA Button */}
          <button
            onClick={handleSignIn}
            className="bg-white text-purple-600 px-8 py-4 rounded-xl font-bold text-lg shadow-2xl hover:scale-105 transition-transform"
          >
            Get Started with Google →
          </button>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-8 mt-20">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6">
              <BookOpen className="w-12 h-12 mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2">Smart Book Processing</h3>
              <p className="text-white/80">Upload any PDF textbook and our AI extracts chapters, concepts, and questions automatically.</p>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6">
              <Brain className="w-12 h-12 mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2">Personalized Explanations</h3>
              <p className="text-white/80">Learn using analogies based on your interests - football, cooking, gaming, and more!</p>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6">
              <Trophy className="w-12 h-12 mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2">Track Your Progress</h3>
              <p className="text-white/80">Earn XP, maintain streaks, and level up as you master new concepts.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}