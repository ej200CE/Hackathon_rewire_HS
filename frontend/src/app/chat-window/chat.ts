// src/app/chat.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as signalR from '@microsoft/signalr';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  // --- IMPORTANT ---
  // Replace this URL with your actual .NET backend's HTTPS URL
  // You can find it in your backend's Properties/launchSettingsCross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at https://172.22.225.165:7160/chathub/negotiate?negotiateVersion=1. (Reason: CORS request did not succeed). Status code: (null).
  private backendUrl = 'http://localhost:5065';
  //private backendUrl = 'https://172.22.225.165:7160';

  private hubConnection!: signalR.HubConnection;

  // Use an RxJS Subject to stream agent messages to components
  public agentMessage$ = new Subject<string>();

  constructor(private http: HttpClient) { }

  // 1. Starts the SignalR connection to the ChatHub
  public startConnection = () => {
    this.hubConnection = new signalR.HubConnectionBuilder()
      .withUrl(`${this.backendUrl}/chathub`)
      .build();

    this.hubConnection
      .start()
      .then(() => console.log('SignalR Connection started'))
      .catch(err => console.error('Error while starting connection: ' + err));

    // Listen for messages from the "ReceiveMessage" event sent by the server
    this.hubConnection.on('ReceiveMessage', (message: string) => {
      this.agentMessage$.next(message);
    });
  }

  // 2. Sends a user's message to the backend's /chat endpoint
  public sendMessage(userMessage: string) {
    const payload = { text: userMessage };
    // This calls the API endpoint that queues the job in RabbitMQ
    return this.http.post(`${this.backendUrl}/chat`, payload);
  }
}