from dataclasses import dataclass
from uuid import UUID


@dataclass
class OperationResult:
    status: bool
    message: str = ""


@dataclass
class GeneratingTaskTicket:
    ticket_id: UUID


@dataclass
class GeneratingTaskResult:
    result: OperationResult
    link: str | None = None
