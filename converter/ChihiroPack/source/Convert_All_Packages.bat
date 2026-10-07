@echo off
setlocal DisableDelayedExpansion
cd /d "%~dp0"
if not exist "%~dp0input" mkdir "%~dp0input"
if not exist "%~dp0output" mkdir "%~dp0output"
echo ChihiroPack - batch conversion
echo Put game folders, ZIPs and 7z packages in the input folder.
echo BINs and verification reports will be written to output.
echo Existing output files will be kept.
echo.
echo Converting... see batch-conversion.log for progress.
"%~dp0ChihiroPack.exe" create "%~dp0input" --batch --output-dir "%~dp0output" > "%~dp0batch-conversion.log" 2>&1
set "pack_result=%errorlevel%"
type "%~dp0batch-conversion.log"
echo.
if "%pack_result%"=="0" (echo Finished successfully.) else (echo One or more packages failed. Check the log above.)
pause
exit /b %pack_result%
