from langdetect import detect
from deep_translator import GoogleTranslator
import autogen

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

# Create instances of the agents
language_agent = LanguageDetectionAgent(name="LanguageDetector")
translation_agent = TranslationAgent(name="Translator")

def process_ticket(ticket_text):
    language = language_agent.detect_language(ticket_text)
    print(f"Detected Language: {language}")
    
    if language != "en":
        translated_text = translation_agent.translate_to_english(ticket_text, language)
        print(f"Translated Text: {translated_text}")
        return translated_text
    
    return ticket_text

# Example usage
ticket_text = "Dear Support Team, I've been using the Wireless Mouse I purchased recently, and all of a sudden, it just stopped working. I've tried changing the batteries and reconnecting it, but nothing helps. Could you please provide a solution?"
processed_text = process_ticket(ticket_text)
print(f"Final Processed Text: {processed_text}")