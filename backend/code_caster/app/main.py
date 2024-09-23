import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    File,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse

from app import schemas
from app.config import settings
from app.depends import verify_token
from app.llm import gen_readme

media_path = Path(settings.MEDIA_PATH)


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(media_path, exist_ok=True)
    yield


app = FastAPI(dependencies=[Depends(verify_token)], lifespan=lifespan)


@app.post(
    "/gen/readme/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.CreateGenReadmeResponse,
)
async def generate_readme(
    backgrounds_tasks: BackgroundTasks,
    source: UploadFile = File(...),
) -> schemas.CreateGenReadmeResponse:
    token = str(uuid.uuid4())
    output_path = media_path / token
    os.makedirs(output_path, exist_ok=True)

    content = await source.read()
    await source.close()
    backgrounds_tasks.add_task(gen_readme, content=content, output_path=output_path)

    return schemas.CreateGenReadmeResponse(token=token)


@app.get(
    "/gen/readme/{token}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.CreateGenReadmeResponse,
)
async def get_generated_readme(
    token: str,
) -> FileResponse:
    output_path = media_path / token

    # check directory
    if not output_path.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="content is not found"
        )
    # check generated output file
    output_file = output_path / "output.md"
    if not output_file.is_file():
        raise HTTPException(
            status_code=status.HTTP_102_PROCESSING, detail="please wait to generate"
        )

    return FileResponse(
        path=output_file,
        filename="code-caster-readme.md",
        media_type="text/plain",
    )
