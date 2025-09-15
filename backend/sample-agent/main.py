import pika
import json
import requests
import time
from dotenv import load_dotenv
import openai
import os

# Load environment variables from .env file for OPENAI_API_KEY
load_dotenv()

# --- Configuration ---
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'FoodVenikWebApi:AgentJobPayload'
BACKEND_RESPONSE_URL = 'https://localhost:7160/internal/agent-response'

# Initialize the OpenAI client
client = openai.OpenAI()


def generate_food_recommendation(payload):
    """
    Acts as a nutritionist/coach to provide food recommendations based on the user's dossier.
    Handles cases where the dossier might be missing.
    """
    user_id = payload['userId']
    user_message = payload['newMessage']
    # 👇 Safely get the userProfile. It will be None if the key doesn't exist.
    user_profile = payload.get('userProfile')

    print(f" [✅] Received job for user: {user_id}")
    print(f" [💬] User Query: {user_message}")

    try:
        # --- THIS IS THE NEW LOGIC ---
        # Check if the user profile exists and is not empty
        if user_profile:
            print(f" [👤] User Profile Loaded. Goal: {user_profile.get('summary', {}).get('goal', 'N/A')}")
            
            # 1. System Prompt for a PERSONALIZED response
            system_prompt = """
            You are an expert nutritionist and encouraging fitness coach. Your role is to provide personalized,
            practical, and safe food recommendations. You will be given a user's detailed profile as a JSON object
            and their specific question.
            **Your Rules:**
            1.  **Strictly Adhere to the Profile:** All recommendations MUST be based on the user's provided profile.
            2.  **Safety First:** Explicitly mention and respect all allergies listed.
            3.  **Keep it Concise:** Provide clear, direct answers.
            """

            # 2. User Prompt with the full profile context
            user_prompt = f"""
            Here is the user's profile:
            ```json
            {json.dumps(user_profile, indent=2)}
            ```
            Based strictly on the profile above, please answer the following question: "{user_message}"
            """
        else:
            # Fallback logic if the profile is missing
            print(" [⚠️] User profile is missing. Providing a generic response.")
            
            # 1. System Prompt for a GENERIC response
            system_prompt = """
            You are a helpful nutritionist and food assistant. Answer the user's question about food or recipes
            in a general, helpful way. The user's specific profile was not available.
            """
            
            # 2. User Prompt is just their direct question
            user_prompt = user_message
        
        # 3. Call the OpenAI API with the chosen prompts
        completion = client.chat.completions.create(
          model="gpt-4-turbo-preview",
          messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
          ]
        )
        agent_answer = completion.choices[0].message.content

    except Exception as e:
        print(f" [!] Error calling OpenAI API: {e}")
        agent_answer = "Sorry, my AI brain is a bit scrambled right now. Please try again."

    return { "userId": user_id, "message": agent_answer }


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    EXCHANGE_NAME = QUEUE_NAME

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout', durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME)
    print(f' [*] Queue "{QUEUE_NAME}" is bound and waiting for messages.')

    def callback(ch, method, properties, body):
        try:
            envelope = json.loads(body.decode())
            payload = envelope['message']
            response_data = generate_food_recommendation(payload)
            requests.post(BACKEND_RESPONSE_URL, json=response_data, verify=False)
            print(f" [>] Sent response for user: {response_data['userId']}")
        except Exception as e:
            print(f" [!] An error occurred in the callback: {e}")
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    main()