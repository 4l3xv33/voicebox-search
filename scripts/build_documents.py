#!/usr/bin/env python3

import json
import re
import subprocess
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_PATH = ROOT / "voi_newsletters.tar"
NEWSLETTER_DIR = ROOT / "voi_newsletters"
OUTPUT_PATH = ROOT / "documents.js"


def ensure_newsletters_extracted() -> None:
    with tarfile.open(ARCHIVE_PATH) as archive:
        archive.extractall(ROOT)


def clean_text(text: str) -> str:
    text = text.replace("\x0c", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def pdf_to_text(pdf_path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return clean_text(result.stdout)


def format_title(filename: str) -> str:
    stem = Path(filename).stem
    match = re.fullmatch(r"(\d{4})-(\d{2})-voi(?:-([a-z]))?", stem)
    if not match:
        return stem.replace("_", " ")

    year, month, suffix = match.groups()
    month_name = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }[month]

    title = f"{month_name} {year} VOI Newsletter"
    if suffix:
        title += f" ({suffix.upper()})"
    return title


def build_documents() -> list[dict[str, str]]:
    ensure_newsletters_extracted()

    documents = []
    for pdf_path in sorted(NEWSLETTER_DIR.glob("*.pdf")):
        documents.append(
            {
                "filename": pdf_path.name,
                "title": format_title(pdf_path.name),
                "filelink": pdf_path.relative_to(ROOT).as_posix(),
                "filecontent": pdf_to_text(pdf_path),
            }
        )

    return documents


def main() -> None:
    documents = build_documents()
    js = "const DOCUMENTS = " + json.dumps(documents, ensure_ascii=True, indent=2) + ";\n"
    OUTPUT_PATH.write_text(js, encoding="utf-8")
    print(f"Wrote {len(documents)} documents to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
