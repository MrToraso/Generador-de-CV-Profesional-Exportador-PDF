from app.db.session import engine
from app.models.analysis import AnalysisResult
from app.models.job_offer import JobOffer
from app.models.resume import Resume
from app.models.user import User
from app.models.base_class import Base


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


__all__ = ["Base", "User", "Resume", "JobOffer", "AnalysisResult", "create_tables"]
