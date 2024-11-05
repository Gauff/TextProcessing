import os
from dotenv import load_dotenv

load_dotenv()

LITE_LLM_URI = os.getenv('LITE_LLM_URI')
SMALL_CONTEXT_MODEL_NAME = os.getenv('SMALL_CONTEXT_MODEL_NAME')
SMALL_CONTEXT_MAX_TOKENS = int(os.getenv('SMALL_CONTEXT_MAX_TOKENS'))
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')