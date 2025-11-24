"""
Prompt template specifically for code improvement suggestions.
"""

from .base_prompt import SYSTEM_ROLE, JSON_INSTRUCTIONS

FEW_SHOT_EXAMPLE = """
EXAMPLE_INPUT:
for i in range(len(items)):
    print(items[i])

EXPECTED_OUTPUT:
{{
  "language": "python",
  "improvements": "Loop can be simplified using direct iteration.",
  "optimized_code": "for item in items:\\n    print(item)"
}}
"""

IMPROVE_PROMPT_TEMPLATE = """
{system_role}

Your task: Suggest improvements for the provided code.  
Focus on readability, optimization, best practices, and performance.

IMPORTANT RULES:
- Respond ONLY with valid JSON.
- Do NOT include any text outside the JSON.
- Do NOT include markdown.
- Do NOT wrap JSON in code fences.
- Output MUST be a single JSON object.

{json_instructions}

FEW_SHOT_EXAMPLE:
{few_shot_example}

Now improve the following code:

CODE_INPUT:
\"\"\"{code}\"\"\"
"""
