from secrets import compare_digest

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from orders_service.api.security import create_access_token, verify_password
from orders_service.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    username_is_valid = compare_digest(request.username, settings.auth_username)

    try:
        password_is_valid = verify_password(
            request.password,
            settings.auth_password_hash.get_secret_value(),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail="Authentication is not configured correctly.",
        ) from exc

    if not username_is_valid or not password_is_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": request.username})
    return TokenResponse(access_token=access_token, token_type="bearer")
