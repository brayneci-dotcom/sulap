import time
import uuid
import json
import logging
from pathlib import Path

from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pypdf import PdfReader, PdfWriter

from config import settings
from db.database import get_db
from auth.dependencies import get_current_user
from audit import log_audit

logger = logging.getLogger("cloudpdf")

router = APIRouter()

PDF_MAGIC = b"%PDF"


@router.post("/rearrange")
async def rearrange_pdf(
    request: Request,
    file: UploadFile = File(...),
    operations: str = Form("[]"),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """Atur ulang halaman PDF: reorder, delete, rotate."""
    job_id = str(uuid.uuid4())[:8]
    input_path = Path(f"/tmp/cpdf_{job_id}_input.pdf")
    output_path = Path(f"/tmp/cpdf_{job_id}_output.pdf")
    start_time = time.monotonic()
    input_size = 0

    try:
        # Parse operations
        try:
            ops = json.loads(operations)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Format operasi tidak valid")

        # Save input
        content = await file.read()
        input_path.write_bytes(content)
        del content

        # Validate
        input_size = input_path.stat().st_size
        if input_size > settings.max_file_size_mb * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"File terlalu besar. Maks {settings.max_file_size_mb}MB")

        with open(input_path, "rb") as f:
            if f.read(4) != PDF_MAGIC:
                raise HTTPException(status_code=400, detail="Format file tidak didukung")

        reader = PdfReader(str(input_path))
        total_pages = len(reader.pages)

        if total_pages > settings.max_pages_rearrange:
            raise HTTPException(status_code=400, detail=f"Maksimal {settings.max_pages_rearrange} halaman")

        # Build target page list: [{reader_index, rotation}, ...]
        pages = [{"index": i, "rotation": 0} for i in range(total_pages)]

        for op in ops:
            if await request.is_disconnected():
                await _audit_fast(db, request, user, file, input_size, 0, "CANCELLED_BY_CLIENT")
                _cleanup(input_path, output_path)
                return StreamingResponse(iter([]), status_code=499)

            action = op.get("action")

            if action == "reorder":
                # op["order"] = new sequence of original indices
                new_order = op.get("order", [])
                if new_order:
                    pages = [pages[i] for i in new_order if 0 <= i < len(pages)]

            elif action == "rotate":
                idx = op.get("page", -1)
                angle = op.get("angle", 90)
                if 0 <= idx < len(pages):
                    pages[idx]["rotation"] = (pages[idx]["rotation"] + angle) % 360

            elif action == "delete":
                idx = op.get("page", -1)
                if 0 <= idx < len(pages):
                    pages.pop(idx)

            elif action == "move":
                idx = op.get("page", -1)
                to_idx = op.get("to", 0)
                if 0 <= idx < len(pages) and 0 <= to_idx < len(pages):
                    item = pages.pop(idx)
                    pages.insert(to_idx, item)

        if not pages:
            raise HTTPException(status_code=400, detail="Tidak ada halaman tersisa")

        # Build output PDF
        writer = PdfWriter()
        for page_info in pages:
            page = reader.pages[page_info["index"]]
            if page_info["rotation"]:
                page.rotate(page_info["rotation"])
            writer.add_page(page)

        writer.write(str(output_path))
        output_data = output_path.read_bytes()
        output_size = len(output_data)
        processing_ms = int((time.monotonic() - start_time) * 1000)

        await _audit_fast(db, request, user, file, input_size, output_size, "SUCCESS", processing_ms)

        logger.info(f"Rearrange {job_id}: {total_pages}p→{len(pages)}p, {processing_ms}ms")

        return StreamingResponse(
            iter([output_data]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="rearranged_{file.filename or "output"}.pdf"',
                "X-Pages-Before": str(total_pages),
                "X-Pages-After": str(len(pages)),
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rearrange error job={job_id}: {e}")
        await _audit_fast(db, request, user, file, input_size, 0, "FAILED", error_msg=str(e)[:500])
        raise HTTPException(status_code=500, detail="Gagal mengatur ulang halaman")
    finally:
        _cleanup(input_path, output_path)


async def _audit_fast(db, request, user, file, input_size, output_size, status, processing_ms=0, error_msg=None):
    await log_audit(
        db=db, request=request,
        user_id=str(user.id), user_email=user.email,
        action="REARRANGE",
        source_files=[file.filename or "unknown"],
        result_file=f"rearranged_{file.filename}" if status == "SUCCESS" else None,
        file_sizes=[input_size],
        result_size=output_size if status == "SUCCESS" else None,
        processing_ms=processing_ms,
        status=status,
        error_message=error_msg,
    )


def _cleanup(*paths: Path):
    for p in paths:
        try:
            p.unlink(missing_ok=True)
        except OSError:
            pass
