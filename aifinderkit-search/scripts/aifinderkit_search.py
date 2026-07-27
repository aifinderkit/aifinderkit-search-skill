#!/usr/bin/env python3
"""Dependency-free client for the AI Finder Kit Search API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


DEFAULT_BASE_URL = "https://api.aifinderkit.com/v1"
CLIENT_VERSION = "1.1.0"


def request_json(path: str, payload: dict | None, timeout: int) -> dict:
    api_key = os.getenv("AIFINDERKIT_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("AIFINDERKIT_API_KEY is not set")
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
    parser.add_argument("--freshness", choices=["day", "week", "month", "year"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {CLIENT_VERSION}")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--compact", action="store_true")
    commands = parser.add_subparsers(dest="command", required=True)

    search = commands.add_parser("search", help="Run one aggregate search")
    search.add_argument("query")
    add_search_options(search)

    batch = commands.add_parser("batch", help="Run two to five searches")
    batch.add_argument("--query", action="append", required=True)
    add_search_options(batch)

    fetch = commands.add_parser("fetch", help="Extract readable text from a URL")
    fetch.add_argument("url")
    fetch.add_argument("--max-chars", type=int, default=30000)

    research = commands.add_parser("research", help="Search and extract top pages")
    research.add_argument("query")
    research.add_argument("--limit", type=int, default=10)
    research.add_argument("--fetch-top", type=int, default=3)
    research.add_argument("--freshness", choices=["day", "week", "month", "year"])

    commands.add_parser("meta", help="Show access tier and limits")
    commands.add_parser("doctor", help="Verify authentication and print a sanitized capability summary")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "search":
        path = "/search"
        payload = {
            "query": args.query,
            "limit": args.limit,
            "mode": args.mode,
            "freshness": args.freshness,
        }
    elif args.command == "batch":
        if not 1 <= len(args.query) <= 5:
            raise SystemExit("batch accepts one to five --query values")
        path = "/batch-search"
        payload = {
            "queries": args.query,
            "limit": args.limit,
            "mode": args.mode,
            "freshness": args.freshness,
        }
    elif args.command == "fetch":
        path = "/fetch"
        payload = {"url": args.url, "max_chars": args.max_chars}
    elif args.command == "research":
        path = "/research"
        payload = {
            "query": args.query,
            "limit": args.limit,
            "fetch_top": args.fetch_top,
            "freshness": args.freshness,
        }
    else:
        path = "/search/meta"
        payload = None

    # Drop optional null fields so the payload stays compatible with strict clients.
    if payload is not None:
        payload = {key: value for key, value in payload.items() if value is not None}
    result = request_json(path, payload, args.timeout)
    if args.command == "doctor":
        result = {
            "ok": True,
            "client_version": CLIENT_VERSION,
            "api_version": result.get("version"),
            "source_tier": result.get("source_tier"),
            "endpoints": result.get("endpoints", []),
            "modes": result.get("modes", []),
            "limits": result.get("limits", {}),
            "credentials_in_bundle": False,
        }
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2))


if __name__ == "__main__":
    main()
