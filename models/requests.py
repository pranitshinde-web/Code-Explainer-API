from pydantic import BaseModel, Field
from typing import Optional


class ExplainCodeRequest(BaseModel):
    """
    Request model for the /explain-code endpoint.
    """
    code: str = Field(..., description="Raw code snippet provided by user.")
    language: Optional[str] = Field(
        None, description="Optional: Language of the code. Auto-detected if missing."
    )


class ImproveCodeRequest(BaseModel):
    """
    Request model for the /suggest-improvements endpoint.
    """
    code: str = Field(..., description="Code for which improvement suggestions are required.")
    language: Optional[str] = Field(
        None, description="Optional: Language of the code. Auto-detected if missing."
    )


class LoginRequest(BaseModel):
    """
    Request model for /auth/login.
    """
    username: str = Field(..., description="Username to login.")
    password: str = Field(..., description="Password to login.")
