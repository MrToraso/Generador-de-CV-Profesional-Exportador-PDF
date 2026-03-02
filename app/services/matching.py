import re
from collections import Counter

TOKEN_PATTERN = re.compile(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9+#.]{3,}")
STOPWORDS = {
    "para",
    "con",
    "las",
    "los",
    "the",
    "and",
    "que",
    "una",
    "por",
    "del",
    "this",
    "you",
}


def extract_keywords(text: str) -> list[str]:
    tokens = [t.lower() for t in TOKEN_PATTERN.findall(text)]
    filtered = [t for t in tokens if t not in STOPWORDS]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(40)]


def calculate_match(resume_text: str, job_description: str) -> dict[str, object]:
    resume_keywords = set(extract_keywords(resume_text))
    job_keywords = extract_keywords(job_description)
    unique_job_keywords = list(dict.fromkeys(job_keywords))

    if not unique_job_keywords:
        return {
            "score": 0.0,
            "matched_keywords": [],
            "missing_keywords": [],
            "matched_count": 0,
            "total_count": 0,
        }

    matched = sorted([kw for kw in unique_job_keywords if kw in resume_keywords])
    missing = sorted([kw for kw in unique_job_keywords if kw not in resume_keywords])
    score = round((len(matched) / len(unique_job_keywords)) * 100, 2)

    return {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "matched_count": len(matched),
        "total_count": len(unique_job_keywords),
    }
