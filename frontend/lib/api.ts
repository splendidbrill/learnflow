/**
 * API Client - Handles all backend communication
 */

import axios from 'axios';
import type { ExplainRequest, ChatRequest, PatternDetectionRequest } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Book Processing
export async function parseBook(data: {
  pdf_url: string;
  book_id: string;
  book_name: string;
  user_id: string;
}) {
  const response = await api.post('/api/books/parse', data);
  return response.data;
}

// Generate Explanation
export async function generateExplanation(data: ExplainRequest) {
  const response = await api.post('/api/explain', data);
  return response.data;
}

// Chat with AI
export async function chatWithAI(data: ChatRequest) {
  const response = await api.post('/api/chat', data);
  return response.data;
}

// Detect Pattern
export async function detectPattern(data: PatternDetectionRequest) {
  const response = await api.post('/api/patterns/detect', data);
  return response.data;
}

// Health Check
export async function healthCheck() {
  const response = await api.get('/health');
  return response.data;
}

export default api;