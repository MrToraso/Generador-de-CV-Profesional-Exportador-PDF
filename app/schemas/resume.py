from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    job_title: str = Field(min_length=2, max_length=160)
    job_description: str = Field(min_length=20)


class ResumeUploadResponse(BaseModel):
    id: int
    filename: str
