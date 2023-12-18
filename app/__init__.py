from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

OUTPUT_DIR = Path("output").resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
