from dataclasses import dataclass


@dataclass
class ResultInfo:
    status: bool
    message: str = ""
