@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment in docs\.venv ...
  py -3 -m venv .venv
  if errorlevel 1 python -m venv .venv
)
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
REM -a -E: rebuild all HTML from a fresh env (avoids stale pages when editing .rst)
".venv\Scripts\python.exe" -m sphinx -a -E -b html . _build/html
if errorlevel 1 exit /b 1
echo.
echo Built: %cd%\_build\html\index.html
echo Receiver BOM:  hardware\components.html#receiver-host-unit-bom
echo Preview:       run preview-docs.cmd  then open the URL above
endlocal
