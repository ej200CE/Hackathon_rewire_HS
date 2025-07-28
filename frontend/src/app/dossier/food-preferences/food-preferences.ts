import { Component } from '@angular/core';

@Component({
  selector: 'app-food-preferences',
  imports: [],
  templateUrl: './food-preferences.html',
  styleUrl: './food-preferences.css'
})
export class FoodPreferences {
    foodPreferences = {
    favorites: [
      'Pasta', 'Grilled Chicken', 'Avocado', 
      'Dark Chocolate', 'Berries', 'Salmon',
      'Sweet Potatoes', 'Almonds', 'Greek Yogurt'
    ],
    dislikes: [
      'Liver', 'Brussels Sprouts', 'Black Licorice',
      'Cottage Cheese', 'Tofu', 'Olives',
      'Blue Cheese', 'Anchovies', 'Okra'
    ]
  };

  // Utility function to chunk array for columns
  chunkArray(arr: any[], size: number): any[] {
    return Array.from({ length: Math.ceil(arr.length / size) }, (_, i) =>
      arr.slice(i * size, i * size + size)
    );
  }
}
