import hashlib
import os
import shutil
from pathlib import Path

from platformdirs import user_data_path

from app_metadata import APP_NAME, resource_path


MODEL_NAME = "u2net"
MODEL_FILENAME = "u2net.onnx"
MODEL_MD5 = "60024c5c889badc19c04ad937298a77b"
REMBG_URL = (
    "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
)


def _md5(path):
    digest = hashlib.md5()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_model():
    """Seed rembg's writable model cache from the bundled, verified model."""
    data_root = os.environ.get("REMBG_STUDIO_DATA_DIR")
    if data_root:
        home = Path(data_root) / "rembg"
    else:
        home = user_data_path(APP_NAME, appauthor=APP_NAME) / "rembg"
    home.mkdir(parents=True, exist_ok=True)
    os.environ.pop("U2NET_HOME", None)
    os.environ["REMBG_HOME"] = str(home)

    model_path = home / "models" / MODEL_NAME / MODEL_FILENAME
    if model_path.is_file() and _md5(model_path) == MODEL_MD5:
        return model_path

    bundled_model = resource_path("models", MODEL_NAME, MODEL_FILENAME)
    if not bundled_model.is_file():
        raise FileNotFoundError(
            "The bundled U-2-Net model is missing. Reinstall the complete package."
        )
    if _md5(bundled_model) != MODEL_MD5:
        raise ValueError("The bundled U-2-Net model failed its integrity check.")

    model_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = model_path.with_name(f"{MODEL_FILENAME}.tmp")
    shutil.copyfile(bundled_model, temporary_path)
    if _md5(temporary_path) != MODEL_MD5:
        temporary_path.unlink(missing_ok=True)
        raise OSError("The U-2-Net model could not be copied correctly.")
    os.replace(temporary_path, model_path)
    return model_path
