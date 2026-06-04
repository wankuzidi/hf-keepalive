"""
Hugging Face Spaces Keepalive Script
Periodically sends GET requests to HF Spaces to prevent sleep due to inactivity.
"""

import os
import sys
import time
import urllib.request
import urllib.error

def ping_space(url: str, token: str | None = None) -> bool:
    """Send a GET request to a HF Space URL. Returns True on success."""
    url = url.strip().rstrip("/")
    if not url:
        return False

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "HF-Keepalive/1.0")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            print(f"  [OK] {url} -> HTTP {status}")
            return True
    except urllib.error.HTTPError as e:
        # 4xx/5xx are still "alive" responses — the space responded
        print(f"  [OK] {url} -> HTTP {e.code} (space is running)")
        return True
    except Exception as e:
        print(f"  [FAIL] {url} -> {e}")
        return False


def main():
    token = os.environ.get("HF_TOKEN", "")
    spaces_env = os.environ.get("SPACES", "")

    # Fallback: read from spaces.txt if env var is empty
    if not spaces_env:
        txt = os.path.join(os.path.dirname(__file__), "spaces.txt")
        if os.path.exists(txt):
            with open(txt) as f:
                spaces_env = f.read()

    spaces = [s.strip() for s in spaces_env.replace("\n", ",").split(",") if s.strip()]

    if not spaces:
        print("No HF Spaces configured. Add URLs to the HF_SPACES variable or spaces.txt.")
        sys.exit(0)

    print(f"Pinging {len(spaces)} space(s)...")
    failed = 0
    for url in spaces:
        if not ping_space(url, token or None):
            failed += 1
        time.sleep(1)   # be polite

    print(f"\nDone. {len(spaces) - failed}/{len(spaces)} succeeded.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
