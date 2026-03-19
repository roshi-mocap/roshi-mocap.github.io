#!/usr/bin/env python3
"""Live preview for the Sphinx documentation site.

This script:
- builds ``docs/`` into ``documentation/``
- serves the generated site locally
- watches ``docs/`` for file changes
- rebuilds on change
- auto-opens the browser and auto-reloads after successful rebuilds
"""

from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


RELOAD_ENDPOINT = "/__docs_reload__"
HTML_SUFFIXES = {".html", ".htm"}
IGNORED_DIR_NAMES = {"_build", "__pycache__"}
RELOAD_SNIPPET = """
<script>
(() => {
  const endpoint = "%s";
  let version = null;

  async function poll() {
    try {
      const response = await fetch(endpoint, { cache: "no-store" });
      const payload = await response.json();
      if (version === null) {
        version = payload.version;
      } else if (payload.version !== version) {
        location.reload();
        return;
      }
    } catch (error) {
      // Keep polling while the local server is up.
    }

    setTimeout(poll, 1000);
  }

  poll();
})();
</script>
""".strip() % RELOAD_ENDPOINT


@dataclass
class BuildState:
    version: int = 0
    last_build_ok: bool = False
    last_build_started_at: float = 0.0
    last_build_finished_at: float = 0.0
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def mark_success(self) -> None:
        with self.lock:
            self.version += 1
            self.last_build_ok = True
            self.last_build_finished_at = time.time()

    def mark_failure(self) -> None:
        with self.lock:
            self.last_build_ok = False
            self.last_build_finished_at = time.time()

    def start_build(self) -> None:
        with self.lock:
            self.last_build_started_at = time.time()

    def payload(self) -> bytes:
        with self.lock:
            data = {
                "version": self.version,
                "last_build_ok": self.last_build_ok,
                "last_build_started_at": self.last_build_started_at,
                "last_build_finished_at": self.last_build_finished_at,
            }
        return json.dumps(data).encode("utf-8")


def inject_reload_snippet(html: str) -> str:
    if RELOAD_ENDPOINT in html:
        return html
    lower = html.lower()
    marker = "</body>"
    index = lower.rfind(marker)
    if index == -1:
        return html + "\n" + RELOAD_SNIPPET + "\n"
    return html[:index] + RELOAD_SNIPPET + "\n" + html[index:]


def should_watch(path: Path, source_dir: Path) -> bool:
    if not path.is_file():
        return False
    relative = path.relative_to(source_dir)
    return not any(part in IGNORED_DIR_NAMES for part in relative.parts)


def snapshot_tree(source_dir: Path) -> dict[str, int]:
    snapshot: dict[str, int] = {}
    for path in source_dir.rglob("*"):
        if not should_watch(path, source_dir):
            continue
        relative = str(path.relative_to(source_dir))
        snapshot[relative] = path.stat().st_mtime_ns
    return snapshot


def summarize_changes(previous: dict[str, int], current: dict[str, int]) -> str:
    changed: list[str] = []
    previous_keys = set(previous)
    current_keys = set(current)

    for key in sorted(previous_keys | current_keys):
        if previous.get(key) != current.get(key):
            changed.append(key)

    if not changed:
        return "change detected"
    if len(changed) <= 5:
        return ", ".join(changed)
    return f"{', '.join(changed[:5])}, ... (+{len(changed) - 5} more)"


def build_docs(repo_root: Path, source_dir: Path, build_dir: Path, state: BuildState) -> bool:
    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        str(source_dir),
        str(build_dir),
    ]

    state.start_build()
    started_at = time.time()
    print(f"[build] {' '.join(cmd)}", flush=True)
    result = subprocess.run(
        cmd,
        cwd=repo_root,
        text=True,
        capture_output=True,
    )
    duration = time.time() - started_at

    output = (result.stdout or "") + (result.stderr or "")
    if output.strip():
        print(output.rstrip(), flush=True)

    if result.returncode == 0:
        state.mark_success()
        print(f"[build] succeeded in {duration:.2f}s", flush=True)
        return True

    state.mark_failure()
    print(f"[build] failed in {duration:.2f}s", flush=True)
    return False


class LivePreviewHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str, state: BuildState, **kwargs):
        self._state = state
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        if parsed.path == RELOAD_ENDPOINT:
            payload = self._state.payload()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        html_path, redirect_target = self._resolve_html_path(parsed.path)
        if redirect_target is not None:
            self.send_response(HTTPStatus.MOVED_PERMANENTLY)
            self.send_header("Location", redirect_target)
            self.end_headers()
            return

        if html_path is not None:
            try:
                html = html_path.read_text(encoding="utf-8")
            except OSError:
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
                return

            body = inject_reload_snippet(html).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        super().do_GET()

    def _resolve_html_path(self, request_path: str) -> tuple[Path | None, str | None]:
        fs_path = Path(self.translate_path(request_path))

        if fs_path.is_dir():
            if not request_path.endswith("/"):
                query = urllib.parse.urlsplit(self.path).query
                target = request_path + "/"
                if query:
                    target += f"?{query}"
                return None, target

            for name in ("index.html", "index.htm"):
                candidate = fs_path / name
                if candidate.is_file():
                    return candidate, None
            return None, None

        if fs_path.is_file() and fs_path.suffix.lower() in HTML_SUFFIXES:
            return fs_path, None

        return None, None


def watch_loop(
    repo_root: Path,
    source_dir: Path,
    build_dir: Path,
    state: BuildState,
    stop_event: threading.Event,
    poll_interval: float,
    debounce_seconds: float,
) -> None:
    previous = snapshot_tree(source_dir)
    pending_since: float | None = None
    pending_summary = ""

    while not stop_event.wait(poll_interval):
        current = snapshot_tree(source_dir)
        if current != previous:
            pending_since = time.time()
            pending_summary = summarize_changes(previous, current)
            previous = current

        if pending_since is None:
            continue

        if time.time() - pending_since < debounce_seconds:
            continue

        print(f"[watch] rebuilding after changes: {pending_summary}", flush=True)
        build_docs(repo_root, source_dir, build_dir, state)
        pending_since = None
        pending_summary = ""


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Live preview for RoSHI docs")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the preview server to")
    parser.add_argument("--port", type=int, default=8000, help="Port for the preview server")
    parser.add_argument("--source", default=str(repo_root / "docs"), help="Sphinx source directory")
    parser.add_argument("--build", default=str(repo_root / "documentation"), help="HTML output directory")
    parser.add_argument("--poll-interval", type=float, default=0.75, help="File polling interval in seconds")
    parser.add_argument("--debounce", type=float, default=0.5, help="Debounce window before rebuild")
    parser.add_argument("--no-open", action="store_true", help="Do not open the browser automatically")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    source_dir = Path(args.source).resolve()
    build_dir = Path(args.build).resolve()

    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}", file=sys.stderr)
        return 1

    build_dir.mkdir(parents=True, exist_ok=True)
    state = BuildState()

    build_docs(repo_root, source_dir, build_dir, state)

    handler = lambda *handler_args, **handler_kwargs: LivePreviewHandler(
        *handler_args,
        directory=str(build_dir),
        state=state,
        **handler_kwargs,
    )
    server = ThreadingHTTPServer((args.host, args.port), handler)

    stop_event = threading.Event()
    watcher = threading.Thread(
        target=watch_loop,
        args=(
            repo_root,
            source_dir,
            build_dir,
            state,
            stop_event,
            args.poll_interval,
            args.debounce,
        ),
        daemon=True,
    )
    watcher.start()

    url = f"http://{args.host}:{args.port}/"
    print(f"[serve] preview available at {url}", flush=True)
    print(f"[watch] watching {source_dir}", flush=True)

    if not args.no_open:
        try:
            webbrowser.open(url, new=2)
        except webbrowser.Error:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[stop] shutting down preview server", flush=True)
    finally:
        stop_event.set()
        server.shutdown()
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
