import json
import re
from utils.logger import log_error

def extract_json(text: str):
    """
    Robustly extract JSON from LLM output using Regex.
    Handles Markdown fences and messy pre/post text.
    """
    try:
        # 1. Attempt to clean markdown code fences (```json ... ```)
        cleaned_text = re.sub(r"^```json\s*", "", text, flags=re.MULTILINE)
        cleaned_text = re.sub(r"^```\s*", "", cleaned_text, flags=re.MULTILINE)
        cleaned_text = re.sub(r"```$", "", cleaned_text, flags=re.MULTILINE)

        # 2. Find the first outer-most curly brace structure
        # This regex looks for a { followed by anything, ending with a }
        # re.DOTALL allows matching across newlines
        match = re.search(r"(\{.*\})", cleaned_text, re.DOTALL)
        
        if not match:
            log_error(f"No JSON structure found in text: {text[:100]}...")
            return None

        candidate = match.group(1)
        
        return json.loads(candidate)

    except json.JSONDecodeError as e:
        log_error(f"JSON Decode Error: {str(e)} | Input: {text[:100]}...")
        return None
    except Exception as e:
        log_error(f"JSON Extraction Error: {str(e)}")
        return None