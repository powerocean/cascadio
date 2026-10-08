"""PyInstaller runtime hook: add cascadio.libs DLL directory to search path.

At runtime, PyInstaller extracts binaries to sys._MEIPASS/. The
delvewheel-patched _core.pyd references hash-named DLLs (e.g.
TKBO-bd10455f....dll) which live in cascadio.libs/. This hook adds
that directory to Windows' DLL search path before cascadio is imported.
"""
import os
import sys

if sys.platform == "win32":
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        # Frozen PyInstaller: binaries extracted to _MEIPASS/
        libs_dir = os.path.join(meipass, "cascadio.libs")
    else:
        # Normal Python: rely on delvewheel's own hook in __init__.py
        libs_dir = None
    if libs_dir and os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)
