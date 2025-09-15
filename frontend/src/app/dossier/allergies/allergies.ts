// src/app/dossier/allergies/allergies.ts

import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-allergies',
  standalone: true,
  imports: [CommonModule],
  // --- CORRECTED URL ---
  templateUrl: './allergies.html',
  styleUrl: './allergies.css'
})
// --- CORRECTED CLASS NAME ---
export class Allergies {
  @Input() allergiesData!: string[];
}