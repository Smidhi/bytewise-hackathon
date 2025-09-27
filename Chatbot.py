import os
import datetime
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
Username = os.getenv("Username", "User")
Assistantname = os.getenv("Assistantname", "Jarvis")
GroqAPIKEY = os.getenv("GroqAPIKEY")

# Check if API key is set correctly
if not GroqAPIKEY:
    raise ValueError("Groq API Key is missing. Check your .env file.")

# Initialize Groq client
client = Groq(api_key=GroqAPIKEY)

# System message for chatbot behavior
System = f"""Hello, I am {Username}. You are an advanced AI chatbot named {Assistantname}, with real-time up-to-date information.
*** Rules: ***
1️⃣ Do not tell the time unless asked.
2️⃣ Keep responses concise and to the point.
3️⃣ Always reply in English, even if the question is in Hindi.
4️⃣ Do not provide notes, just direct answers.
"""

SystemChatBot = [{"role": "system", "content": System}]

# Chat log file path
chat_log_file = "Data/ChatLog.json"
chat_log_dir = os.path.dirname(chat_log_file)

# Make sure the folder exists
if not os.path.exists(chat_log_dir):
    os.makedirs(chat_log_dir)

# Make sure the file exists
if not os.path.exists(chat_log_file):
    with open(chat_log_file, "w") as f:
        json.dump([], f)

def load_chat_log():
    try:
        with open(chat_log_file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_chat_log(messages):
    with open(chat_log_file, "w") as f:
        json.dump(messages, f, indent=4)

# Function to get real-time information
def get_realtime_info():
    now = datetime.datetime.now()
    return f"Current Date & Time: {now.strftime('%A, %d %B %Y, %H:%M:%S')}"

# Function to clean chatbot output
def clean_response(response):
    return "\n".join(line.strip() for line in response.split("\n") if line.strip())

# Chatbot function
def ChatBot(Query):
    messages = load_chat_log()
    messages.append({"role": "user", "content": Query})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Updated model
            messages=SystemChatBot + [{"role": "system", "content": get_realtime_info()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1
        )

        Answer = completion.choices[0].message.content if completion.choices else "Error: No response from API."
        Answer = Answer.replace("</s>", "").strip()

        messages.append({"role": "assistant", "content": Answer})
        save_chat_log(messages)

        return clean_response(Answer)

    except Exception as e:
        print(f"Error: {e}")
        return "I'm facing an issue. Please try again later."

# Run chatbot in a loop
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        if not user_input.strip():
            print("Please type a valid query.")
            continue
        print(ChatBot(user_input))
