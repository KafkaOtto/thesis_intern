import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Choose a Hugging Face model (can be changed in .env)
HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")