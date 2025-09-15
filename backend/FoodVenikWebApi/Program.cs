using MassTransit;
using FoodVenikWebApi; // 👈 1. Ensures your records are recognized
using Microsoft.AspNetCore.SignalR;

var builder = WebApplication.CreateBuilder(args);

// --- CORS POLICY ---
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAngularApp",
        policy =>
        {
            policy.SetIsOriginAllowed(_ => true) // For development
            .AllowAnyHeader()
            .AllowAnyMethod()
            .AllowCredentials();
        });
});

// --- SERVICES ---
builder.Services.AddMassTransit(x =>
{
    x.UsingRabbitMq((context, cfg) =>
    {
        cfg.Host("localhost", "/", h => {
            h.Username("guest");
            h.Password("guest");
        });
        cfg.ConfigureEndpoints(context);
    });
});
builder.Services.AddSignalR();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// --- HTTP PIPELINE ---
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
app.UseRouting();
app.UseCors("AllowAngularApp");

// --- API ENDPOINTS ---
app.MapHub<ChatHub>("/chathub");

app.MapPost("/chat", async (ChatMessage message, IPublishEndpoint publishEndpoint) => // 👈 2. Uses the imported ChatMessage record
{
    var userId = "user-123";

    var agentJob = new AgentJobPayload(
        JobId: Guid.NewGuid().ToString(),
        UserId: userId,
        NewMessage: message.Text,
        UserProfile: message.Profile
    );

    await publishEndpoint.Publish(agentJob);

    return Results.Accepted();
});

app.MapPost("/internal/agent-response",
    async (AgentResponse response, IHubContext<ChatHub> hubContext) =>
{
    await hubContext.Clients.All.SendAsync("ReceiveMessage", response.Message);
    return Results.Ok();
});

app.MapGet("/", () => "API is running!");

app.Run();

// 3. Note that the record definitions are no longer here 👇