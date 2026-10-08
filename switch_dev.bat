@echo off
setlocal
REM Switch between dev mode (editable install) and wheel mode
REM 版本号与 pyproject.toml 的 [project].version 保持一致
set VERSION=0.2.0
set WHL=dist\cascadio-%VERSION%-cp312-abi3-win_amd64.whl

if "%1"=="dev" (
    echo === Switch to dev mode (editable install) ===
    uv pip install -e .
) else if "%1"=="wheel" (
    echo === Switch to wheel mode ===
    uv pip install %WHL% --force-reinstall
) else (
    echo Usage: switch_dev.bat dev ^| wheel
)
