from langdetect import detect
from deep_translator import GoogleTranslator
import autogen
import openai
import os
from googlesearch import search

# Set your OpenAI API key
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


class PriorityDeterminationAgent(autogen.Agent):
    def __init__(self, name):
        super().__init__(name=name)

    def determine_priority(self, text):
        """Uses OpenAI's GPT-4 to determine the priority level (1, 2, or 3)."""
        prompt = f"""
        You are a helpdesk assistant determining the priority level of a ticket.
        Assign a priority level based on the following criteria:
        
        - Priority 1 (High): Critical issues (e.g., system outages, major financial discrepancies, urgent security concerns, severe hardware failures).
        - Priority 2 (Medium): Important but not urgent issues (e.g., incorrect invoice, software bugs affecting workflow, non-critical hardware issues).
        - Priority 3 (Low): Minor issues (e.g., general inquiries, feature requests, small inconveniences).

        Ticket: "{text}"

        Respond with ONLY the priority number: 1, 2, or 3.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are a helpdesk assistant determining ticket priority."},
                          {"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0
            )
            priority = response.choices[0].message.content.strip()
            return priority
        except Exception as e:
            return f"Error determining priority: {str(e)}"
        

#Drafting solution for user.
class SolutionSuggestionAgent(autogen.Agent):
    def __init__(self, name):
        super().__init__(name=name)

    def generate_suggestion(self, text):
        """Uses OpenAI's GPT-4 to suggest a possible solution and fetch relevant resources."""
        prompt = f"""
        You are an AI helpdesk assistant. Provide a helpful troubleshooting message to the user for their issue.

        Ticket: "{text}"

        Suggest a possible solution that the user can try on their own.

        Keep it short and to the point.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are a troubleshooting assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.5
            )
            solution = response.choices[0].message.content.strip()

            # Fetch additional resources (2 YouTube videos + 1 Article)
            youtube_videos = list(search(f"site:youtube.com {text} troubleshooting", num_results=2))
            article = list(search(f"{text} troubleshooting guide", num_results=1))

            return solution, youtube_videos, article

        except Exception as e:
            return f"Error generating solution: {str(e)}", [], []

def send_alert_email():
    """Simulates sending an email if priority is 1."""
    print("Sending mail to head-support@company.com...")


# Create instances of the agents
language_agent = LanguageDetectionAgent(name="LanguageDetector")
translation_agent = TranslationAgent(name="Translator")
categorization_agent = CategorizationAgent(name="Categorizer")
priority_agent = PriorityDeterminationAgent(name="PriorityAssigner")
solution_agent = SolutionSuggestionAgent(name="SolutionAssistant")


def process_ticket(ticket_text):
    """Processes a helpdesk ticket by detecting language, translating if necessary, categorizing, and determining priority."""
    
    # Detect the language
    language = language_agent.detect_language(ticket_text)
    print(f"Detected Language: {language}")
    
    # Translate if not in English
    if language != "en":
        translated_text = translation_agent.translate_to_english(ticket_text, language)
        print(f"Translated Text: {translated_text}")
    else:
        translated_text = ticket_text
    
    # Categorize the ticket
    category = categorization_agent.categorize_ticket(translated_text)
    print(f"Ticket Category: {category}")

    # Determine ticket priority
    priority = priority_agent.determine_priority(translated_text)
    print(f"Ticket Priority: {priority}")

    if priority == "1":
        send_alert_email()
    else:
        # If priority is not 1, generate a troubleshooting message for the user
        solution, youtube_videos, article = solution_agent.generate_suggestion(translated_text)
        print(f"Suggested Solution for User: {solution}")
        print("📺 Recommended YouTube Videos:")
        flag = 0
        for video in youtube_videos:
            if flag == 0:
                flag += 1
                continue
            print(f"🔗 {video}")
            
        print("📝 Recommended Article:")
        for link in article:
            print(f"🔗 {link}")


    return translated_text, category, priority


# Example usage
ticket_text = """
I'm trying to get a print out from the company printer but not sure hot to do it.
"""

processed_text, category, priority = process_ticket(ticket_text)

print(f"Final Processed Text: {processed_text}")
print(f"Final Ticket Category: {category}")
print(f"Final Ticket Priority: {priority}")