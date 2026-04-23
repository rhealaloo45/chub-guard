import google.generativeai as genai
model = genai.GenerativeModel("gemini-pro")
response = model.generate_content("Hello")
