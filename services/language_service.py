# services/language_service.py

import re
from utils.logger import log_error


class LanguageService:

    @staticmethod
    def detect_language(code: str) -> str:
        """
        Lightweight heuristics to detect common programming languages.
        """

        try:
            # Python
            if re.search(r"def\s+|import\s+|print\(", code):
                return "python"

            # JavaScript
            if re.search(r"function\s+|console\.log|=>", code):
                return "javascript"

            # Java
            if re.search(r"public\s+class|System\.out\.println", code):
                return "java"

            # C++
            if re.search(r"#include\s+<|std::", code):
                return "cpp"

            # C
            if re.search(r"#include\s+<.*\.h>", code):
                return "c"

            # HTML
            if "<html>" in code.lower():
                return "html"

            return "unknown"

        except Exception as e:
            log_error(f"LanguageService Exception: {str(e)}")
            return "unknown"
