import shutil

from fastapi import APIRouter, File, UploadFile

from app.core.config import settings
from app.rag.pipeline import process_pdf

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
):
    upload_dir = settings.upload_path
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    # Upload then index via RAG
    process_pdf(str(file_path))

    return {
        "filename": file.filename,
        "status": "uploaded and indexed",
    }
