#!/usr/bin/env python3
"""Fetch Directus folder file names and save them to a text file."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Iterable, List, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the `filename_disk` values for files in a Directus folder."
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("DIRECTUS_BASE_URL", "https://db.dl.tlu.ee"),
        help="Directus base URL (default: https://db.dl.tlu.ee or DIRECTUS_BASE_URL env).",
    )
    parser.add_argument(
        "--folder-id",
        required=True,
        help="UUID of the Directus folder whose file list should be exported.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("DIRECTUS_TOKEN"),
        help="Static token or personal access token (default: DIRECTUS_TOKEN env).",
    )
    parser.add_argument(
        "--output",
        default="file_lists/directus_filenames.txt",
        help="Destination text file (default: file_lists/directus_filenames.txt).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Number of items per request (default: 200).",
    )
    return parser.parse_args()


def ensure_positive_limit(limit: int) -> int:
    if limit <= 0:
        raise ValueError("--limit must be a positive integer")
    return limit


def fetch_filenames(
    base_url: str,
    folder_id: str,
    token: Optional[str],
    limit: int,
) -> List[str]:
    """Retrieve all filename_disk values from the specified folder."""

    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Strip trailing slash to avoid double slashes in the final URL.
    api_url = base_url.rstrip("/") + "/files"

    filenames: List[str] = []
    offset = 0
    total: Optional[int] = None

    while True:
        params = {
            "filter[folder][_eq]": folder_id,
            "fields": "filename_disk",
            "limit": limit,
            "offset": offset,
            "meta": "total_count",
        }
        encoded_params = urllib.parse.urlencode(params, doseq=True)
        request_url = f"{api_url}?{encoded_params}"
        request = urllib.request.Request(request_url, headers=headers)

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read()
                encoding = response.headers.get_content_charset("utf-8")
                payload = json.loads(body.decode(encoding))
        except urllib.error.HTTPError as error:
            raise RuntimeError(
                f"Request failed at offset {offset}: HTTP {error.code}"
            ) from error
        except urllib.error.URLError as error:
            raise RuntimeError(
                f"Network error at offset {offset}: {error.reason}"
            ) from error

        data = payload.get("data", [])
        meta = payload.get("meta", {})
        if total is None:
            total = meta.get("total_count")

        filenames.extend(
            item["filename_disk"]
            for item in data
            if item.get("filename_disk")
        )

        if not data:
            break

        offset += limit
        # Stop when we reach the total number of records Directus reported.
        if total is not None and offset >= total:
            break

        # Defensive break in case Directus stops returning rows before total is known.
        if len(data) < limit:
            break

    return filenames


def write_lines(path: str, lines: Iterable[str]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for line in lines:
            handle.write(f"{line}\n")


def main() -> None:
    args = parse_args()

    try:
        limit = ensure_positive_limit(args.limit)
        filenames = fetch_filenames(
            base_url=args.base_url,
            folder_id=args.folder_id,
            token=args.token,
            limit=limit,
        )
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    write_lines(args.output, filenames)
    print(f"Saved {len(filenames)} filenames to {args.output}")


if __name__ == "__main__":
    main()
