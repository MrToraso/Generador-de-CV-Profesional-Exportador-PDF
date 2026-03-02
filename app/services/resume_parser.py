from io import BytesIO

from pypdf import PdfReader


class ResumeParserError(Exception):
    pass


def extract_text_from_upload(filename: str, raw_content: bytes) -> str:
    suffix = filename.lower().split(".")[-1]
    if suffix == "txt":
        return raw_content.decode("utf-8", errors="ignore").strip()
    if suffix == "pdf":
        reader = PdfReader(BytesIO(raw_content))
        text = "\n".join((page.extract_text() or "") for page in reader.pages).strip()
        return text
    raise ResumeParserError("Formato no soportado. Usa .txt o .pdf")
