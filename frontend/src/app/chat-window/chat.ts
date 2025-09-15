// src/app/chat.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as signalR from '@microsoft/signalr';
import { Subject } from 'rxjs';
import { DossierService } from '../dossier/dossier-service'; // 👈 1. Import the DossierService

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private backendUrl = 'http://localhost:5065';
  private hubConnection!: signalR.HubConnection;
  public agentMessage$ = new Subject<string>();

  // 👇 2. Inject the DossierService in the constructor
  constructor(private http: HttpClient, private dossierService: DossierService) { }

  // This method remains unchanged
  public startConnection = () => {
    this.hubConnection = new signalR.HubConnectionBuilder()
      .withUrl(`${this.backendUrl}/chathub`)
      .build();

    this.hubConnection
      .start()
      .then(() => console.log('SignalR Connection started'))
      .catch(err => console.error('Error while starting connection: ' + err));

    this.hubConnection.on('ReceiveMessage', (message: string) => {
      this.agentMessage$.next(message);
    });
  }

  // 👇 3. Update the sendMessage method to include the profile
  public sendMessage(userMessage: string) {
    // Get the current user profile from the DossierService
    const userProfile = this.dossierService.getCurrentProfile();

    // Create the new payload including both the text and the profile
    const payload = {
      text: userMessage,
      profile: userProfile
    };

    // Send the complete payload to the backend
    return this.http.post(`${this.backendUrl}/chat`, payload);
  }
}