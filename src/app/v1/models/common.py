from dataclasses import dataclass
from uuid import UUID


@dataclass
class OperationResult:
    status: bool
    message: str = ""


@dataclass
class TaskTicket:
    ticket_id: UUID


@dataclass
class TaskResult:
    result: OperationResult
    link: str | None = None
