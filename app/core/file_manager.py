# app/core/file_manager.py
from __future__ import annotations
import re
import shutil
import hashlib
from pathlib import Path
from typing import Union

from app.core.database import archive_root


def slugify(s: str) -> str:
    """
    Turn an arbitrary string into a filesystem-safe slug.
    Example: "Security Engineer @ R&D" -> "security_engineer_r_d"
    """
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)  # Replace non-alphanumeric with _
    s = re.sub(r"_+", "_", s)          # Collapse multiple underscores
    return s.strip("_")


def company_dir(company: str) -> Path:
    """
    Directory for a specific company's resumes.
    Creates it if missing.
    """
    d = archive_root() / slugify(company)
    d.mkdir(parents=True, exist_ok=True)
    return d


def next_version(company: str, role: str, date_str: str) -> int:
    """
    Determine the next available version number for a given company/role/date.
    """
    d = company_dir(company)
    pattern = f"{date_str}__{slugify(company)}__{slugify(role)}__v"
    existing = [p.name for p in d.glob("*.pdf") if p.name.startswith(pattern)]
    if not existing:
        return 1
    versions = []
    for name in existing:
        match = re.search(r"__v(\\d+)\\.pdf$", name)
        if match:
            versions.append(int(match.group(1)))
    return max(versions, default=0) + 1


def make_filename(date_str: str, company: str, role: str, version: int) -> str:
    """
    Create the standardized filename.
    """
    return f"{date_str}__{slugify(company)}__{slugify(role)}__v{version}.pdf"


def copy_to_archive(
    src: Union[str, Path],
    company: str,
    role: str,
    date_str: str,
) -> Path:
    """
    Copy a source PDF to the archive folder with standardized filename + versioning.
    Returns the destination Path.
    """
    src = Path(src).expanduser().resolve()
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"Source file does not exist: {src}")
    if src.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are allowed")

    version = next_version(company, role, date_str)
    fname = make_filename(date_str, company, role, version)
    dest = company_dir(company) / fname

    counter = 1
    while dest.exists():
        dest = dest.with_name(dest.stem + f"_dup{counter}" + dest.suffix)
        counter += 1

    shutil.copy2(src, dest)
    return dest


def compute_hash(path: Union[str, Path]) -> str:
    """
    Compute SHA256 hash of a file.
    """
    path = Path(path)
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
