import sys
from pathlib import Path


APP_NAME = "Rembg Studio"
APP_VERSION = "1.0.0"
APP_COPYRIGHT = "Copyright (c) 2026 Rembg Studio contributors"


def resource_path(*parts):
    """Return a path to a bundled asset or a source-tree asset."""
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return root.joinpath(*parts)
