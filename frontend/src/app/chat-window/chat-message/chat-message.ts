import { Component, Input} from '@angular/core';

@Component({
  selector: 'app-chat-message',
  imports: [],
  templateUrl: './chat-message.html',
  styleUrl: './chat-message.css'
})
export class ChatMessage {
  @Input({required: true}) message!: {
    sender: string,
    // date: Date,
    text: string
  }

    get messageClass() {
    return this.message.sender === 'agent' ? 'agent-message' : 'user-message';
  }


}
