import { Component, Output, EventEmitter} from '@angular/core';
import { ChatMessage } from './chat-message/chat-message';
import { ChatTextbox } from './chat-textbox/chat-textbox';
import { ViewChild } from '@angular/core';
import { ElementRef } from '@angular/core';
import { AfterViewChecked } from '@angular/core';
import { first } from 'rxjs';
import { ChatService } from './chat';

@Component({
  selector: 'app-chat-window',
  imports: [ChatMessage, ChatTextbox],
  templateUrl: './chat-window.html',
  styleUrl: './chat-window.css'
})
export class ChatWindow {
   @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

   initialMessageSent = false;
   @Output() firstMessage = new EventEmitter<void>();

  chatHistory = [
    {
      sender: 'agent',
      text: 'Welcome to the chat bot'
    }
  ]

      // Inject the ChatService in the constructor
  constructor(private chatService: ChatService) {}

    // Start the connection and subscribe to messages when the component loads
    ngOnInit(): void {
      this.chatService.startConnection();
      this.chatService.agentMessage$.subscribe(agentMessage => {
        this.chatHistory.push({
          sender: 'agent',
          text: agentMessage
        });
      });
    }


   ngAfterViewChecked() {
    this.scrollToBottom();
  }

   private scrollToBottom(): void {
    try {
      const container = this.messagesContainer.nativeElement;
      container.scrollTop = container.scrollHeight;
    } catch(err) { console.error(err); }
  }

  handleNewMessage(message: string) {
    if (!this.initialMessageSent) {
      this.initialMessageSent = true;
      this.firstMessage.emit();
    }

    this.chatHistory.push({
      sender: 'user',
      text: message
    });

    // setTimeout(() => {
    //   this.chatHistory.push({
    //     sender: 'agent',
    //     text: 'no food for you today'
    //   });
    // }, 1500);
          // --- REPLACE THE FAKE TIMEOUT ---
      // Send the message to the backend via the service
      this.chatService.sendMessage(message).subscribe({
        next: () => console.log('Message sent to backend.'),
        error: (err) => console.error('Error sending message:', err)
      });
  }
}
