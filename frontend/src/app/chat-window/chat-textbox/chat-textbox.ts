import { Component, Output, EventEmitter } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat-textbox',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './chat-textbox.html',
  styleUrls: ['./chat-textbox.css']
})
export class ChatTextbox {
  @Output() messageSent = new EventEmitter<string>();
  messageText = '';

  onSubmit() {
    if (this.messageText.trim()) {
      this.messageSent.emit(this.messageText.trim());
      this.messageText = '';
    }
  }
}