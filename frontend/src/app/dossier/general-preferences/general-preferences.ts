import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TitleCasePipe } from '@angular/common'; // Import TitleCasePipe
import { FormatEquipmentPipe } from './format-equipment.pipe'; // Assuming you still have this pipe

// Define a type for the incoming data. Note that 'allergies' is intentionally omitted.
type PreferencesData = {
  mealsPerDay: number;
  budget: { perDay: number; perWeek: number; };
  equipment: { [key: string]: boolean; };
  cookingMethods: { [key: string]: boolean; };
  portionSize: string;
  mealPrep: { difficulty: string; cookingTime: string; };
};

@Component({
  selector: 'app-general-preferences',
  standalone: true,
  imports: [CommonModule, FormatEquipmentPipe, TitleCasePipe], // Add TitleCasePipe to imports
  templateUrl: './general-preferences.html',
  styleUrl: './general-preferences.css'
})
export class GeneralPreferences {
  // @Input() receives the preferences-specific data from the parent component
  @Input() preferencesData!: PreferencesData;

  // This helper function is still useful for iterating over objects in the template
  objectEntries(obj: any): { key: string, value: any }[] {
    return Object.keys(obj).map(key => ({ key, value: obj[key] }));
  }
}