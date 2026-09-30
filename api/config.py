import os
#from dotenv import load_dotenv

# 1. FIX: Explicitly target the custom file named "1.env" instead of the default ".env"
#load_dotenv(dotenv_path="1.env")

# 
# 2. Safely read the loaded API key variable strings
GENAI_API_KEY = os.getenv("GENAI_API_KEY","")

