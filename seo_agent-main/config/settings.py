"""
Configuration settings for SEO Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

# LLM Configuration
PRIMARY_LLM = "groq"  # "groq" or "openai"
GROQ_MODEL = "llama-3.3-70b-versatile"  # qwen-32b, gpt-oss-120b, mixtral-8x7b-32768
OPENAI_MODEL = "gpt-4"

# Backend Settings
BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8000
DEBUG = True

# Memory Settings
MEMORY_DIR = "./data/memory"
ANALYSIS_HISTORY_FILE = "./data/memory/analysis_history.json"
MEMORY_DB_FILE = "./data/memory/memory_db.json"

# SEO Settings
MIN_TITLE_LENGTH = 30
MAX_TITLE_LENGTH = 60
MIN_META_DESCRIPTION_LENGTH = 120
MAX_META_DESCRIPTION_LENGTH = 160

# Analytics
TRACK_IMPROVEMENTS = True
IMPROVEMENT_WINDOW = 5  # days

# CORS Settings
ALLOWED_ORIGINS = ["*"]
