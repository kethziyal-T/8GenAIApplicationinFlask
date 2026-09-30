import os
#from dotenv import load_dotenv

# 1. FIX: Explicitly target the custom file named "1.env" instead of the default ".env"
#load_dotenv(dotenv_path="1.env")

# 
# 2. Safely read the loaded API key variable strings
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# 3. Security Check: Raise a helpful message if the variable is missing
if not GENAI_API_KEY:
    raise ValueError(
        "❌ Critical Configuration Error: 'GENAI_API_KEY' was not found. "
        "Please check your environment configurations or your local 1.env file setup."
    )
