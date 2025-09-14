using MassTransit;
using FoodVenikWebApi;
using Microsoft.AspNetCore.SignalR;

var builder = WebApplication.CreateBuilder(args);

// --- 1. ADD CORS POLICY ---
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAngularApp",
        policy =>
        {
            // policy.WithOrigins("http://localhost:4200") // Your Angular app's URL
            //        .AllowAnyHeader()
            //        .AllowAnyMethod()
            //        .AllowCredentials(); // Important for SignalR

            policy.SetIsOriginAllowed(_ => true) // Allow any origin during development
            .AllowAnyHeader()
            .AllowAnyMethod()
            .AllowCredentials();
        });


});

// Add MassTransit and configure it to use RabbitMQ
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

// Add SignalR for real-time communication
builder.Services.AddSignalR();

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

//app.UseHttpsRedirection();
app.UseRouting(); // Ensure this is called first
app.UseCors("AllowAngularApp");

app.MapHub<ChatHub>("/chathub");

app.MapPost("/chat", async (UserMessage message, IPublishEndpoint publishEndpoint) =>
{
    // In a real app, you'd get this from an authentication token
    var userId = "user-123";

    // 1. Create the job payload for the agent
    var agentJob = new AgentJobPayload(
        JobId: Guid.NewGuid().ToString(),
        UserId: userId,
        NewMessage: message.Text
    );

    // 2. Publish the job to RabbitMQ using MassTransit
    await publishEndpoint.Publish(agentJob);

    // 3. Respond immediately to the frontend
    //    202 Accepted is the correct HTTP status code for "Your request was accepted and is being processed."
    return Results.Accepted();
});

app.MapPost("/internal/agent-response", 
    async (AgentResponse response, IHubContext<ChatHub> hubContext) =>
{
    // Use the Hub Context to send a message to connected clients
    // "ReceiveMessage" is the event name the frontend will listen for.
    await hubContext.Clients.All.SendAsync("ReceiveMessage", response.Message);

    // Note: Clients.All sends to EVERY connected user. Later, you'll want to
    // send to a specific user with `Clients.User(response.UserId)...` after
    // implementing authentication.

    return Results.Ok();
});

// Placeholder for future API endpoints
app.MapGet("/", () => "API is running!");

app.Run();

