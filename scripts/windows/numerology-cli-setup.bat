@echo off

cls

set PROJECT_NAME=numerology-cli
set VERSION=0.1.0
set ENTRYPOINT_FILE_NAME=__init__
set ENTRYPOINT_FILE=numerology_cli\src\numerology_cli\entrypoint\%ENTRYPOINT_FILE_NAME%.py
set PACKAGE_NAME=%PROJECT_NAME%-%VERSION%.tar
set NUITKA_OUTPUT_DIR=dist
set NUITKA_OPTIONS=--standalone --assume-yes-for-downloads --nofollow-import-to=pydantic.v1.* --output-filename=%PROJECT_NAME% --output-dir=%NUITKA_OUTPUT_DIR% %ENTRYPOINT_FILE%


echo Check output dir...
if exist %NUITKA_OUTPUT_DIR% (
    rd /S /Q %NUITKA_OUTPUT_DIR%
    echo Clean origin output dir
)

echo ====================Building====================
echo Step1: compile and build...
uv run -- nuitka %NUITKA_OPTIONS%
if %ERRORLEVEL% NEQ 0 (
    echo Failed to compile and build
    exit /B %ERRORLEVEL%
)

echo Step2: rename folder...
ren %NUITKA_OUTPUT_DIR%\%ENTRYPOINT_FILE_NAME%.dist %PROJECT_NAME%
if %ERRORLEVEL% NEQ 0 (
    echo Failed to rename folder
    exit /B %ERRORLEVEL%
)

echo Step3: verify...
%NUITKA_OUTPUT_DIR%\%PROJECT_NAME%\%PROJECT_NAME%.exe --help
%NUITKA_OUTPUT_DIR%\%PROJECT_NAME%\%PROJECT_NAME%.exe -v
if %ERRORLEVEL% NEQ 0 (
    echo %PROJECT_NAME% is not working 1>&2
    exit /B %ERRORLEVEL%
)

echo ===========Building successfully done===========