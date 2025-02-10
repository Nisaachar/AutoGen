import autogen
import os

api_key = os.getenv("OPENAI_API_KEY")

# def main():
#     # Create an agent that uses OpenAI’s LLM.
#     # The system prompt instructs the agent to detect the language of the input text.
#     language_detector = autogen.Agent(
#         name="LanguageDetector",
#         system_prompt=(
#             "You are a language detection agent. When given an input text, "
#             "determine the language in which it is written and respond with only the language's name."
#         ),
#         llm_config={
#             "model": "gpt-3.5-turbo",  # or another OpenAI model of your choice
#             "temperature": 0.0,
#             "api_key": api_key,     # use a deterministic output
#         }
#     )

#     # Prompt the user to input some text
#     user_input = input("Enter text: ")

#     # Run the agent on the input text
#     detected_language = language_detector.run(user_input)

#     # Display the detected language
#     print("Detected language:", detected_language.strip())




def main():
    # Use a factory method (if available) to create a concrete agent.
    language_detector = autogen.create_agent(
        name="LanguageDetector",
        system_prompt=(
            "You are a language detection agent. When given an input text, "
            "determine the language in which it is written and respond with only the language's name."
        ),
        llm_config={
            "model": "gpt-3.5-turbo",
            "temperature": 0.0,
            "api_key": api_key,
        }
    )

    user_input = input("Enter text: ")
    detected_language = language_detector.run(user_input)
    print("Detected language:", detected_language.strip())



if __name__ == "__main__":
    main()