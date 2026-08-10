#!/usr/bin/env python3
"""Bounded, credential-free smoke checks for a loopback Paperclip pilot."""

from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, urlunparse

ALLOWED_HOSTS = {"127.0.0.1", "localhost", "::1"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Turn redirects into HTTP errors instead of following them."""

    def redirect_request(self, request, file_pointer, code, message, headers, url):
        return None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_loopback(address: str) -> bool:
    parsed = ipaddress.ip_address(address)
    if isinstance(parsed, ipaddress.IPv6Address) and parsed.ipv4_mapped:
        parsed = parsed.ipv4_mapped
    return parsed.is_loopback


def render_receipt(receipt: dict[str, Any], destination: Path | None) -> None:
    rendered = json.dumps(receipt, indent=2) + "\n"
    if destination:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


def request_metadata(
    display_url: str,
    connection_url: str,
    *,
    accept: str,
    host_header: str,
    expected_content_type: str,
    body_marker: bytes | None = None,
) -> dict[str, object]:
    request = urllib.request.Request(
        connection_url,
        headers={
            "Accept": accept,
            "Host": host_header,
            "User-Agent": "awesome-agentic-tech-paperclip-smoke/2",
        },
    )
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        NoRedirect(),
    )
    try:
        with opener.open(request, timeout=10) as response:
            body = response.read(1_000_000)
            content_type = response.headers.get("Content-Type", "")
            marker_present = body_marker is None or body_marker.lower() in body.lower()
            content_type_matches = expected_content_type in content_type.lower()
            if expected_content_type == "application/json":
                try:
                    parsed_body = json.loads(body)
                    marker_present = parsed_body.get("status") == "ok"
                except (AttributeError, json.JSONDecodeError, UnicodeDecodeError):
                    marker_present = False
            return {
                "url": display_url,
                "status": response.status,
                "content_type": content_type,
                "content_type_matches": content_type_matches,
                "content_length_observed": len(body),
                "body_is_nonempty": bool(body),
                "expected_marker_present": marker_present,
                "redirect_followed": False,
                "passed": response.status == 200
                and bool(body)
                and content_type_matches
                and marker_present,
            }
    except urllib.error.HTTPError as exc:
        return {
            "url": display_url,
            "status": exc.code,
            "content_type": exc.headers.get("Content-Type", ""),
            "content_type_matches": False,
            "content_length_observed": 0,
            "body_is_nonempty": False,
            "expected_marker_present": False,
            "redirect_followed": False,
            "passed": False,
            "error": f"HTTP {exc.code}",
        }
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {
            "url": display_url,
            "status": None,
            "content_type": "",
            "content_type_matches": False,
            "content_length_observed": 0,
            "body_is_nonempty": False,
            "expected_marker_present": False,
            "redirect_followed": False,
            "passed": False,
            "error": type(exc).__name__,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:3100")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    receipt = {
        "schema": "paperclip-pilot-smoke.v1",
        "startedAt": utc_now(),
        "status": "error",
        "passed": False,
        "requestCredentialHeadersSent": False,
        "credentialStateOfTargetService": "not_assessed",
    }
    try:
        base = args.base_url.rstrip("/")
        parsed = urlparse(base)
        if (
            parsed.scheme != "http"
            or parsed.hostname not in ALLOWED_HOSTS
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or parsed.path not in {"", "/"}
        ):
            raise ValueError("refusing unsafe or non-loopback Paperclip smoke target")

        port = parsed.port or 80
        addresses = sorted(
            {item[4][0] for item in socket.getaddrinfo(parsed.hostname, port)}
        )
        if not addresses or not all(is_loopback(address) for address in addresses):
            raise ValueError("target did not resolve exclusively to loopback addresses")

        # Connect to the validated literal address so the request cannot trigger
        # a second DNS resolution. Prefer IPv4 when both families are present.
        connected_address = sorted(addresses, key=lambda value: ":" in value)[0]
        literal_host = (
            f"[{connected_address}]" if ":" in connected_address else connected_address
        )
        authority = f"{literal_host}:{port}"
        host_header = parsed.netloc

        def connection_url(path: str) -> str:
            return urlunparse(("http", authority, path, "", "", ""))

        checks = [
            request_metadata(
                f"{base}/api/health",
                connection_url("/api/health"),
                accept="application/json",
                host_header=host_header,
                expected_content_type="application/json",
            ),
            request_metadata(
                f"{base}/",
                connection_url("/"),
                accept="text/html",
                host_header=host_header,
                expected_content_type="text/html",
                body_marker=b"paperclip",
            ),
        ]
        loopback_only = all(is_loopback(address) for address in addresses)
        passed = loopback_only and all(bool(check["passed"]) for check in checks)
        receipt.update(
            {
                "finishedAt": utc_now(),
                "status": "passed" if passed else "failed",
                "baseUrl": base,
                "resolvedAddresses": addresses,
                "connectedAddress": connected_address,
                "loopbackOnly": loopback_only,
                "redirectPolicy": "forbid",
                "checks": checks,
                "passed": passed,
            }
        )
    except (OSError, ValueError, urllib.error.URLError) as exc:
        receipt.update(
            {
                "finishedAt": utc_now(),
                "status": "error",
                "error": {"type": type(exc).__name__, "message": str(exc)},
                "passed": False,
            }
        )

    render_receipt(receipt, args.receipt)
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
