# agent.py

import pika
import json
import requests
import time
from dotenv import load_dotenv
import openai
import os

# Load environment variables from the .env file (for OPENAI_API_KEY)
load_dotenv()

# --- Configuration ---
RABBITMQ_HOST = 'localhost'
# This queue name is created by MassTransit based on your C# record's namespace and name.
# It's crucial that this name matches EXACTLY.
QUEUE_NAME = 'FoodVenikWebApi:AgentJobPayload'
# This is the internal endpoint of your .NET backend.
# Use the static IP we configured.
BACKEND_RESPONSE_URL = 'https://localhost:7160/internal/agent-response'

# This is the new function to replace your old one.
import openai
import os

# Initialize the OpenAI client. It will automatically find the API key
# from the .env file we're about to load.
client = openai.OpenAI()

def process_message(payload):
    """
    This function takes the user's message, sends it to the OpenAI API,
    and returns the model's response.
    """
    user_message = payload['newMessage']
    print(f" [x] Received job for user: {payload['userId']}")
    print(f" [x] New message: {user_message}")

    try:
        # Define the persona and the user's query for the AI model
        messages_for_api = [
            {"role": "system", "content": "Make a small poem (5 rows max) about the messages"},
            {"role": "user", "content": user_message}
        ]

        # Call the OpenAI API
        completion = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=messages_for_api
        )

        agent_answer = completion.choices[0].message.content

    except Exception as e:
        print(f" [!] Error calling OpenAI API: {e}")
        agent_answer = "Sorry, I'm having trouble connecting to my AI brain right now. Please try again later."

    # Return the data in the format the .NET backend expects
    return {
        "userId": payload['userId'],
        "message": agent_answer
    }

def process_messagev2(payload):
    """
    This is where the core logic of the agent goes.
    """
    print(f" [x] Received job for user: {payload['userId']}")
    print(f" [x] New message: {payload['newMessage']}")

    # --- TODO: Add your AI and database logic here ---
    # 1. Understand the user's intent from `newMessage`.
    # 2. Query the RDS database for products, discounts, etc.
    # 3. Generate a helpful response.
    # For now, we'll just fake a response after a delay.
    time.sleep(3)
    agent_answer = f"I processed your message: '{payload['newMessage']}'. Here is some info from the database!"

    return {
        "userId": payload['userId'],
        "message": agent_answer
    }


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # In this publish/subscribe pattern, the exchange name is the same as the queue name
    EXCHANGE_NAME = QUEUE_NAME

    # 1. The consumer should also declare the exchange to ensure it exists.
    #    MassTransit's "Publish" uses a 'fanout' exchange by default.
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout', durable=True)

    # 2. The consumer declares the queue.
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # 3. *** THIS IS THE MISSING STEP ***
    #    Bind the queue to the exchange to receive messages.
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME)

    print(f' [*] Queue "{QUEUE_NAME}" is bound to exchange "{EXCHANGE_NAME}". Waiting for messages.')

    def callback(ch, method, properties, body):
        # Decode the entire envelope
        envelope = json.loads(body.decode())
        
        # Extract your actual payload from the 'message' key
        payload = envelope['message']
        
        # Now the rest of the code will work perfectly
        response_data = process_message(payload)
        try:
            # Note: verify=False is used to ignore SSL certificate errors for local dev.
            requests.post(BACKEND_RESPONSE_URL, json=response_data, verify=False)
            print(f" [>] Sent response for user: {response_data['userId']}")
        except requests.exceptions.RequestException as e:
            print(f" [!] Could not send response to backend: {e}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    main()