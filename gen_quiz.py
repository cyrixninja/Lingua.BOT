# Importing Libraries
import google.generativeai as genai
import json

# Selecting the Gemini model and configuring the API key
model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key='AIzaSyCxHYxcENbPNzwzoBOlQa48orv09s2BXpM')

# Sample data
json_example_data = """
{
  "questions": [
    {
      "question": "How do you say hello in German?",
      "options": [
        "Guten Tag",
        "Hallo",
        "Tschüss",
        "Danke"
      ],
      "answer": "Hallo"
    },
    {
      "question": "What is the German word for book ?",
      "options": [
        "Buch",
        "Auto",
        "Haus",
        "Hund"
      ],
      "answer": "Buch"
    },
    {
      "question": "How do you say thank you in German?",
      "options": [
        "Bitte",
        "Danke",
        "Entschuldigung",
        "Nein"
      ],
      "answer": "Danke"
    },
    {
      "question": "What is the German word for cat ?",
      "options": [
        "Katze",
        "Maus",
        "Hund",
        "Vogel"
      ],
      "answer": "Katze"
    },
    {
      "question": "How do you say my name is in German?",
      "options": [
        "Ich heiße",
        "Mein Name ist",
        "Ich bin",
        "Ich habe"
      ],
      "answer": "Ich heiße"
    },
    {
      "question": "What is the German word for red ?",
      "options": [
        "Rot",
        "Blau",
        "Grün",
        "Gelb"
      ],
      "answer": "Rot"
    },
    {
      "question": "How do you say good morning in German?",
      "options": [
        "Guten Morgen",
        "Guten Tag",
        "Guten Abend",
        "Gute Nacht"
      ],
      "answer": "Guten Morgen"
    },
    {
      "question": "What is the German word for dog ?",
      "options": [
        "Hund",
        "Katze",
        "Maus",
        "Vogel"
      ],
      "answer": "Hund"
    },
    {
      "question": "How do you say goodbye in German?",
      "options": [
        "Tschüss",
        "Auf Wiedersehen",
        "Bis bald",
        "Ciao"
      ],
      "answer": "Tschüss"
    },
    {
      "question": "What is the German word for green ?",
      "options": [
        "Grün",
        "Blau",
        "Rot",
        "Gelb"
      ],
      "answer": "Grün"
    }
  ]
}
"""

# Function to generate quiz
def generate_quiz(language,difficulty):
    # Prompting the model to generate content
    data = f"""
     Prompt - Generate 10 multiple choice questions on German Language of Easy difficulty and also provide answer .Give Answer in json format                            
    {json_example_data}
    Prompt - Generate 10 multiple choice questions on {language} Language of {difficulty} difficulty and also provide answer .Give Answer in json format                        
    """

    response = model.generate_content(data)
    response_text = response.text
    print(response_text)
    res = json.loads(response_text)

    return res