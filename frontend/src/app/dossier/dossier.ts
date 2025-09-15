// src/app/dossier/dossier.ts (Updated)

import { Component, OnInit } from '@angular/core'; // 👈 Import OnInit
import { CommonModule } from '@angular/common';
import { MatTabsModule } from '@angular/material/tabs';

// 👇 1. Import your new service and the UserProfile type
import { DossierService, UserDossier } from './dossier-service';

// Import all the child components
import { DossierSummaryCard } from './dossier-summary-card/dossier-summary-card';
import { UserGoals } from './user-goals/user-goals';
import { GeneralPreferences } from './general-preferences/general-preferences';
import { FoodPreferences } from './food-preferences/food-preferences';
import { Allergies } from './allergies/allergies';

@Component({
  selector: 'app-dossier',
  standalone: true,
  imports: [
    CommonModule,
    MatTabsModule,
    DossierSummaryCard,
    UserGoals,
    GeneralPreferences,
    FoodPreferences,
    Allergies
  ],
  templateUrl: './dossier.html',
  styleUrl: './dossier.css'
})
export class Dossier implements OnInit { // 👈 2. Implement the OnInit lifecycle hook
  // This property will now be populated from the service.
  userProfile!: UserDossier;

  // 👇 3. Inject the DossierService into the constructor
  constructor(private dossierService: DossierService) {}

  // 👇 4. Use ngOnInit to set up the data in the service
  ngOnInit(): void {
    // The profile object is now defined here, inside the setup method.
    const initialProfile: UserDossier = {
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

    // 5. Push this data into the shared service
    this.dossierService.setProfile(initialProfile);

    // 6. Subscribe to the service to get the data for the template
    this.dossierService.userProfile$.subscribe(profile => {
      if (profile) {
        this.userProfile = profile;
      }
    });
  }
}