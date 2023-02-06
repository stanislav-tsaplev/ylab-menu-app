from dataclasses import dataclass


@dataclass
class OperationResult:
    status: bool
    message: str = ""


@dataclass
class TaskTicket:
    ticket_id: str


@dataclass
class TaskResult:
    ticket_id: str
    status: str
    file_path: str | None = None
