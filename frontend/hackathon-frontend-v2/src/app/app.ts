import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChatWindow } from "./chat-window/chat-window";
import { Header } from "./header/header";
import { Dossier } from "./dossier/dossier";
import { trigger, state, style, animate, transition } from '@angular/animations';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ChatWindow, Header, Dossier],
  templateUrl: './app.html',
  styleUrl: './app.css',
  
})
export class App {
  showDossier = false;

  protected readonly title = signal('hackathon-frontend-v2');


  onFirstMessageSent() {
    this.showDossier = true;
  }
}
