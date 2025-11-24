# utils/logger.py

import logging

# Create the logger
logger = logging.getLogger("code_explainer")
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Format logs
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add handler to logger
if not logger.handlers:
    logger.addHandler(console_handler)


def log_info(message: str):
    logger.info(message)


def log_error(message: str):
    logger.error(message)
