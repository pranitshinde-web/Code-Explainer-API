def extract_json(text: str):
    """
    Extract the first valid JSON object from a string.
    This method is robust against markdown, code fences, and extra text.
    """
    import json

    stack = 0
    start = None

    for i, char in enumerate(text):
        if char == '{':
            if stack == 0:
                start = i
            stack += 1
        elif char == '}':
            stack -= 1
            if stack == 0 and start is not None:
                candidate = text[start:i + 1]
                try:
                    return json.loads(candidate)  # success!
                except json.JSONDecodeError:
                    continue

    return None
