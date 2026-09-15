import os
from dotenv import load_dotenv

load_dotenv()

NCBI_API_KEY = os.getenv("NCBI_API_KEY", "")
if NCBI_API_KEY:
    os.environ["NCBI_API_KEY"] = NCBI_API_KEY

LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
LMSTUDIO_MODEL_NAME = os.getenv("LMSTUDIO_MODEL_NAME", "google/gemma-4-e2b")

