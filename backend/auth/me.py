from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from auth.dependencies import get_current_user

router = APIRouter()


@router.get("/me")
async def get_me(request: Request, user=Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email,
        "display_name": user.display_name,
        "picture_url": user.picture_url,
        "role": user.role,
    }
