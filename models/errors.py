from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    Standard error response model for the entire API.
    """
    error_code: str = Field(..., description="Machine-readable error identifier.")
    message: str = Field(..., description="Human-friendly error message.")
