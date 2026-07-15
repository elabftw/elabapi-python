#!/usr/bin/env python

from pathlib import Path

import elabapi_python
from client import api_client

# Folder containing the PDF files
PDF_FOLDER = Path("data/sops")

# Target resource category: items_types.id
TARGET_CATEGORY_ID = 1

items_api = elabapi_python.ItemsApi(api_client)
uploads_api = elabapi_python.UploadsApi(api_client)


def create_resource_from_pdf(pdf_path: Path) -> int:
    title = pdf_path.stem

    response = items_api.post_item_with_http_info(
        body={
            "category": TARGET_CATEGORY_ID,
            "tags": ["imported"],
        }
    )

    location = response[2].get("Location")
    if location is None:
        raise RuntimeError(f"No Location header returned for {pdf_path.name}")

    item_id = int(location.rstrip("/").split("/")[-1])

    # patch_item has the unusual signature (body, id), so use named arguments.
    items_api.patch_item(
        id=item_id,
        body={
            "title": title,
        },
    )

    uploads_api.post_upload(
        "items",
        item_id,
        file=str(pdf_path),
        comment="Uploaded with APIv2",
    )

    print(f"Created resource {item_id}: {title}")
    return item_id


def main() -> None:
    if not PDF_FOLDER.is_dir():
        raise NotADirectoryError(f"PDF folder does not exist: {PDF_FOLDER}")

    pdf_files = sorted(
        path for path in PDF_FOLDER.iterdir()
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    if not pdf_files:
        print(f"No PDF files found in {PDF_FOLDER}")
        return

    for pdf_path in pdf_files:
        try:
            create_resource_from_pdf(pdf_path)
        except Exception as exc:
            print(f"Failed to import {pdf_path.name}: {exc}")


if __name__ == "__main__":
    main()
