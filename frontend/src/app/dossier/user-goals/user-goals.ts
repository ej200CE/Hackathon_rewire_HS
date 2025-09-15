import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

// Define a type for the component's expected data
type GoalsData = {
  age: number;
  sex: string;
  description: string;
  activity: string;
  maintenanceCalories: number;
  estimatedWeeklyChange: string;
};

@Component({
  selector: 'app-user-goals',
  standalone: true, // Assuming standalone
  imports: [CommonModule],
  templateUrl: './user-goals.html',
  styleUrl: './user-goals.css'
})
export class UserGoals {
  // @Input() receives the goal-specific data from the parent component
  @Input() goalsData!: GoalsData;
}