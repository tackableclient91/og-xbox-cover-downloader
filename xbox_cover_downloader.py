#!/usr/bin/env python3
"""OG Xbox game cover downloader.

Data source:
- https://github.com/libretro-thumbnails/Microsoft_-_Xbox
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

REPO_OWNER = "libretro-thumbnails"
REPO_NAME = "Microsoft_-_Xbox"
GITHUB_API_TREE = "https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
RAW_BASE = "https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
CACHE_SECONDS = 24 * 60 * 60
DEFAULT_DOWNLOAD_RETRIES = 3


@dataclass
class CoverEntry:
    title: str
    filename: str
    path: str
    branch: str

    @property
    def url(self) -> str:
        encoded_path = quote(self.path, safe="/")
        return RAW_BASE.format(
            owner=REPO_OWNER,
            repo=REPO_NAME,
            branch=self.branch,
            path=encoded_path,
        )


def http_get_json(url: str) -> dict:
    req = Request(
        url,
        headers={
            "User-Agent": "xbox-cover-downloader/1.0",
            "Accept": "application/vnd.github+json",
        },
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_cover_index() -> tuple[str, list[str]]:
    """Return branch + list of paths inside Named_Boxarts."""
    branches = ["master", "main"]
    errors: list[str] = []

    for branch in branches:
        url = GITHUB_API_TREE.format(owner=REPO_OWNER, repo=REPO_NAME, branch=branch)
        try:
            payload = http_get_json(url)
            tree = payload.get("tree", [])
            paths = [
                item["path"]
                for item in tree
                if item.get("type") == "blob"
                and str(item.get("path", "")).startswith("Named_Boxarts/")
                and str(item.get("path", "")).lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            ]
            if paths:
                return branch, paths
            errors.append(f"No boxart files found on branch '{branch}'.")
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            errors.append(f"{branch}: {exc}")

    raise RuntimeError("Unable to build cover index. " + " | ".join(errors))


def load_cached_index(cache_file: Path) -> dict | None:
    if not cache_file.exists():
        return None

    try:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(data, dict):
        return None

    ts = data.get("timestamp")
    if not isinstance(ts, (int, float)):
        return None

    if time.time() - ts > CACHE_SECONDS:
        return None

    return data


def save_cached_index(cache_file: Path, branch: str, paths: list[str]) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": int(time.time()),
        "branch": branch,
        "paths": paths,
    }
    cache_file.write_text(json.dumps(payload), encoding="utf-8")


def normalize_title(title: str) -> str:
    title = title.lower()
    title = title.replace("&", " and ")
    title = re.sub(r"\([^)]*\)", " ", title)
    title = re.sub(r"\[[^\]]*\]", " ", title)
    title = re.sub(r"[^a-z0-9]+", " ", title)
    return " ".join(title.split())


def filename_to_title(path: str) -> str:
    name = Path(path).stem
    name = re.sub(r"\s+", " ", name).strip()
    return name


def build_entries(branch: str, paths: Iterable[str]) -> list[CoverEntry]:
    entries: list[CoverEntry] = []
    for path in paths:
        filename = Path(path).name
        title = filename_to_title(path)
        entries.append(CoverEntry(title=title, filename=filename, path=path, branch=branch))
    return entries


def score_entry(query_norm: str, entry: CoverEntry, preferred_regions: list[str]) -> float:
    title_norm = normalize_title(entry.title)
    if not title_norm:
        return 0.0

    # Primary similarity signal.
    ratio = difflib.SequenceMatcher(a=query_norm, b=title_norm).ratio()

    # Bonus when all query tokens appear in title.
    q_tokens = query_norm.split()
    contains_all = all(token in title_norm for token in q_tokens) if q_tokens else False
    token_bonus = 0.2 if contains_all else 0.0

    # Region preference bonus from tags like (USA), (Europe), etc.
    region_bonus = 0.0
    lower_title = entry.title.lower()
    for idx, region in enumerate(preferred_regions):
        if region.lower() in lower_title:
            region_bonus = max(region_bonus, (len(preferred_regions) - idx) * 0.01)

    return ratio + token_bonus + region_bonus


def find_matches(
    entries: list[CoverEntry],
    query: str,
    max_results: int,
    exact: bool,
    preferred_regions: list[str],
) -> list[tuple[CoverEntry, float]]:
    query_norm = normalize_title(query)
    if not query_norm:
        return []

    if exact:
        exact_results: list[tuple[CoverEntry, float]] = []
        for entry in entries:
            if normalize_title(entry.title) == query_norm:
                exact_results.append((entry, 1.0))
        return exact_results[:max_results]

    ranked: list[tuple[CoverEntry, float]] = []
    for entry in entries:
        score = score_entry(query_norm, entry, preferred_regions)
        if score >= 0.35:
            ranked.append((entry, score))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:max_results]


def safe_name(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]", "_", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or "cover"


def download_cover(
    entry: CoverEntry,
    output_dir: Path,
    retries: int = DEFAULT_DOWNLOAD_RETRIES,
    timeout: int = 60,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(entry.filename).suffix or ".png"
    out_file = output_dir / f"{safe_name(entry.title)}{ext}"

    last_error: Exception | None = None
    attempts = max(1, retries)
    for attempt in range(1, attempts + 1):
        try:
            req = Request(entry.url, headers={"User-Agent": "xbox-cover-downloader/1.0"})
            with urlopen(req, timeout=timeout) as resp:
                out_file.write_bytes(resp.read())
            return out_file
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < attempts:
                # Brief linear backoff for transient network failures.
                time.sleep(attempt)

    if last_error is None:
        raise RuntimeError(f"Failed to download cover for {entry.title}")
    raise last_error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download original Xbox game covers.")
    parser.add_argument("query", nargs="?", help="Game title to search for.")
    parser.add_argument(
        "--file",
        dest="query_file",
        type=Path,
        help="Text file with one game title per line.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("covers"),
        help="Download folder (default: covers).",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=5,
        help="Max matches per query (default: 5).",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_only",
        help="List matches only; do not download.",
    )
    parser.add_argument(
        "--all-matches",
        action="store_true",
        help="Download all returned matches up to --max (default downloads best match only).",
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Exact title matching after normalization.",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force index refresh from GitHub (ignore cache).",
    )
    parser.add_argument(
        "--region-order",
        default="USA,World,Europe,Japan",
        help="Comma-separated preferred region order for tie-breaking.",
    )
    return parser.parse_args()


def read_queries(args: argparse.Namespace) -> list[str]:
    queries: list[str] = []

    if args.query:
        queries.append(args.query.strip())

    if args.query_file:
        if not args.query_file.exists():
            raise FileNotFoundError(f"Query file not found: {args.query_file}")
        lines = args.query_file.read_text(encoding="utf-8").splitlines()
        queries.extend(line.strip() for line in lines if line.strip() and not line.strip().startswith("#"))

    queries = [q for q in queries if q]
    if not queries:
        raise ValueError("Provide a title query or --file with titles.")

    return queries


def get_entries(cache_file: Path, refresh: bool) -> list[CoverEntry]:
    cached = load_cached_index(cache_file)

    if cached and not refresh:
        branch = str(cached.get("branch", "master"))
        paths = [str(p) for p in cached.get("paths", [])]
        return build_entries(branch, paths)

    try:
        branch, paths = fetch_cover_index()
        save_cached_index(cache_file, branch, paths)
        return build_entries(branch, paths)
    except RuntimeError:
        # If refresh fails, fall back to known-good cache instead of hard failing.
        if cached:
            branch = str(cached.get("branch", "master"))
            paths = [str(p) for p in cached.get("paths", [])]
            return build_entries(branch, paths)
        raise


def main() -> int:
    args = parse_args()

    if args.max < 1:
        raise ValueError("--max must be >= 1")

    queries = read_queries(args)
    preferred_regions = [p.strip() for p in args.region_order.split(",") if p.strip()]

    cache_file = Path.home() / ".cache" / "xbox_cover_index.json"
    entries = get_entries(cache_file, refresh=args.refresh)
    print(f"Indexed {len(entries)} OG Xbox covers.")

    total_downloaded = 0

    for query in queries:
        print(f"\nQuery: {query}")
        matches = find_matches(
            entries=entries,
            query=query,
            max_results=args.max,
            exact=args.exact,
            preferred_regions=preferred_regions,
        )

        if not matches:
            print("  No matches found.")
            continue

        for idx, (entry, score) in enumerate(matches, start=1):
            print(f"  {idx}. {entry.title} [score={score:.3f}]")

        if args.list_only:
            continue

        to_download = matches if args.all_matches else [matches[0]]
        for entry, _ in to_download:
            try:
                out_path = download_cover(entry, args.output)
                print(f"  Downloaded: {out_path}")
                total_downloaded += 1
            except (HTTPError, URLError, TimeoutError, OSError) as exc:
                print(f"  Failed: {entry.title} ({exc})")

    if args.list_only:
        print("\nDone. Listed matches only.")
    else:
        print(f"\nDone. Downloaded {total_downloaded} cover(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
