from pathlib import Path

from .content import DOCS_DIR, GOVERNANCE_DOCUMENTS


def resolve_document_path(slug: str) -> Path | None:
    document = next((item for item in GOVERNANCE_DOCUMENTS if item["slug"] == slug), None)
    if document is None or not DOCS_DIR.exists():
        return None

    for path in sorted(DOCS_DIR.glob("*.pdf")):
        name = path.name.lower()
        if all(token.lower() in name for token in document["tokens"]):
            return path
    return None
