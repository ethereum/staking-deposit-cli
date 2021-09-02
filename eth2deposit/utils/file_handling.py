import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource in a manner friendly to PyInstaller.
    PyInstaller creates a temp folder and stores path in _MEIPASS which this function swaps
    into a resource path so it is available both when building binaries and running natively.
    """
    try:
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
