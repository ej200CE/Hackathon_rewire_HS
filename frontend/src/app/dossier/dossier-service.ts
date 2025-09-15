// src/app/dossier.service.ts

import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

// 👇 Define the full structure of your user profile object here
export interface UserDossier {
  summary: {
    name: string;
    avatar: string;
    goal: string;
    calorieTarget: number;
    macros: { protein: number; carbs: number; fats: number; };
  };
  goals: {
    age: number;
    sex: string;
    description: string;
    activity: string;
    maintenanceCalories: number;
    estimatedWeeklyChange: string;
  };
  preferences: {
    mealsPerDay: number;
    budget: { perDay: number; perWeek: number; };
    equipment: { [key: string]: boolean; };
    cookingMethods: { [key: string]: boolean; };
    portionSize: string;
    mealPrep: { difficulty: string; cookingTime: string; };
  };
  food: {
    favorites: string[];
    dislikes: string[];
  };
  allergies: string[];
}

@Injectable({
  providedIn: 'root'
})
export class DossierService {
  private readonly _userProfile = new BehaviorSubject<UserDossier | null>(null);
  readonly userProfile$ = this._userProfile.asObservable();

  setProfile(profile: UserDossier) {
    this._userProfile.next(profile);
  }

  getCurrentProfile(): UserDossier | null {
    return this._userProfile.getValue();
  }
}