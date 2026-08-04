import logging

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from db.queries import insert_audit_log

logger = logging.getLogger("cloudpdf")


async def log_audit(
    db: AsyncSession,
    request: Request,
    user_id: str | None,
    user_email: str,
    action: str,
    source_files: list[str] | None = None,
    result_file: str | None = None,
    file_sizes: list[int] | None = None,
    result_size: int | None = None,
    processing_ms: int | None = None,
    status: str = "SUCCESS",
    error_message: str | None = None,
) -> None:
    try:
        ip = request.client.host if request.client else None
        ua = request.headers.get("user-agent", "")
        await insert_audit_log(
            db=db,
            user_id=user_id,
            user_email=user_email,
            action=action,
            source_files=source_files,
            result_file=result_file,
            file_sizes=file_sizes,
            result_size=result_size,
            processing_ms=processing_ms,
            status=status,
            error_message=error_message,
            ip_address=ip,
            user_agent=ua,
        )
    except Exception as e:
        logger.error(f"Failed to insert audit log: {e}")
