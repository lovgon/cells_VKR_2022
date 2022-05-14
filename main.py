from pathlib import Path
from typing import List
from uuid import uuid4

import aiofiles
import uvicorn
from fastapi import Body
from fastapi import FastAPI
from fastapi import File
from fastapi import Request
from fastapi import UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from detector import detect
from schemas import ProcessModelResponse
from settings import settings

app = FastAPI()
app.mount(settings.STATIC_DIR_PATH, StaticFiles(directory=settings.STATIC_DIR_PREFIX, check_dir=False), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def main(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("main.html", context={"request": request})


@app.post("/upload-files", response_model=ProcessModelResponse)
async def create_upload_files(
        confidence_threshold: float = Body(settings.DEFAULT_CONFIDENCE_THRESHOLD),
        files: List[UploadFile] = File(...),
) -> ProcessModelResponse:
    batch_id = uuid4()
    upload_dir = Path(settings.UPLOAD_DIR) / str(batch_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    result_dir = Path(settings.RESULT_DIR) / str(batch_id)
    result_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        destination_file_path = upload_dir / file.filename
        async with aiofiles.open(destination_file_path, 'wb+') as out_file:
            while content := await file.read(1024):
                await out_file.write(content)

    files, avg_time, total_time = detect.run(
        source=upload_dir,
        project=result_dir,
        conf_thres=confidence_threshold,
    )

    return ProcessModelResponse(
        files=files,
        total_time=total_time,
        econom_time=9/avg_time,
        avg_time=avg_time,
        batch_id=batch_id,

    )


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
    print("running")
