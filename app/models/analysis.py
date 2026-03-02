from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_class import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False)
    job_offer_id: Mapped[int] = mapped_column(ForeignKey("job_offers.id"), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    matched_keywords_count: Mapped[int] = mapped_column(Integer, nullable=False)
    total_keywords_count: Mapped[int] = mapped_column(Integer, nullable=False)
    matched_keywords: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    missing_keywords: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
    job_offer = relationship("JobOffer", back_populates="analyses")
