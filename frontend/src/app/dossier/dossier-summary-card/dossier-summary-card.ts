import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

// Define a type for the incoming data for better code quality
type SummaryData = {
  name: string;
  avatar: string;
  goal: string;
  calorieTarget: number;
  macros: { protein: number; carbs: number; fats: number; };
};

@Component({
  selector: 'app-dossier-summary-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dossier-summary-card.html',
  styleUrl: './dossier-summary-card.css'
})
export class DossierSummaryCard {
  // Use @Input() to receive the summaryData from the parent container.
  // The '!' tells TypeScript that this property will be initialized by the parent.
  @Input() summaryData!: SummaryData;
}