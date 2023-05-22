from typing import List
from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import datetime


class DiagnosisRequest(BaseModel):
    diag_code: str
    full_code: str
    abb_desc: str
    full_desc: str
    code: str
    title: str


class UpdateDiagnosisRequest(BaseModel):
    diag_code: Optional[str]
    full_code: Optional[str]
    abb_desc: Optional[str]
    full_desc: Optional[str]
    code: Optional[str]
    title: Optional[str]


class DiagnosisUpdateResponse(BaseModel):
    id: uuid.UUID
    diag_code: Optional[str]
    full_code: Optional[str]
    abb_desc: Optional[str]
    full_desc: Optional[str]
    code: Optional[str]
    title: Optional[str]

    class Config:
        orm_mode = True


class UploadFileRequest(BaseModel):
    file_name: str
    recipient_email: str
    file_content: str


class DiagnosisResponse(DiagnosisRequest):
    id: uuid.UUID
    diag_code: str
    full_code: str
    abb_desc: str
    full_desc: str
    code: str
    title: str
    created_at: datetime


# class DiagnosesListResponse(BaseModel):
#     metadata: dict
#     data: List[DiagnosisResponse]
