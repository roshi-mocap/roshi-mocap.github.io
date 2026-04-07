@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment in docs\.venv ...
  py -3 -m venv .venv
  if errorlevel 1 python -m venv .venv
)
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
".venv\Scripts\python.exe" -m sphinx -b html . _build/html
if errorlevel 1 exit /b 1
echo.
echo Built: %cd%\_build\html\index.html
echo Open that file in a browser, or run:  preview-docs.cmd
endlocal
