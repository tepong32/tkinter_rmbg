import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import shutil
import sys
import time

import requests


URL = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
EXPECTED_MD5 = "60024c5c889badc19c04ad937298a77b"
EXPECTED_SIZE = 175_997_641
CHUNK_SIZE = 1024 * 1024
WORKERS = 12
DESTINATION = Path(__file__).resolve().parent.parent / "models" / "u2net" / "u2net.onnx"
TEMPORARY = DESTINATION.with_suffix(".onnx.download")
CHUNK_DIRECTORY = DESTINATION.parent / ".u2net-download-chunks"


def download_chunk(index, start, end):
    chunk_path = CHUNK_DIRECTORY / f"chunk-{index:04d}"
    headers = {"Range": f"bytes={start}-{end}"}
    last_error = None
    for attempt in range(5):
        try:
            with requests.get(URL, headers=headers, stream=True, timeout=(30, 180)) as response:
                if response.status_code != 206:
                    raise IOError(f"Range request returned HTTP {response.status_code}")
                expected_range = f"bytes {start}-{end}/{EXPECTED_SIZE}"
                if response.headers.get("Content-Range") != expected_range:
                    raise IOError("Model server returned an unexpected byte range")
                with chunk_path.open("wb") as output:
                    for data in response.iter_content(chunk_size=64 * 1024):
                        if data:
                            output.write(data)
            expected_length = end - start + 1
            if chunk_path.stat().st_size != expected_length:
                raise IOError(f"Downloaded chunk {index} has an incorrect size")
            return chunk_path
        except Exception as error:
            last_error = error
            chunk_path.unlink(missing_ok=True)
            time.sleep(2 ** attempt)
    raise IOError(f"Unable to download model chunk {index}: {last_error}")


def main():
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    CHUNK_DIRECTORY.mkdir(exist_ok=True)
    ranges = [
        (index, start, min(start + CHUNK_SIZE - 1, EXPECTED_SIZE - 1))
        for index, start in enumerate(range(0, EXPECTED_SIZE, CHUNK_SIZE))
    ]
    try:
        completed = 0
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = [pool.submit(download_chunk, *item) for item in ranges]
            for future in as_completed(futures):
                future.result()
                completed += 1
                print(f"\rDownloaded {completed} / {len(ranges)} chunks", end="", flush=True)
        print()

        digest = hashlib.md5()
        with TEMPORARY.open("wb") as output:
            for index, _, _ in ranges:
                chunk_path = CHUNK_DIRECTORY / f"chunk-{index:04d}"
                with chunk_path.open("rb") as chunk_file:
                    while data := chunk_file.read(1024 * 1024):
                        output.write(data)
                        digest.update(data)
        if TEMPORARY.stat().st_size != EXPECTED_SIZE:
            raise ValueError("Downloaded model has an unexpected size")
        if digest.hexdigest() != EXPECTED_MD5:
            raise ValueError(f"MD5 mismatch: {digest.hexdigest()}")
        TEMPORARY.replace(DESTINATION)
        print(f"Verified model saved to {DESTINATION}")
    except Exception:
        TEMPORARY.unlink(missing_ok=True)
        raise
    finally:
        shutil.rmtree(CHUNK_DIRECTORY, ignore_errors=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Model download failed: {error}", file=sys.stderr)
        raise SystemExit(1)
