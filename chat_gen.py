# Importing Libraries
import google.generativeai as genai

# Selecting the Gemini model and configuring the API key
model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key='api_key')

