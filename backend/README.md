# Project Backend

This directory contains the backend services for our conversational AI application. The backend is designed using a message-driven, asynchronous architecture to ensure responsiveness and scalability.

---
## Core Concept

The backend acts as a bridge between the user-facing frontend and one or more specialized Python "agents." Instead of handling potentially long-running AI and database tasks directly, the main .NET API quickly accepts user requests and places them on a message queue. This allows the frontend to remain fast and responsive, while the Python agents can process the jobs in the background at their own pace.

When an agent finishes its work, it sends the result back to the .NET API, which then pushes the response to the user in real-time.

---
## Architecture Flow

The data flow for a single user message is as follows:

1.  The **Angular Frontend** sends a new chat message **along with the user's current dossier (profile)** via an HTTP POST request to the .NET API.
2.  The **.NET Web API** receives the request, packages the message and dossier into an `AgentJobPayload`, and publishes it to a **RabbitMQ** exchange. It immediately returns a `202 Accepted` response to the frontend.
3.  **RabbitMQ** routes the message from the exchange to a queue.
4.  A **Python Agent**, which is subscribed to the queue, consumes the message.
5.  The Python agent processes the job by **using the user's message and the provided dossier as context** to generate a personalized AI response from the OpenAI API.
6.  After processing, the agent sends the result via an HTTP POST request to an internal endpoint on the **.NET Web API**.
7.  The .NET API receives the result and uses a **SignalR Hub** to push the final message directly to the correct user's browser over a persistent WebSocket connection.

---
## Key Components

* **.NET 8 Web API**: The primary entry point for the frontend. Its responsibilities include:
    * Handling public API requests.
    * Publishing jobs to RabbitMQ (acting as a **Producer**).
    * Hosting the SignalR hub for real-time communication.
    * Receiving results from the Python agents.

* **RabbitMQ**: The message broker that decouples the API from the processing agents. It provides a resilient queue for jobs, ensuring no messages are lost if the agents are busy or offline.

* **Python Agent(s)**: The worker processes that act as **Consumers**. Their responsibilities include:
    * Listening for jobs on the RabbitMQ queue.
    * Executing context-aware logic by leveraging the user's dossier to generate personalized responses from the OpenAI API.
    * Communicating with external services like the OpenAI API.

* **SignalR**: A real-time communication library for .NET that allows the server to push information to clients instantly, which is essential for a chat application.

---
## Getting Started

### Prerequisites

* .NET 8 SDK
* Python 3.10+
* Docker Desktop
* An OpenAI API key

### Running the Backend

1.  **Start RabbitMQ**: Run the message broker in Docker.
    ```bash
    docker run -d --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    ```

2.  **Configure the Python Agent**:
    * Navigate to the `backend/sample-agent` directory.
    * Create a `.env` file and add your OpenAI API key: `OPENAI_API_KEY="sk-..."`
    * Create a virtual environment and install dependencies: `pip install -r requirements.txt`

3.  **Run the .NET API**:
    * Navigate to the `backend/FoodVenikWebApi` directory.
    * Run the server using the `https` profile to enable SSL.
    ```bash
    dotnet run --launch-profile https
    ```

4.  **Run the Python Agent**:
    * In a new terminal, navigate to the `backend/sample-agent` directory.
    * Run the agent script.
    ```bash
    python agent.py
    ```

With all services running, the backend is now fully operational.

---
## To Do / Future Work

This project has a functional end-to-end pipeline. The following is a list of planned features and improvements to enhance its capabilities.

### 🤖 Agent Enhancements

-   [ ] **Implement Database Integration**: Connect the Python agent to a database to fetch real-time product and nutritional information.
-   [ ] **Advanced Prompt Engineering**: Improve the system prompt sent to OpenAI to make better use of database context (a basic form of Retrieval-Augmented Generation - RAG).
-   [ ] **Implement Conversation History**: Modify the `AgentJobPayload` to include the last few messages so the agent can understand the context of the conversation.
-   [ ] **Add functionality for the AI agent to suggest and apply updates to the user dossier.** (Requires backend support for persistent storage).

### ⚙️ Backend Improvements

-   [ ] **Implement User Authentication**: Add a proper authentication system (e.g., JWT) to manage users instead of using a hardcoded `userId`.
-   [ ] **Persistent User Dossiers**: Implement database storage for user dossiers to allow for creation, reading, and updating.
-   [ ] **User-Specific SignalR Messaging**: Change `Clients.All.SendAsync` to `Clients.User(userId).SendAsync` to ensure responses are sent only to the correct user.
-   [ ] **Configuration Management**: Move hardcoded URLs and settings into `appsettings.json` and a Python config file.
-   [ ] **Dead-Letter Queue**: Configure RabbitMQ with a dead-letter queue to handle messages that repeatedly fail processing.

### 🎨 Frontend Features

-   [ ] **Implement manual editing of the user dossier.**
-   [ ] **Fix AI response formatting in the chat window** (e.g., properly render markdown, lists, and code blocks).
-   [ ] **Improve the Profile Visualization**: Create a more interactive UI for the dossier, allowing users to easily see their generated nutritional and preference data.
-   [ ] **"Agent is Typing..." Indicator**: Show a typing indicator after a user sends a message and before the agent's response is received.
-   [ ] **Error Handling**: Display user-friendly messages if the backend connection fails.

### 🚀 DevOps / Infrastructure

-   [ ] **Setup a CI/CD Pipeline**: Create an automated pipeline (e.g., using GitHub Actions) to build, test, and deploy the backend services and the frontend application.