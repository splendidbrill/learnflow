/**
 * TypeScript Types for the Application
 */

// Enums
export enum BookType {
    PHYSICS = 'physics',
    CHEMISTRY = 'chemistry',
    BIOLOGY = 'biology',
    MATH = 'math',
    ENGLISH = 'english',
    LITERATURE = 'literature',
    HISTORY = 'history',
    GEOGRAPHY = 'geography',
    CIVICS = 'civics',
    SELF_IMPROVEMENT = 'self_improvement',
  }
  
  export enum ContentBlockType {
    PARAGRAPH = 'paragraph',
    DIAGRAM = 'diagram',
    EXAMPLE_QUESTION = 'example_question',
    PRACTICE_QUESTION = 'practice_question',
    SOLUTION = 'solution',
  }
  
  export enum Mode {
    EXPLAIN = 'explain',
    VERIFY = 'verify',
    CONNECT = 'connect',
    STORY = 'story',
    ADAPTIVE = 'adaptive',
  }
  
  // Database Types
  export interface User {
    id: string;
    email: string;
    name: string;
    age?: number;
    gender?: string;
    country?: string;
    state?: string;
    city?: string;
    school?: string;
    interest?: string;
    created_at: string;
  }
  
  export interface Subject {
    id: string;
    user_id: string;
    name: string;
    description?: string;
    created_at: string;
  }
  
  export interface Book {
    id: string;
    subject_id: string;
    user_id: string;
    name: string;
    author: string;
    pdf_url: string;
    category: BookType;
    processing_status: 'pending' | 'processing' | 'completed' | 'failed';
    created_at: string;
  }
  
  export interface Chapter {
    id: string;
    book_id: string;
    chapter_number: number;
    title: string;
    content?: string;
    order_index: number;
    created_at: string;
  }
  
  export interface ContentBlock {
    id: string;
    chapter_id: string;
    type: ContentBlockType;
    order_index: number;
    original_content: string;
    diagram_url?: string;
    diagram_description?: string;
    personalized_explanation?: string;
    diagram_explanation?: string;
    pattern_insight?: string;
    difficulty_level?: 'easy' | 'medium' | 'hard';
    estimated_time?: number;
    created_at: string;
  }
  
  export interface Progress {
    id: string;
    user_id: string;
    content_block_id: string;
    status: 'not_started' | 'in_progress' | 'clarifying' | 'completed' | 'skipped';
    started_at?: string;
    completed_at?: string;
    time_spent: number;
    xp_earned: number;
    created_at: string;
  }
  
  export interface Gamification {
    user_id: string;
    total_xp: number;
    current_streak: number;
    longest_streak: number;
    last_study_date?: string;
    level: number;
    created_at: string;
  }
  
  // API Request Types
  export interface ExplainRequest {
    content_block_id: string;
    user_id: string;
    user_name: string;
    user_age: number;
    user_interests: string[];
    book_name: string;
    book_type: BookType;
    chapter_number: number;
    chapter_title: string;
    content_block_type: ContentBlockType;
    original_content: string;
    diagram_description?: string;
    mode: Mode;
    conversation_history?: Array<{ role: string; content: string }>;
    recently_learned?: string[];
  }
  
  export interface ChatRequest {
    content_block_id: string;
    user_id: string;
    user_name: string;
    user_interests: string[];
    original_content: string;
    question: string;
    conversation_history: Array<{ role: string; content: string }>;
  }
  
  export interface PatternDetectionRequest {
    book_id: string;
    chapter_id: string;
    example_problems: Array<{ problem: string; solution: string }>;
    user_interest: string;
  }
  
  // API Response Types
  export interface ExplanationResponse {
    mode: string;
    explanation: {
      summary: string;
      personalized: string;
      diagram?: {
        what: string;
        how: string;
        why: string;
        interactive_elements: string[];
      };
      pattern?: {
        name: string;
        recognition_cues: string;
        steps: Array<{ step: number; action: string; reasoning: string }>;
        analogy: string;
        common_mistakes: string[];
      };
    };
    verify_question?: {
      question: string;
      correct_answer: string;
      correct_response: string;
      incorrect_response: string;
      hint: string;
    };
    connections?: Array<{ concept: string; relationship: string }>;
    metadata: {
      difficulty_level: string;
      estimated_time: string;
      prerequisites?: string[];
      next_concepts?: string[];
    };
  }
  
  export interface ChatResponse {
    answer: string;
  }
  
  export interface PatternCardResponse {
    pattern_name: string;
    recognition_cues: string;
    steps: Array<{ step: number; action: string; reasoning: string }>;
    analogy: string;
    common_mistakes: string[];
  }