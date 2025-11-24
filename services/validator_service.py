# services/validator_service.py

import re
from utils.logger import log_error


class ValidatorService:

    @staticmethod
    def is_valid_code(code: str) -> bool:
        """
        Checks if code is non-empty and not harmful.
        """
        try:
            if not code or code.strip() == "":
                return False

            # Check for harmful patterns (basic)
            dangerous_patterns = [
                r"rm\s+-rf", 
                r"shutdown\s+-h",
                r"del\s+/f",
                r"DROP\s+DATABASE",
                r":(){:|:&};:"  # fork bomb
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    log_error(f"Dangerous code detected: {pattern}")
                    return False

            return True

        except Exception as e:
            log_error(f"ValidatorService Exception: {str(e)}")
            return False
