from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.analysis import AnalysisResult
from app.models.job_offer import JobOffer
from app.models.resume import Resume
from app.models.user import PlanType, User
from app.schemas.analysis import AnalysisHistoryItem, AnalysisResponse
from app.services.matching import calculate_match
from app.services.pdf_generator import build_optimized_resume_pdf
from app.services.resume_parser import ResumeParserError, extract_text_from_upload
from app.utils.limits import FREE_PLAN_ANALYSIS_LIMIT

router = APIRouter(prefix="/resume-analysis", tags=["resume-analysis"])


@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_resume(
    job_title: str = Form(...),
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    if user.plan == PlanType.FREE:
        total_analyses = db.scalar(
            select(func.count(AnalysisResult.id)).where(AnalysisResult.user_id == user.id)
        )
        if total_analyses >= FREE_PLAN_ANALYSIS_LIMIT:
            raise HTTPException(
                status_code=403,
                detail="Límite del plan free alcanzado. Actualiza a premium.",
            )

    raw_content = await resume_file.read()
    try:
        extracted_text = extract_text_from_upload(resume_file.filename, raw_content)
    except ResumeParserError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not extracted_text:
        raise HTTPException(status_code=400, detail="No se pudo extraer texto del CV")

    resume = Resume(user_id=user.id, filename=resume_file.filename, content=extracted_text)
    offer = JobOffer(user_id=user.id, title=job_title, description=job_description)
    db.add_all([resume, offer])
    db.flush()

    match = calculate_match(extracted_text, job_description)
    analysis = AnalysisResult(
        user_id=user.id,
        resume_id=resume.id,
        job_offer_id=offer.id,
        score=match["score"],
        matched_keywords_count=match["matched_count"],
        total_keywords_count=match["total_count"],
        matched_keywords=match["matched_keywords"],
        missing_keywords=match["missing_keywords"],
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return AnalysisResponse(
        analysis_id=analysis.id,
        score=analysis.score,
        matched_keywords=analysis.matched_keywords,
        missing_keywords=analysis.missing_keywords,
        matched_keywords_count=analysis.matched_keywords_count,
        total_keywords_count=analysis.total_keywords_count,
        created_at=analysis.created_at,
    )


@router.get("/history", response_model=list[AnalysisHistoryItem])
def analysis_history(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[AnalysisHistoryItem]:
    query = (
        select(AnalysisResult, Resume.filename, JobOffer.title)
        .join(Resume, Resume.id == AnalysisResult.resume_id)
        .join(JobOffer, JobOffer.id == AnalysisResult.job_offer_id)
        .where(AnalysisResult.user_id == user.id)
        .order_by(AnalysisResult.created_at.desc())
    )
    rows = db.execute(query).all()
    return [
        AnalysisHistoryItem(
            id=analysis.id,
            resume_filename=filename,
            job_title=title,
            score=analysis.score,
            created_at=analysis.created_at,
        )
        for analysis, filename, title in rows
    ]


@router.get("/{analysis_id}/export-pdf")
def export_optimized_pdf(
    analysis_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    query = (
        select(AnalysisResult, Resume, JobOffer)
        .join(Resume, Resume.id == AnalysisResult.resume_id)
        .join(JobOffer, JobOffer.id == AnalysisResult.job_offer_id)
        .where(AnalysisResult.id == analysis_id, AnalysisResult.user_id == user.id)
    )
    row = db.execute(query).first()
    if not row:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")

    analysis, resume, offer = row
    pdf_bytes = build_optimized_resume_pdf(
        candidate_name=user.full_name,
        resume_text=resume.content,
        job_title=offer.title,
        score=analysis.score,
        matched_keywords=analysis.matched_keywords,
        missing_keywords=analysis.missing_keywords,
    )
    filename = f"resumefix_optimized_{analysis_id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
