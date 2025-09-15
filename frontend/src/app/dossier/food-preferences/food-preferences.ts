import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

// Define the type for the food data
type FoodData = {
  favorites: string[];
  dislikes: string[];
};

@Component({
  selector: 'app-food-preferences',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './food-preferences.html',
  styleUrl: './food-preferences.css'
})
export class FoodPreferences {
  // @Input() receives the food data from the parent component
  @Input() foodData!: FoodData;
}