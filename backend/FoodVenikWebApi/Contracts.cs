using System.Text.Json; // 👈 Add this for JsonElement

namespace FoodVenikWebApi;

// 1. This new record replaces the old 'UserMessage' record.
//    It matches the payload coming from the Angular frontend.
public record ChatMessage(string Text, JsonElement Profile);

// 2. The job payload is updated to include the user's profile.
//    This is the data that gets sent to RabbitMQ for the agent.
public record AgentJobPayload(string JobId, string UserId, string NewMessage, JsonElement UserProfile);

// This record is for the agent's response and does not need to be changed.
public record AgentResponse(string UserId, string Message);