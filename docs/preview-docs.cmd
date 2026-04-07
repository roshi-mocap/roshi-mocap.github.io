@echo off
cd /d "%~dp0"
if not exist "_build\html\index.html" (
  echo Run build-html.cmd first.
  exit /b 1
)
echo Serving http://127.0.0.1:8765/  (Ctrl+C to stop)
".venv\Scripts\python.exe" -m http.server 8765 --directory _build/html
