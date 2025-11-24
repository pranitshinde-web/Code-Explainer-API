from fastapi import APIRouter, Depends, HTTPException, Body
from models.requests import ImproveCodeRequest
from models.responses import CodeImprovementResponse
from models.errors import ErrorResponse
from services.validator_service import ValidatorService
from services.language_service import LanguageService
from services.gemini_service import GeminiService
from utils.logger import log_info
from auth.jwt_handler import verify_access_token
from services.extract_json import extract_json

router = APIRouter(prefix="/improve", tags=["Improve Code"])


# Auth dependency
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
    raw_output = await gemini_service.suggest_improvements(
        code=req.code,
        lang=detected_lang
    )

    # Step 4: Extract JSON output from Gemini
    parsed = extract_json(raw_output)

    if not parsed:
        raise HTTPException(
            status_code=500,
            detail="Gemini did not return valid JSON."
        )

    # Step 5: Build final response
    improvements_value = parsed.get("improvements", "")

# If Gemini returns a list instead of a string
    if isinstance(improvements_value, list):
        improvements_value = "\n".join(improvements_value)

    return CodeImprovementResponse(
        language=parsed.get("language", detected_lang),
        improvements=improvements_value,
        optimized_code=parsed.get("optimized_code")
    )

