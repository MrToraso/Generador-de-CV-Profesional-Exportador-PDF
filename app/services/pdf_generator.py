import re


def _sanitize_text(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    return normalized[:4000]


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_optimized_resume_pdf(
    candidate_name: str,
    resume_text: str,
    job_title: str,
    score: float,
    matched_keywords: list[str],
    missing_keywords: list[str],
) -> bytes:
    lines = [
        f"ResumeFix - CV optimizado: {candidate_name}",
        f"Vacante objetivo: {job_title}",
        f"Score compatibilidad: {score}%",
        f"Keywords coincidentes: {', '.join(matched_keywords) or 'N/A'}",
        f"Keywords por reforzar: {', '.join(missing_keywords[:20]) or 'N/A'}",
        "",
        "Resumen profesional ATS-friendly:",
        _sanitize_text(resume_text),
    ]

    y = 780
    text_ops = ["BT", "/F1 11 Tf", "50 800 Td"]
    for line in lines:
        safe = _escape_pdf_text(line)
        text_ops.append(f"1 0 0 1 50 {y} Tm ({safe}) Tj")
        y -= 16
        if y < 60:
            break
    text_ops.append("ET")
    content_stream = "\n".join(text_ops).encode("latin-1", errors="ignore")

    objects = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n")
    objects.append(
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
    )
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    objects.append(
        f"5 0 obj << /Length {len(content_stream)} >> stream\n".encode("ascii")
        + content_stream
        + b"\nendstream endobj\n"
    )

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.extend(
        f"trailer << /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF".encode(
            "ascii"
        )
    )
    return bytes(pdf)
