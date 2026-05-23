#!/usr/bin/env python3
"""Download UAP PURSUE Release 02 files from war.gov."""

import time
import zipfile
from pathlib import Path

try:
    from curl_cffi import requests as curl_requests
except ImportError:
    raise SystemExit("Run: pip install curl_cffi")

OUT = Path(__file__).parent
PORTAL = "https://www.war.gov/UFO/"
DOCS_URL = "https://www.war.gov/medialink/ufo/052226/release_02/release_02_document_bundle.zip"
VIDEOS_URL = "https://d34w7g4gy10iej.cloudfront.net/uap052226.zip"

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "Referer": PORTAL,
    "Upgrade-Insecure-Requests": "1",
}


CHUNK_SIZE = 2 * 1024 * 1024  # 2 MB per Range request — stays under Akamai's ~3MB cutoff


def make_session(warm: bool = True) -> curl_requests.Session:
    s = curl_requests.Session()
    if warm:
        try:
            r = s.get(PORTAL, impersonate="chrome", timeout=20)
            print(f"  Session warm-up: HTTP {r.status_code}")
        except Exception as e:
            print(f"  Session warm-up failed (continuing anyway): {e}")
    return s


def get_total_size(url: str, session: curl_requests.Session) -> int:
    """HEAD request to get Content-Length."""
    r = session.request("HEAD", url, impersonate="chrome", timeout=20, headers=BROWSER_HEADERS)
    return int(r.headers.get("content-length", 0))


def download_chunk(url: str, session: curl_requests.Session, start: int, end: int) -> bytes:
    """Download a single byte range, retrying up to 3 times."""
    hdrs = dict(BROWSER_HEADERS)
    hdrs["Range"] = f"bytes={start}-{end}"
    for attempt in range(1, 4):
        try:
            r = session.get(url, impersonate="chrome", timeout=120, headers=hdrs)
            if r.status_code in (200, 206):
                return r.content
            raise RuntimeError(f"HTTP {r.status_code}")
        except Exception as e:
            if attempt == 3:
                raise
            time.sleep(5 * attempt)
    return b""


def download_file(url, dest, label, impersonate=True):
    if dest.exists():
        print(f"  SKIP (exists): {label}")
        return True
    tmp = dest.with_suffix(".part")

    s = make_session(warm=impersonate)
    total = get_total_size(url, s) if impersonate else 0

    # Fall back to plain streaming for CloudFront (no Akamai bot issues there)
    if not impersonate:
        tmp.unlink(missing_ok=True)
        total_cf = 0
        try:
            print(f"  Streaming {label}...", flush=True)
            with s.stream("GET", url, timeout=7200, headers={"Referer": PORTAL}) as r:
                if r.status_code != 200:
                    print(f"  FAIL HTTP {r.status_code}")
                    return False
                total_cf = int(r.headers.get("content-length", 0))
                downloaded = 0
                last_pct = -1
                with tmp.open("wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                        if total_cf and downloaded > 0:
                            pct = int(downloaded / total_cf * 100)
                            if pct % 5 == 0 and pct != last_pct:
                                print(f"    {pct}% ({downloaded//1024//1024} MB)", flush=True)
                                last_pct = pct
            on_disk = tmp.stat().st_size if tmp.exists() else 0
            if not total_cf or on_disk >= total_cf:
                tmp.rename(dest)
                print(f"  OK {on_disk//1024//1024} MB: {label}")
                return True
        except Exception:
            on_disk = tmp.stat().st_size if tmp.exists() else 0
            if total_cf and on_disk >= total_cf:
                tmp.rename(dest)
                print(f"  OK {on_disk//1024//1024} MB (conn closed): {label}")
                return True
        tmp.unlink(missing_ok=True)
        return False

    # Chunked range-request download for Akamai-protected URLs
    if total == 0:
        print(f"  FAIL: could not get file size for {label}")
        return False

    print(f"  Size: {total // 1024 // 1024} MB — downloading in {CHUNK_SIZE // 1024 // 1024}MB chunks", flush=True)
    # Resume support: check how much we already have
    start = tmp.stat().st_size if tmp.exists() else 0
    if start > 0:
        print(f"  Resuming from {start // 1024 // 1024} MB", flush=True)

    last_pct = int(start / total * 100) if total else 0
    try:
        with tmp.open("ab") as f:
            pos = start
            while pos < total:
                end = min(pos + CHUNK_SIZE - 1, total - 1)
                data = download_chunk(url, s, pos, end)
                f.write(data)
                f.flush()
                pos += len(data)
                pct = int(pos / total * 100)
                if pct % 5 == 0 and pct != last_pct:
                    print(f"    {pct}% ({pos//1024//1024} MB)", flush=True)
                    last_pct = pct
                time.sleep(0.3)  # brief pause between chunks to avoid rate-limit
    except Exception as e:
        print(f"  ERROR mid-download: {e} — will resume on next run")
        return False

    on_disk = tmp.stat().st_size
    if on_disk >= total:
        tmp.rename(dest)
        print(f"  OK {on_disk//1024//1024} MB: {label}")
        return True
    print(f"  INCOMPLETE {on_disk//1024//1024}/{total//1024//1024} MB")
    return False


def extract_zip(zip_path, extract_to, label):
    print(f"\nExtracting {label}...")
    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        members = zf.namelist()
        print(f"  {len(members)} files in archive")
        zf.extractall(extract_to)
    print(f"  Extracted to: {extract_to}")


def main():
    print("=== UAP Release 02 Downloader ===\n")

    # Documents zip
    docs_zip = OUT / "release_02_document_bundle.zip"
    print("--- Documents (70.1 MB) ---")
    ok = download_file(DOCS_URL, docs_zip, "Release 02 Documents", impersonate=True)
    if ok:
        extract_zip(docs_zip, OUT / "documents", "documents")

    print()

    # Videos zip
    videos_zip = OUT / "release_02_videos.zip"
    print("--- Videos (5.6 GB) ---")
    ok = download_file(VIDEOS_URL, videos_zip, "Release 02 Videos", impersonate=False)
    if ok:
        extract_zip(videos_zip, OUT / "videos", "videos")

    print("\n=== Done ===")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    main()
