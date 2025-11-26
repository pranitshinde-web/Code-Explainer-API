import re
import json
from fastapi import APIRouter, Depends, HTTPException, Body
from models.requests import ImproveCodeRequest
from models.responses import CodeImprovementResponse
from models.errors import ErrorResponse
from services.validator_service import ValidatorService
from services.language_service import LanguageService
from services.gemini_service import GeminiService
from utils.logger import log_info, log_error
from auth.jwt_handler import verify_access_token

# Note: We are replacing the generic extract_json with a specific parser below
# from services.extract_json import extract_json 

router = APIRouter(prefix="/improve", tags=["Improve Code"])

# --- Helper Parser Function ---
def parse_split_response(text: str) -> dict:
    """
    Extracts JSON metadata AND the separate XML code block.
    Robust against C/C++ quotes breaking JSON.
    """
    result = {
        "language": None,
        "improvements": "",
        "optimized_code": None
    }

    # 1. Extract JSON Metadata (Non-greedy match for first brace block)
    # This captures {"language": "...", "improvements": "..."}
    json_match = re.search(r"(\{[\s\S]*?\})", text)
    if json_match:
        try:
            json_str = json_match.group(1)
            # Clean generic markdown code fences if present inside the match
            if "```json" in json_str:
                json_str = re.sub(r"```json\s*", "", json_str)
                json_str = re.sub(r"```", "", json_str)
            
            data = json.loads(json_str)
            result["language"] = data.get("language")
            result["improvements"] = data.get("improvements", "")
        except json.JSONDecodeError as e:
            log_error(f"Failed to parse metadata JSON: {e}")

    # 2. Extract Code from XML tags
    # This captures content between <optimized_code> tags, ignoring whatever quotes are inside
    code_match = re.search(r"<optimized_code>([\s\S]*?)</optimized_code>", text)
    if code_match:
        result["optimized_code"] = code_match.group(1).strip()
    
    return result


# --- Auth dependency ---
def get_current_user(token: str = Depends(verify_access_token)):
    return token


@router.post(
    "/code",
    response_model=CodeImprovementResponse,
    responses={400: {"model": ErrorResponse}}
)
async def suggest_improvements(
    code: str = Body(..., media_type="text/plain"),
    language: str | None = None,
    user=Depends(get_current_user)
):
    """
    Suggest improvements, optimizations, best practices, and provide optimized code.
    """

    # Convert raw text → model
    req = ImproveCodeRequest(code=code)

    log_info("Received improve request")
    gemini_service = GeminiService()

    # Step 1: Validate
    if not ValidatorService.is_valid_code(req.code):
        raise HTTPException(status_code=400, detail="Invalid or empty code")

    # Step 2: Detect language
    detected_lang = LanguageService.detect_language(req.code)

    # Step 3: Call Gemini
    # Ensure your GeminiService returns the RAW text (not pre-parsed JSON)
    raw_output = await gemini_service.suggest_improvements(
        code=req.code,
        lang=detected_lang
    )

    # Step 4: Parse using the split parser
    parsed = parse_split_response(raw_output)

    # Validation: If we got absolutely nothing, something went wrong with the AI
    if not parsed["improvements"] and not parsed["optimized_code"]:
        log_error(f"Gemini output parsing failed. Raw output start: {raw_output[:100]}")
        raise HTTPException(
            status_code=500,
            detail="Failed to parse AI response."
        )

    # Step 5: Build final response
    improvements_value = parsed.get("improvements", "")

    # If Gemini returns a list instead of a string (rare but possible)
    if isinstance(improvements_value, list):
        improvements_value = "\n".join(improvements_value)

    return CodeImprovementResponse(
        # Use detected language if AI didn't specify one
        language=parsed.get("language") or detected_lang,
        improvements=improvements_value,
        # If AI didn't provide code, fallback to the original code
        optimized_code=parsed.get("optimized_code") or req.code
    )