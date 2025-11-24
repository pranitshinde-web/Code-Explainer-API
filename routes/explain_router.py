from fastapi import APIRouter, Depends, HTTPException
from models.requests import ExplainCodeRequest
from models.responses import CodeExplanationResponse
from models.errors import ErrorResponse
from services.validator_service import ValidatorService
from services.language_service import LanguageService
from services.gemini_service import GeminiService
from utils.logger import log_info
from auth.jwt_handler import verify_access_token
import json
import re

router = APIRouter(prefix="/explain", tags=["Explain Code"])


# Dependency - for authenticated endpoints
def get_current_user(token: str = Depends(verify_access_token)):
    return token


@router.post(
    "/code",
    response_model=CodeExplanationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def explain_code(req: ExplainCodeRequest, user=Depends(get_current_user)):
    """
    Explain code in simple terms.
    """
    log_info("Received explain request")
    gemini_service = GeminiService()

    # Step 1: Validate Input
    if not ValidatorService.is_valid_code(req.code):
        raise HTTPException(status_code=400, detail="Invalid or empty code")

    # Step 2: Detect Language
    detected_lang = LanguageService.detect_language(req.code)

    # Step 3: Call Gemini
    raw_output = await gemini_service.explain_code(
        code=req.code,
        lang=detected_lang,
    )

    # -----------------------------------------
    # Step 4: Extract valid JSON from model output
    # -----------------------------------------

    match = re.search(r"\{(.|\n)*\}", raw_output)
    if not match:
        raise HTTPException(
            status_code=500,
            detail="Gemini did not return valid JSON."
        )

    try:
        parsed = json.loads(match.group())
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to parse JSON returned by Gemini."
        )

    # -----------------------------------------
    # Step 5: Return structured validated output
    # -----------------------------------------
    return CodeExplanationResponse(
        language=parsed.get("language", detected_lang),
        high_level_explanation=parsed.get("high_level_explanation", ""),
        line_by_line_explanation=parsed.get("line_by_line_explanation", {})
    )
