from .base_prompt import SYSTEM_ROLE, JSON_INSTRUCTIONS

# 1. Update the Example to show the split format
FEW_SHOT_EXAMPLE = """
EXAMPLE_INPUT:
for i in range(len(items)):
    print(items[i])

EXPECTED_OUTPUT:
{
  "language": "python",
  "improvements": "Loop can be simplified using direct iteration."
}
<optimized_code>
for item in items:
    print(item)
</optimized_code>
"""

# 2. Update the Template instructions
IMPROVE_PROMPT_TEMPLATE = """
{system_role}

Your task: Suggest improvements for the provided code.  
Focus on readability, optimization, best practices, and performance.

IMPORTANT OUTPUT RULES:
1. **Metadata (JSON):** valid JSON object containing "language" and "improvements".
2. **Code (XML):** The optimized code MUST be placed OUTSIDE the JSON, wrapped in <optimized_code> tags.
3. **No Markdown:** Do not use markdown code fences (```) for the JSON.

{json_instructions}

FEW_SHOT_EXAMPLE:
{few_shot_example}

Now improve the following code:

CODE_INPUT:
<code_input>
{code}
</code_input>
"""