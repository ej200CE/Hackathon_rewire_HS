using Microsoft.AspNetCore.SignalR;

public class ChatHub : Hub
{
    // This is a placeholder method to show how the hub can be called.
    // In our final design, the server will PUSH messages, not receive them this way.
    public async Task SendMessage(string user, string message)
    {
        await Clients.All.SendAsync("ReceiveMessage", user, message);
    }
}