# services/gemini_service.py

import google.generativeai as genai
from utils.logger import log_info, log_error
from ai.prompts.explain_prompt import EXPLAIN_PROMPT_TEMPLATE
from ai.prompts.improve_prompt import IMPROVE_PROMPT_TEMPLATE
from config import settings


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-2.0-flash")

    async def explain_code(self, code: str, lang: str) -> str:
        try:
            from ai.prompts.base_prompt import SYSTEM_ROLE, JSON_INSTRUCTIONS
            from ai.prompts.explain_prompt import FEW_SHOT_EXAMPLE

            prompt = EXPLAIN_PROMPT_TEMPLATE.format(
                system_role=SYSTEM_ROLE,
                json_instructions=JSON_INSTRUCTIONS,
                few_shot_example=FEW_SHOT_EXAMPLE,
                code=code,
                lang=lang
            )

            log_info("Sending explain prompt to Gemini")

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            log_error(f"GeminiService explain_code Exception: {str(e)}")
            raise RuntimeError("Failed to generate explanation")

    async def suggest_improvements(self, code: str,lang:str) -> str:
        try:
            from ai.prompts.base_prompt import SYSTEM_ROLE, JSON_INSTRUCTIONS
            from ai.prompts.improve_prompt import FEW_SHOT_EXAMPLE

            prompt = IMPROVE_PROMPT_TEMPLATE.format(
                system_role=SYSTEM_ROLE,
                json_instructions=JSON_INSTRUCTIONS,
                few_shot_example=FEW_SHOT_EXAMPLE,
                code=code,
                lang=lang
            )

            log_info("Sending improve prompt to Gemini")

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            log_error(f"GeminiService suggest_improvements Exception: {str(e)}")
            raise RuntimeError("Failed to generate improvements")
