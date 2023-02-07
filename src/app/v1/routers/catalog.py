from uuid import uuid4

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from .. import crud
from ..models.common import TaskTicket, TaskResult
from ..processing.tasks import generate_xls_file_task
from .helpers import http_exception_response

XLS_FILES_FOLDER = "/xls"

router = APIRouter(prefix="/api/v1/catalog-request")


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def request_catalog() -> TaskTicket:
    catalog = await crud.read_catalog()

    xls_file_id = uuid4()
    xls_filename = f"{XLS_FILES_FOLDER}/{xls_file_id}.xlsx"

    task = generate_xls_file_task.delay(catalog, xls_filename)
    return TaskTicket(ticket_id=str(task))


@router.get("/{ticket_id}")
async def check_catalog_status(ticket_id: str) -> TaskResult:
    task = AsyncResult(ticket_id)

    if not task.ready():
        return TaskResult(
            ticket_id=ticket_id,
            status=task.status,
        )

    catalog_file_path = task.get()
    return TaskResult(
        ticket_id=ticket_id,
        status=task.status,
        file_path=catalog_file_path,
    )


@router.get(
    "/{ticket_id}/result",
    responses=http_exception_response(
        status_code=status.HTTP_404_NOT_FOUND, detail="file not found"
    ),
)
async def download_catalog(ticket_id: str) -> FileResponse:
    task = AsyncResult(ticket_id)

    if not task.ready():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="file not found"
        )

    catalog_file_path = task.get()
    return FileResponse(
        path=catalog_file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
