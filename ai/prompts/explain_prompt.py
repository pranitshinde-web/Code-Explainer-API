"""
Prompt template specifically for code explanation.
"""

from .base_prompt import SYSTEM_ROLE, JSON_INSTRUCTIONS

# Few-shot example to guide model
FEW_SHOT_EXAMPLE = """
EXAMPLE_INPUT:
x = 5
y = x + 10
print(y)

EXPECTED_OUTPUT:
{
  "language": "python",
  "high_level_explanation": "This code stores a value, adds 10 to it, and prints it.",
  "line_by_line_explanation": {
    "1": "A variable x is created and assigned 5.",
    "2": "A variable y stores x + 10.",
    "3": "The value in y is printed."
  }
}
"""

# Main prompt template
EXPLAIN_PROMPT_TEMPLATE = """
{system_role}

Your task: Explain the given code step-by-step in clear and simple language.

{json_instructions}

Use this JSON output format:
{{
  "language": "",
  "high_level_explanation": "",
  "line_by_line_explanation": {{}}
}}

FEW_SHOT_EXAMPLE:
{few_shot_example}

Now explain the following code:

CODE_INPUT:
\"\"\"{code}\"\"\"
"""
