from app.services.matching import calculate_match


def test_calculate_match_score() -> None:
    resume = "Python FastAPI Docker SQL AWS"
    job = "Se busca desarrollador Python con FastAPI y AWS"

    result = calculate_match(resume, job)

    assert result["score"] > 0
    assert "python" in result["matched_keywords"]
    assert result["matched_count"] <= result["total_count"]
