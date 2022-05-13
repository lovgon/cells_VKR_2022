from uuid import UUID

from pydantic import BaseModel


class FileDetectResult(BaseModel):
    input_file: str
    output_file: str
    file_name: str
    cells: int = 0
    time: float


class ProcessModelResponse(BaseModel):
    files: list[FileDetectResult]
    avg_time: float
    total_time: float
    econom_time: float
    batch_id: UUID
