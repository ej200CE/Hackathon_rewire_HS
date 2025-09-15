import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTabsModule } from '@angular/material/tabs';

// --- CORRECTED IMPORTS (without 'Component' suffix in class name and '.component' in path) ---
import { DossierSummaryCard } from '../dossier-summary-card/dossier-summary-card';
import { UserGoals } from '../user-goals/user-goals';
import { GeneralPreferences } from '../general-preferences/general-preferences';
import { FoodPreferences } from '../food-preferences/food-preferences';
import { Allergies } from '../allergies/allergies';

@Component({
  selector: 'app-dossier-container',
  standalone: true,
  imports: [
    CommonModule,
    MatTabsModule,
    // --- CORRECTED IMPORTS ARRAY ---
    DossierSummaryCard,
    UserGoals,
    GeneralPreferences,
    FoodPreferences,
    Allergies
  ],
  // --- CORRECTED URL (remove '.component') ---
  templateUrl: './dossier-container.html',
  styleUrl: './dossier-container.css'
})
export class DossierContainer {
  // --- Centralized User Profile Object ---
  // This is the single source of truth for the entire user profile.
  userProfile = {
    summary: {
      name: 'Leha',
      avatar: 'assets/kaban.png',
      goal: 'Muscle Gain',
      calorieTarget: 2800,
      macros: { protein: 180, carbs: 250, fats: 70 }
    },
    goals: {
      age: 45,
      sex: 'Skuf',
      description: 'Focusing on lean muscle development while minimizing fat gain.',
      activity: 'Moderately Active (3-5 workouts/week)',
      maintenanceCalories: 2500,
      estimatedWeeklyChange: '+0.3kg'
    },
    preferences: {
      mealsPerDay: 3,
      budget: { perDay: 15, perWeek: 100 },
      equipment: { oven: true, stove: true, microwave: true, airFryer: false, blender: true, slowCooker: false },
      cookingMethods: { raw: true, boiled: true, fried: false, baked: true, steamed: true },
      portionSize: 'Medium',
      mealPrep: { difficulty: 'Medium', cookingTime: '30-45 minutes' }
    },
    food: {
      favorites: ['Pasta', 'Grilled Chicken', 'Avocado', 'Dark Chocolate', 'Berries', 'Salmon'],
      dislikes: ['Liver', 'Brussels Sprouts', 'Black Licorice', 'Cottage Cheese', 'Tofu']
    },
    allergies: ['Peanuts', 'Shellfish']
  };
}