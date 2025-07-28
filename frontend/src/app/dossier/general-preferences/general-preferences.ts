import { Component } from '@angular/core';
import { Pipe } from '@angular/core';
import { FormatEquipmentPipe } from './format-equipment.pipe';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-general-preferences',
  imports: [FormatEquipmentPipe, CommonModule],
  templateUrl: './general-preferences.html',
  styleUrl: './general-preferences.css'
})
export class GeneralPreferences {
 preferences = {
    // Meal structure
    mealsPerDay: 3,
    mealFrequency: 'Regular (3 main meals)', // Options: Fewer, Regular, Snacker
    
    // Budget
    budget: {
      perMeal: 5,
      perDay: 15,
      perWeek: 100
    },
    
    // Equipment
    equipment: {
      oven: true,
      stove: true,
      microwave: true,
      airFryer: false,
      blender: true,
      slowCooker: false
    },
    
    // Cooking preferences
    cookingMethods: {
      raw: true,
      boiled: true,
      fried: false,
      baked: true,
      steamed: true
    },
    
    // Food consistency
    foodConsistency: {
      solid: true,
      liquid: true,
      pureed: false
    },
    
    // Portion sizes
    portionSize: 'Medium', // Small, Medium, Large
    
    // Allergies (would normally come from backend)
    allergies: ['Peanuts', 'Shellfish'],
    
    // Meal prep preferences
    mealPrep: {
      mealsPerBatch: 3,
      difficulty: 'Medium', // Easy, Medium, Hard
      variability: 'Some variation', // Same meals, Some variation, Always different
      cookingTime: '30-45 minutes' // Quick (<30), Medium, Lengthy (>60)
    }
  };

  // Add to your component class
objectEntries(obj: any): {key: string, value: any}[] {
  return Object.keys(obj).map(key => ({key, value: obj[key]}));
}

// Add this to your app module or a shared pipes file
}
