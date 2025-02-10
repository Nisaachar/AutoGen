import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

# Retrieve the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Define OpenAI Model Configuration (Fixed)
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": api_key,
        }
    ],
}

# User Proxy Agent (Represents the human user submitting tickets)
user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="A human admin interacting with AI agents.",
    human_input_mode="TERMINATE",  # Stops after initial input
    code_execution_config={"use_docker": False},  # Disable Docker Execution
)

# Language Detector Agent
language_detector = AssistantAgent(
    name="LanguageDetector",
    system_message="Detect the language of the provided text and respond with the two-letter language code (e.g., 'en' for English, 'es' for Spanish, 'fr' for French). If the text is already in English, just return 'en'.",
    llm_config=llm_config,  
)

# Translation Agent (Translates to English if necessary)
translation_agent = AssistantAgent(
    name="TranslationAgent",
    system_message="If the given text is NOT in English, translate it into English. If it is already in English, return the text as is.",
    llm_config=llm_config,  
)

# GroupChat Setup (Now has Language Detector & Translation Agent)
groupchat = GroupChat(
    agents=[user_proxy, language_detector, translation_agent], 
    messages=[], 
    max_round=12
)
manager = GroupChatManager(groupchat=groupchat)

# Function to process user input
def handle_ticket(ticket_text: str) -> None:
    # Step 1: Detect Language
    response = manager.initiate_chat(user_proxy, message=f"Detect the language of the following text: {ticket_text}")
    
    # Step 2: Extract detected language from response
    print(response)
    detected_language = response.chat_history[-1]["content"].strip().lower() if response.chat_history else ""
    # print(response)
    
    # Step 3: If the text is not in English, call the translation agent
    if detected_language != "en":
        print(f"Detected Language: {detected_language}. Translating...")
        translation_response = manager.initiate_chat(user_proxy, message=f"Translate the following text to English: {ticket_text}")
        translated_text = translation_response.get("last_message", {}).get("content", "").strip()
        print(f"Translated Ticket: {translated_text}")
    else:
        print("The ticket is already in English. No translation needed.")

# Example Test Cases
print("------ Test 1: Spanish Ticket ------")
handle_ticket("Este es un problema con mi computadora portátil.")

print("\n------ Test 2: English Ticket ------")
handle_ticket("My laptop is not turning on.")