from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

ALLOWED_ORIGIN = None  # Set from config in production


@router.get("/health")
async def health_check():
    """Cloud Run health check. Liveness only — no DB dep."""
    return {"status": "UP"}


# Origin validation middleware (applied to mutation endpoints)
async def validate_origin(request: Request):
    if request.method in ("GET", "HEAD", "OPTIONS"):
        return
    origin = request.headers.get("origin") or request.headers.get("referer", "")
    if ALLOWED_ORIGIN and origin and not origin.startswith(ALLOWED_ORIGIN):
        raise HTTPException(status_code=403, detail="Origin not allowed")
    return
