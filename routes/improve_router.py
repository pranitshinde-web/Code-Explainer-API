from fastapi import APIRouter, Depends, HTTPException
from models.requests import ImproveCodeRequest
from models.responses import CodeImprovementResponse
from models.errors import ErrorResponse
from services.validator_service import ValidatorService
from services.gemini_service import GeminiService
from utils.logger import log_info
from auth.jwt_handler import verify_access_token


router = APIRouter(prefix="/improve", tags=["Improve Code"])


def get_current_user(token: str = Depends(verify_access_token)):
    return token


@router.post(
    "/code",
    response_model=CodeImprovementResponse,
    responses={400: {"model": ErrorResponse}}
)
async def suggest_improvements(req: ImproveCodeRequest, user=Depends(get_current_user)):
    """
    Suggest improvements, best practices, optimizations.
    """
    log_info("Received improve request")

    # Step 1: Validate
    if not ValidatorService.is_valid_code(req.code):
        raise HTTPException(status_code=400, detail="Invalid or empty code")

    # Step 2: Call Gemini
    improvements = await GeminiService.suggest_improvements(
        code=req.code,
        target=req.target_area
    )

    return CodeImprovementResponse(
        improvements=improvements,
        area=req.target_area
    )
