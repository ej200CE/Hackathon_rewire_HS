namespace FoodVenikWebApi;

// The message object coming from the frontend
public record UserMessage(string Text);

// The job payload we will send to RabbitMQ for the agent
public record AgentJobPayload(string JobId, string UserId, string NewMessage);

public record AgentResponse(string UserId, string Message);