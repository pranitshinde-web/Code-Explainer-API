"""
Prompt template specifically for code improvement suggestions.
"""

from .base_prompt import SYSTEM_ROLE, JSON_INSTRUCTIONS

FEW_SHOT_EXAMPLE = """
EXAMPLE_INPUT:
for i in range(len(items)):
    print(items[i])

EXPECTED_OUTPUT:
{
  "language": "python",
  "improvements": "Loop can be simplified using direct iteration.",
  "optimized_code": "for item in items:\\n    print(item)"
}
"""

IMPROVE_PROMPT_TEMPLATE = f"""
{SYSTEM_ROLE}

Your task: Suggest improvements for the provided code.
Focus on readability, optimization, best practices, and performance.

{JSON_INSTRUCTIONS}

Use this JSON structure:
{{
  "language": "",
  "improvements": "",
  "optimized_code": ""
}}

FEW_SHOT_EXAMPLE:
{FEW_SHOT_EXAMPLE}

Now improve the following code:

CODE_INPUT:
\"\"\"{{code}}\"\"\"
"""
