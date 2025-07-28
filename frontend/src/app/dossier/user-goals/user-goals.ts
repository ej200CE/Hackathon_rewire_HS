import { Component } from '@angular/core';

@Component({
  selector: 'app-user-goals',
  imports: [],
  templateUrl: './user-goals.html',
  styleUrl: './user-goals.css'
})
export class UserGoals {

  /* Dossier container - prevent unnecessary scroll */
  user = {
    name: 'Leha',
    age: 45,
    sex: 'Skuf',
    // avatar: '👨', // or use image path
    avatar: 'assets/kaban.png',
    goal: 'Muscle Gain',
    description: 'Focusing on lean muscle development while minimizing fat gain',
    macros: {
      protein: 180,
      carbs: 250,
      fats: 70,
      ratio: [0.35, 0.45, 0.20] // Protein/Carbs/Fats ratio
    },
    activity: 'Moderately Active (3-5 workouts/week)',
    maintenanceCalories: 2500,
    calorieTarget: 2800, // +300 surplus
    estimatedWeeklyChange: '+0.3kg'
  };

}
