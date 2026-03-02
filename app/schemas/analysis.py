from datetime import datetime

from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    analysis_id: int
    score: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    matched_keywords_count: int
    total_keywords_count: int
    created_at: datetime


class AnalysisHistoryItem(BaseModel):
    id: int
    resume_filename: str
    job_title: str
    score: float
    created_at: datetime
