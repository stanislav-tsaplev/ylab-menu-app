from uuid import UUID, uuid4

from fastapi import APIRouter, status

from ..crud.catalog import read_catalog
from ..models.common import GeneratingTaskTicket, GeneratingTaskResult, OperationResult
from ..processing.catalog import generate_xls_file

router = APIRouter(prefix="/api/v1/catalog")


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def generate_catalog() -> GeneratingTaskTicket:
    catalog = await read_catalog()

    ticket_id = uuid4()
    xls_filename = f"xls/{ticket_id}.xlsx"
    generate_xls_file(catalog, xls_filename)

    return GeneratingTaskTicket(ticket_id=ticket_id)


@router.get("/{ticket_id}")
async def get_catalog_link(ticket_id: UUID) -> GeneratingTaskResult:
    return GeneratingTaskResult(
        result=OperationResult(status=True, message="Demanded catalog is ready"),
        link=f"xls/{ticket_id}.xlsx",
    )
