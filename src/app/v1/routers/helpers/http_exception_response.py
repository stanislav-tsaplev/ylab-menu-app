from http import HTTPStatus

from pydantic import BaseModel


class HTTPExceptionResponse(BaseModel):
    detail: str


def http_exception_response(
    status_code: int, detail: str | None = None
) -> dict:
    if detail is None:
        detail = HTTPStatus(status_code).description

    return {
        status_code: {
            "description": HTTPStatus(status_code).phrase,
            "model": HTTPExceptionResponse,
            "content": {"application/json": {"example": {"detail": detail}}},
        }
    }
