import { Component, Output, EventEmitter} from '@angular/core';
import { ChatMessage } from './chat-message/chat-message';
import { ChatTextbox } from './chat-textbox/chat-textbox';
import { ViewChild } from '@angular/core';
import { ElementRef } from '@angular/core';
import { AfterViewChecked } from '@angular/core';
import { first } from 'rxjs';
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
    },
    {
      sender: 'user',
      text: 'what do I eat'
    },
    {
      sender: 'agent',
      text: 'healthy, I guess'
    },
  ]


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

    setTimeout(() => {
      this.chatHistory.push({
        sender: 'agent',
        text: 'no food for you today'
      });
    }, 1500);
  }
}
