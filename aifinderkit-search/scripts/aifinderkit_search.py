#!/usr/bin/env python3
"""Dependency-free client for the AI Finder Kit Search API."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import stat
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "https://api.aifinderkit.com/v1"
CLIENT_VERSION = "1.3.0"
DEFAULT_KEY_FILE = Path("~/.config/aifinderkit/credentials").expanduser()


def credential_path() -> Path:
    configured = os.getenv("AIFINDERKIT_API_KEY_FILE", "").strip()
    return Path(configured).expanduser() if configured else DEFAULT_KEY_FILE


def load_api_key() -> str:
    environment_key = os.getenv("AIFINDERKIT_API_KEY", "").strip()
    if environment_key:
        return environment_key
    path = credential_path()
    if not path.is_file():
        raise SystemExit(
            "AIFINDERKIT_API_KEY is not set and no protected credential file exists"
        )
    if os.name == "posix" and stat.S_IMODE(path.stat().st_mode) & 0o077:
        raise SystemExit(f"Credential file permissions are too broad: {path}; require 0600")
    api_key = path.read_text(encoding="utf-8").strip()
    if not api_key:
        raise SystemExit(f"Credential file is empty: {path}")
    return api_key


def configure_key() -> Path:
    api_key = os.getenv("AIFINDERKIT_API_KEY", "").strip()
    if not api_key:
        api_key = getpass.getpass("AI Finder Kit API key: ").strip()
    if not api_key:
        raise SystemExit("API key must not be empty")
    path = credential_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(api_key + "\n")
    if os.name == "posix":
        path.chmod(0o600)
    return path


def request_json(path: str, payload: dict | None, timeout: int) -> dict:
    api_key = load_api_key()
    base_url = os.getenv("AIFINDERKIT_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}{path}",
        data=data,
        method="GET" if payload is None else "POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"aifinderkit-search-skill/{CLIENT_VERSION}",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        try:
            detail = json.load(error)
        except Exception:
            detail = {"detail": error.reason}
        raise SystemExit(
            f"AI Finder Kit API returned HTTP {error.code}: "
            f"{json.dumps(detail, ensure_ascii=False)}"
        ) from error
    except urllib.error.URLError as error:
        raise SystemExit(f"Could not reach AI Finder Kit API: {error.reason}") from error


def add_search_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--mode", choices=["fast", "balanced", "deep"], default="balanced")
    parser.add_argument("--preset", choices=["academic-relaxed", "academic-strict"])
    parser.add_argument("--freshness", choices=["day", "week", "month", "year"])
    parser.add_argument("--language", help="Preferred result language, for example zh or en")
    parser.add_argument(
        "--category",
        dest="categories",
        action="append",
        help="Search category; repeat up to five times",
    )
    parser.add_argument("--include-domain", dest="include_domains", action="append")
    parser.add_argument("--exclude-domain", dest="exclude_domains", action="append")


def parse_key_values(values: list[str] | None) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for item in values or []:
        if "=" not in item:
            raise SystemExit("--vertical-param must use key=value format")
        key, value = item.split("=", 1)
        if not key:
            raise SystemExit("--vertical-param key must not be empty")
        parsed[key] = value
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {CLIENT_VERSION}")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--compact", action="store_true")
    commands = parser.add_subparsers(dest="command", required=True)

    search = commands.add_parser("search", help="Run one aggregate search")
    search.add_argument("query")
    add_search_options(search)
    search.add_argument("--vertical-domain")
    search.add_argument("--vertical-sub-domain")
    search.add_argument("--vertical-param", dest="vertical_params", action="append")

    batch = commands.add_parser("batch", help="Run two to five searches")
    batch.add_argument("--query", action="append", required=True)
    add_search_options(batch)

    fetch = commands.add_parser("fetch", help="Extract readable text from a URL")
    fetch.add_argument("url")
    fetch.add_argument("--max-chars", type=int, default=30000)

    map_command = commands.add_parser("map", help="List bounded same-host page links")
    map_command.add_argument("url")
    map_command.add_argument("--max-links", type=int, default=50)

    crawl = commands.add_parser("crawl", help="Crawl a small same-host static site section")
    crawl.add_argument("url")
    crawl.add_argument("--max-pages", type=int, default=5)
    crawl.add_argument("--max-depth", type=int, default=1)
    crawl.add_argument("--max-chars-per-page", type=int, default=12000)

    domains = commands.add_parser("domains", help="Discover AnySearch vertical sub-domains")
    domains.add_argument("--domain", dest="domains", action="append", required=True)

    research = commands.add_parser("research", help="Search and extract top pages")
    research.add_argument("query")
    research.add_argument("--subquery", dest="subqueries", action="append")
    research.add_argument("--limit", type=int, default=10)
    research.add_argument("--fetch-top", type=int, default=3)
    research.add_argument("--preset", choices=["academic-relaxed", "academic-strict"])
    research.add_argument("--freshness", choices=["day", "week", "month", "year"])
    research.add_argument("--language")
    research.add_argument("--category", dest="categories", action="append")
    research.add_argument("--include-domain", dest="include_domains", action="append")
    research.add_argument("--exclude-domain", dest="exclude_domains", action="append")

    commands.add_parser("meta", help="Show access tier and limits")
    commands.add_parser(
        "configure", help="Store a key in a protected file outside the skill directory"
    )
    commands.add_parser(
        "doctor", help="Verify authentication and print a sanitized capability summary"
    )
    return parser


def build_request(args: argparse.Namespace) -> tuple[str, dict | None]:
    if args.command == "search":
        path = "/search"
        payload = {
            "query": args.query,
            "limit": args.limit,
            "mode": args.mode,
            "preset": args.preset,
            "freshness": args.freshness,
            "language": args.language,
            "categories": args.categories or [],
            "include_domains": args.include_domains or [],
            "exclude_domains": args.exclude_domains or [],
            "vertical_domain": args.vertical_domain,
            "vertical_sub_domain": args.vertical_sub_domain,
            "vertical_params": parse_key_values(args.vertical_params),
        }
    elif args.command == "batch":
        if not 1 <= len(args.query) <= 5:
            raise SystemExit("batch accepts one to five --query values")
        path = "/batch-search"
        payload = {
            "queries": args.query,
            "limit": args.limit,
            "mode": args.mode,
            "preset": args.preset,
            "freshness": args.freshness,
            "language": args.language,
            "categories": args.categories or [],
            "include_domains": args.include_domains or [],
            "exclude_domains": args.exclude_domains or [],
        }
    elif args.command == "fetch":
        path = "/fetch"
        payload = {"url": args.url, "max_chars": args.max_chars}
    elif args.command == "map":
        path = "/map"
        payload = {"url": args.url, "max_links": args.max_links}
    elif args.command == "crawl":
        path = "/crawl"
        payload = {
            "url": args.url,
            "max_pages": args.max_pages,
            "max_depth": args.max_depth,
            "max_chars_per_page": args.max_chars_per_page,
        }
    elif args.command == "domains":
        path = "/vertical-domains"
        payload = {"domains": args.domains}
    elif args.command == "research":
        path = "/research"
        payload = {
            "query": args.query,
            "subqueries": args.subqueries or [],
            "limit": args.limit,
            "fetch_top": args.fetch_top,
            "preset": args.preset,
            "freshness": args.freshness,
            "language": args.language,
            "categories": args.categories or [],
            "include_domains": args.include_domains or [],
            "exclude_domains": args.exclude_domains or [],
        }
    else:
        path = "/search/meta"
        payload = None

    # Drop optional null fields so the payload stays compatible with strict clients.
    if payload is not None:
        payload = {key: value for key, value in payload.items() if value is not None}
    return path, payload


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "configure":
        path = configure_key()
        print(json.dumps({"ok": True, "credential_file": str(path)}, ensure_ascii=False))
        return
    path, payload = build_request(args)
    result = request_json(path, payload, args.timeout)
    if args.command == "doctor":
        result = {
            "ok": True,
            "client_version": CLIENT_VERSION,
            "api_version": result.get("version"),
            "source_tier": result.get("source_tier"),
            "endpoints": result.get("endpoints", []),
            "modes": result.get("modes", []),
            "presets": result.get("presets", []),
            "limits": result.get("limits", {}),
            "credentials_in_bundle": False,
        }
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2))


if __name__ == "__main__":
    main()
