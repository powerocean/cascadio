@echo off
setlocal
REM Build stp2glb standalone exe
REM 版本号与 pyproject.toml 的 [project].version 保持一致
set VERSION=0.2.0
set WHL=dist\cascadio-%VERSION%-cp312-abi3-win_amd64.whl

REM 1. Build wheel with latest code
echo === Step 1: Build wheel ===
uv build --wheel
if %errorlevel% neq 0 exit /b %errorlevel%

REM 2. Patch wheel with OCCT DLLs
echo === Step 2: delvewheel repair ===
delvewheel repair --add-path occt_cache\win64\vc14\bin -w dist %WHL%
if %errorlevel% neq 0 exit /b %errorlevel%

REM 3. Install patched wheel (replaces editable install)
echo === Step 3: Install patched wheel ===
uv pip install %WHL% --force-reinstall
if %errorlevel% neq 0 exit /b %errorlevel%

REM 4. Build single-file exe
echo === Step 4: PyInstaller ===
pyinstaller stp2glb.spec --noconfirm --clean
if %errorlevel% neq 0 exit /b %errorlevel%

echo === Done! ===
echo Result: dist\stp2glb.exe
