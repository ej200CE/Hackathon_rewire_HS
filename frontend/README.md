
# Frontend Documentation

## Overview
The frontend is an Angular-based web application that provides a Matrix-themed chat interface with integrated user profiling capabilities. It consists of three main components working together to deliver a seamless user experience for meal planning and dietary management.

## Key Components

### Chat Interface
- **Chat Window**: Real-time messaging interface with agent/user differentiation
- **Message Bubbles**: Themed left/right aligned message containers
- **Text Input**: Matrix-styled input box with submission handling

### User Profile System (Dossier)
- **User Goals**: Displays nutritional targets and fitness objectives
- **General Preferences**: Shows cooking habits, equipment availability, and meal preferences
- **Food Preferences**: Tracks liked/disliked foods and dietary restrictions

### Data Visualization
- Macro nutrient breakdown charts
- Meal plan visualizations
- Interactive preference selectors

## Data Models

### 1. Message Model
```typescript
interface Message {
  id: string;          // Unique message identifier
  sender: 'user' | 'agent'; // Message origin
  text: string;        // Message content
  timestamp?: Date;    // When message was sent
  isTyping?: boolean;  // Visual typing indicator
}
```

### 2. User Profile Model
```typescript
interface UserProfile {
  basicInfo: {
    name: string;
    age: number;
    sex: string;
    avatar: string;    // URL or base64 image
  };
  
  goals: {
    target: 'weight-loss' | 'maintenance' | 'muscle-gain';
    calories: number;
    macros: {
      protein: number; // in grams
      carbs: number;
      fats: number;
    };
  };
  
  preferences: {
    cooking: {
      equipment: string[]; // ['oven', 'airFryer', ...]
      difficulty: 'easy' | 'medium' | 'hard';
      timeAvailable: number; // minutes/day
    };
    food: {
      likes: string[];     // Food items
      dislikes: string[];
      allergies: string[];
      restrictions: string[]; // ['vegetarian', 'gluten-free', ...]
    };
  };
}
```

### 3. Meal Plan Model
```typescript
interface MealPlan {
  id: string;
  dateRange: {
    start: Date;
    end: Date;
  };
  dailyPlans: {
    [date: string]: {
      meals: Meal[];
      nutrients: {
        calories: number;
        protein: number;
        carbs: number;
        fats: number;
      };
    };
  };
}

interface Meal {
  name: string;
  type: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  ingredients: { name: string; amount: string; substitutes: string[]; }[];
  instructions: string[];
  prepTime: number;
  nutrition: {
    calories: number;
    macros: {
      protein: number;
      carbs: number;
      fats: number;
    };
  };
}
```

## Architecture Overview
The Angular application follows a modular structure with:
- Core module for foundational services
- Shared module for common components
- Feature modules for chat, profile, and visualization components
- State management using NgRx for complex state interactions

## Getting Started
1. Clone the repository
2. Install dependencies: `npm install`
3. Run development server: `ng serve`
4. Build for production: `ng build --configuration production`

## Dependencies
- Angular 15+
- RxJS for reactive programming
- Chart.js for data visualization
- Date-fns for date manipulation

## Styling
The application uses SCSS with:
- Matrix-inspired green/black color scheme
- Responsive design patterns
- Angular Material components for UI consistency
