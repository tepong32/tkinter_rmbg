from importlib.metadata import distributions
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parent.parent
LICENSES = ROOT / "LICENSES"
LICENSES.mkdir(exist_ok=True)
locked_names = {
    line.split("==", 1)[0].strip().lower().replace("_", "-").replace(".", "-")
    for line in (ROOT / "requirements-lock-py313-win.txt").read_text(encoding="utf-8").splitlines()
    if "==" in line
}
# PyInstaller is build-only, but its compiled bootloader is shipped in the app.
locked_names.add("pyinstaller")
entries = []

for dist in sorted(distributions(), key=lambda item: (item.metadata.get("Name") or "").lower()):
    name = dist.metadata.get("Name")
    if not name:
        continue
    normalized_name = name.lower().replace("_", "-").replace(".", "-")
    if normalized_name not in locked_names:
        continue
    version = dist.version
    license_name = dist.metadata.get("License-Expression") or dist.metadata.get("License")
    if not license_name:
        license_name = next(
            (value.split("::", 1)[1].strip() for value in dist.metadata.get_all("Classifier", [])
             if value.startswith("License ::")),
            "See bundled license file or package metadata",
        )

    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
    package_dir = LICENSES / f"{safe_name}-{version}"
    copied = []
    for file in dist.files or ():
        filename = Path(str(file)).name
        lower = filename.lower()
        if any(token in lower for token in ("license", "copying", "notice", "patent")):
            source = Path(dist.locate_file(file))
            if source.is_file():
                relative = Path(*(
                    part for part in Path(str(file)).parts if part not in (".", "..")
                ))
                destination = package_dir / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
                copied.append(destination.relative_to(ROOT).as_posix())
    files = ", ".join(f"`{path}`" for path in copied) or "No separate license text was present in the installed distribution."
    entries.append(f"- **{name} {version}** — {license_name}. {files}")

body = "\n".join([
    "# Third-party notices",
    "",
    "This application includes the runtime packages listed below. Their license texts are copied into `LICENSES/` from the installed distributions used to produce `requirements-lock-py313-win.txt`. PyInstaller is also listed because its compiled bootloader is included in the Windows executable.",
    "",
    *entries,
    "",
    "## U-2-Net model",
    "",
    "The application explicitly uses rembg's `u2net` ONNX model. The 176.3 MB model file is included in the offline Windows CPU package at `models/u2net/u2net.onnx` and copied into the user's writable model cache on first run. The upstream U-2-Net repository distributes the project under Apache-2.0; a copy of its license is included at `LICENSES/U-2-Net/LICENSE`. This notice applies independently of the rembg package license.",
    "Source: <https://github.com/xuebinqin/U-2-Net>",
    "",
    "The rembg package and the model weights are separate works with separate licensing. Review the upstream notices before redistributing modified or alternative models.",
    "",
])
(ROOT / "THIRD_PARTY_NOTICES.md").write_text(body, encoding="utf-8")
