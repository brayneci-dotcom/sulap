import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from jose import jwt, JWTError

from config import settings

router = APIRouter()


def create_token(user_id: str, email: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=settings.jwt_expiry_days),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except JWTError:
        return None


async def get_token_from_cookie(request: Request) -> str | None:
    return request.cookies.get("cpdf_token")


@router.post("/logout")
async def logout():
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie(key="cpdf_token", path="/api")
    return response
