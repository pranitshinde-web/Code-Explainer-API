from pydantic import BaseModel, Field
from typing import Dict, Optional


class CodeExplanationResponse(BaseModel):
    """
    Response returned by /explain-code.
    """
    language: str = Field(..., description="Detected or provided programming language.")
    high_level_explanation: str = Field(..., description="Overall summary of what the code does.")
    line_by_line_explanation: Dict[str, str] = Field(
        ..., description="Detailed explanation for each line. Key = line number."
    )


class CodeImprovementResponse(BaseModel):
    """
    Response returned by /suggest-improvements.
    """
    language: str = Field(..., description="Detected or provided programming language.")
    improvements: str = Field(..., description="List of improvement suggestions for the code.")
    optimized_code: Optional[str] = Field(
        None, description="If Gemini suggests an optimized version, it appears here."
    )


class AuthResponse(BaseModel):
    """
    Response returned by /auth/login.
    """
    access_token: str = Field(..., description="JWT access token.")
    token_type: str = Field(default="bearer", description="Type of token.")
