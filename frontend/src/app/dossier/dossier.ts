import { Component } from '@angular/core';
import { UserGoals } from './user-goals/user-goals';
import { GeneralPreferences } from './general-preferences/general-preferences';
import { FoodPreferences } from './food-preferences/food-preferences';

@Component({
  selector: 'app-dossier',
  imports: [UserGoals, GeneralPreferences, FoodPreferences],
  templateUrl: './dossier.html',
  styleUrl: './dossier.css'
})
export class Dossier {

}
