from langdetect import detect
from deep_translator import GoogleTranslator
import autogen
import openai
import os

# Set your OpenAI API key
# openai.api_key = os.getenv('')

api_key = os.getenv("OPENAI_API_KEY")

# Ensure OpenAI client is properly initialized
client = openai.OpenAI(api_key=api_key)


class LanguageDetectionAgent(autogen.Agent):
    def __init__(self, name):
        super().__init__(name=name)

    def detect_language(self, text):
        try:
            language = detect(text)
            return language
        except Exception as e:
            return f"Error detecting language: {str(e)}"

class TranslationAgent(autogen.Agent):
    def __init__(self, name):
        super().__init__(name=name)

    def translate_to_english(self, text, source_language):
        try:
            translated_text = GoogleTranslator(source=source_language, target='en').translate(text)
            return translated_text
        except Exception as e:
            return f"Error translating text: {str(e)}"

class CategorizationAgent(autogen.Agent):
    def __init__(self, name):
        super().__init__(name=name)

    def categorize_ticket(self, text):
        """Uses OpenAI's GPT-4 to categorize the ticket into 'Hardware', 'Accounting', or 'Software'."""
        prompt = f"""
        You are an AI helpdesk assistant. Categorize the following ticket into one of the three categories: 
        - 'Hardware' (for issues related to physical devices like printers, mice, and keyboards)
        - 'Accounting' (for billing, invoices, and financial matters)
        - 'Software' (for application-related issues, installations, or errors)
        
        Ticket: "{text}"
        
        Respond with ONLY the category name: 'Hardware', 'Accounting', or 'Software'.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are a classification assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0
            )
            category = response.choices[0].message.content.strip()
            return category
        except Exception as e:
            return f"Error categorizing text: {str(e)}"
        

# Create instances of the agents
language_agent = LanguageDetectionAgent(name="LanguageDetector")
translation_agent = TranslationAgent(name="Translator")
categorization_agent = CategorizationAgent(name="Categorizer")

def process_ticket(ticket_text):
    language = language_agent.detect_language(ticket_text)
    print(f"Detected Language: {language}")
    
    if language != "en":
        translated_text = translation_agent.translate_to_english(ticket_text, language)
        print(f"Translated Text: {translated_text}")
    else:
        translated_text = ticket_text
    
    category = categorization_agent.categorize_ticket(translated_text)
    print(f"Ticket Category: {category}")

    return translated_text, category

# Example usage
ticket_text = "Bonjour, nous rencontrons un problème avec notre matériel IP PBX. Les connexions sont instables et nous observons des interruptions fréquentes. Cela affecte fortement notre communication interne. Votre assistance serait très appréciée pour régler ce problème rapidement."
processed_text, category = process_ticket(ticket_text)
print(f"Final Processed Text: {processed_text}")
print(f"Final Ticket Category: {category}")