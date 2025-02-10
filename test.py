import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from autogen_core.models import UserMessage



from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables from the .env file
load_dotenv()

async def main() -> None:
    # Retrieve the API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    

    # Initialize the AssistantAgent with the API key
    agent = AssistantAgent(
        "assistant",
        OpenAIChatCompletionClient(model="gpt-4o", api_key=api_key),
    )
    print(await agent.run(task="Say 'Hello World!'"))

    async def assistant_run() -> None:
        response = await agent.on_messages(
            [TextMessage(content="Find information on AutoGen", source="user")],
            cancellation_token=CancellationToken(),
        )
        print(response.inner_messages)
        print(response.chat_message)


# Use asyncio.run(assistant_run()) when running in a script.
    await assistant_run()

# Run the main function
asyncio.run(main())