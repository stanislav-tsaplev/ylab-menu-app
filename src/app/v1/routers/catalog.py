from os import getenv, mkdir
from os.path import exists as path_exists
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from .. import crud
from ..models.common import TaskTicket, TaskResult, OperationResult
from ..processing.catalog import generate_xls_file

XLS_FILES_FOLDER = getenv("XLS_FILES_FOLDER", "xls")

router = APIRouter(prefix="/api/v1/catalog")


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def generate_catalog() -> TaskTicket:
    catalog = await crud.read_catalog()

    ticket_id = uuid4()
    xls_filename = f"{XLS_FILES_FOLDER}/{ticket_id}.xlsx"
    if not path_exists(XLS_FILES_FOLDER):
        mkdir(XLS_FILES_FOLDER)

    generate_xls_file(catalog, xls_filename)

    return TaskTicket(ticket_id=ticket_id)


@router.get("/{ticket_id}")
async def get_catalog_link(ticket_id: UUID) -> TaskResult:
    return TaskResult(
        result=OperationResult(status=True, message="Demanded catalog is ready"),
        link=f"{XLS_FILES_FOLDER}/{ticket_id}.xlsx",
    )


@router.get("/{ticket_id}/download")
async def download_catalog(ticket_id: UUID) -> FileResponse:
    if not path_exists(f"{XLS_FILES_FOLDER}/{ticket_id}.xlsx"):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such file"
        )
    return FileResponse(f"{XLS_FILES_FOLDER}/{ticket_id}.xlsx")
