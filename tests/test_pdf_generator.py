from app.services.pdf_generator import build_optimized_resume_pdf


def test_build_optimized_resume_pdf_returns_pdf_bytes() -> None:
    pdf = build_optimized_resume_pdf(
        candidate_name="Jane Doe",
        resume_text="Python developer with FastAPI and AWS experience.",
        job_title="Backend Engineer",
        score=82.5,
        matched_keywords=["python", "fastapi", "aws"],
        missing_keywords=["kubernetes"],
    )

    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 100
