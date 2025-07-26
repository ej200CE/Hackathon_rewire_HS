// src/app/shared/pipes/format-equipment.pipe.ts
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'formatEquipment',
  standalone: true // Mark as standalone if using standalone components
})
export class FormatEquipmentPipe implements PipeTransform {
  transform(value: string): string {
    if (!value) return value;
    return value
      .replace(/([A-Z])/g, ' $1') // Add space before capital letters
      .replace(/^./, str => str.toUpperCase()) // Capitalize first letter
      .replace(' Air Fryer', ' AirFryer'); // Special case for AirFryer
  }
}