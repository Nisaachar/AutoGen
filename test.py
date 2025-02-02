import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

async def main() -> None:
    # Retrieve the API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    # print(api_key)
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    # Initialize the AssistantAgent with the API key
    agent = AssistantAgent(
        "assistant",
        OpenAIChatCompletionClient(model="gpt-4o", api_key=api_key),
    )
    print(await agent.run(task="Say 'Hello World!'"))

# Run the main function
asyncio.run(main())
