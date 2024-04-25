from typing import Annotated

from fastapi import APIRouter, Request, UploadFile, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.file_worker import FileWorker
from src.tfidf_inspector import TfidfInspector

tfidf_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

worker = FileWorker()


@tfidf_router.get("/", response_class=HTMLResponse)
async def main(request: Request):
    context = {
        "request": request,
        "title": "TF-IDF главная"
    }

    return templates.TemplateResponse("index.html", context)


@tfidf_router.post("/uploadfiles", response_class=HTMLResponse, response_model=None)
async def upload_files(
        files: list[UploadFile],
        request: Request,
):

    summary_files = await worker.worker(files)

    context = {
        "request": request,
        "title": "Загрузка файлов",
        "files": files,
        "text": summary_files,
    }

    return templates.TemplateResponse("upload.html", context)


@tfidf_router.get("/tf-idf", response_class=HTMLResponse)
async def tf_idf(file: str, request: Request, inspector: Annotated[TfidfInspector, Depends()]):
    result = inspector.inspector(worker.texts, file)

    context = {
        "request": request,
        "title": "Расчет TF-IDF",
        "result": result,
    }

    return templates.TemplateResponse("tf-idf.html", context)
