import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(question: str):
    for attempt in range(3):
        try:
            response = client.interactions.create(
                model="gemini-3.6-flash",
                input=question,
            )

            return response.output_text

        except errors.RateLimitError:
            raise

        except Exception:
            if attempt == 2:
                raise

            time.sleep(2 ** attempt)