@echo off

cls

set PROJECT_NAME=numerology-cli
set VERSION=0.1.0
set ENTRYPOINT_FILE=./src/numerology_cli/entrypoint/__init__.py
set PACKAGE_NAME=%PROJECT_NAME%-%VERSION%.tar
set NUITKA_OUTPUT_DIR=./build
set NUITKA_OPTIONS=--standalone --assume-yes-for-downloads --output-filename=%PROJECT_NAME% --output-dir=%NUITKA_OUTPUT_DIR% %ENTRYPOINT_FILE%


echo Prepare for environment
uv sync --active --no-cache
echo %ERRORLEVEL%
if %ERRORLEVEL% NEQ 0 (
    echo Failed to compile and build
    exit /B %ERRORLEVEL%
)

echo ====================Building====================
echo Step1: compile and build
uv run -- nuitka %NUITKA_OPTIONS%
echo %ERRORLEVEL%
if %ERRORLEVEL% NEQ 0 (
    echo Failed to compile and build
    exit /B %ERRORLEVEL%
)

echo Step2: rename folder
ren build\__init__.dist %PROJECT_NAME%
if %ERRORLEVEL% NEQ 0 (
    echo Failed to rename folder
    exit /B %ERRORLEVEL%
)

echo Step3: verify
%PROJECT_NAME%/n%PROJECT_NAME%.exe --help
if %ERRORLEVEL% NEQ 0 (
    echo %PROJECT_NAME% is not working 1>&2
    exit /B %ERRORLEVEL%
)

echo Step4: package
tar -cvf %PACKAGE_NAME% %PROJECT_NAME%
if %ERRORLEVEL% NEQ 0 (
    echo Failed to package 1>&2
    exit /B %ERRORLEVEL%
)

echo ===========Building successfully done===========