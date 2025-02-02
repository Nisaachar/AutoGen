import os
import autogen

# Disable Docker usage globally
os.environ["AUTOGEN_USE_DOCKER"] = "0"

# Configuration for the LLM
llm_config = {
    "config_list": [
        {
            "provider": "azure_openai",
            "deployment_name": "clin-inquiry-agent-gpt4o",  # Replace with your deployment name
            "model": "gpt4",                     # Replace with your model version
            "api_key": "7af322a7e69945f08d7dab40bf724955",      # Replace with your Azure API Key
            "api_base": "https://dev-clin-inquiry-openai-useast.openai.azure.com/",  # Replace with your endpoint
            "temperature": 0.7,                   # Adjust temperature if needed
        }
    ],
    "cache_seed": 42
}
# Define user agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False  # Explicitly disable Docker here
    },
    human_input_mode="TERMINATE"
)

# Define assistant agents
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config
)

pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config
)

# Define a group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, coder, pm],
    messages=[],  # Initial messages
    max_round=12  # Define the number of maximum rounds
)

# Create a group chat manager
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# Test: Adding a simple interaction
def main():
    print("Starting the Group Chat...")
    manager.run(input_text="Create a basic script for Azure OpenAI integration in AutoGen.")

if __name__ == "__main__":
    main()