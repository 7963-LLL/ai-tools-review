#!/usr/bin/env python3
"""Find images from a URL for the daily update."""
import sys, re, subprocess, json

url = sys.argv[1]
outfile = sys.argv[2] if len(sys.argv) > 2 else None

# curl with proxy
cmd = [
    "curl", "-sL", "-A", "Mozilla/5.0", url,
    "-x", "socks5://127.0.0.1:7897",
    "--proxy-user", "set-your-secret:",
    "--ssl-no-revoke"
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
html = result.stdout

# Find og:image
og = re.search(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"', html)
if og:
    print(f"og:image: {og.group(1)}")

# Find img tags
imgs = re.findall(r'<img[^>]+src="([^"]+\.(?:jpg|jpeg|png|webp))"', html)
seen = set()
for i, s in enumerate(imgs):
    sl = s.lower()
    if any(x in sl for x in ['icon','avatar','logo','favicon','pixel','analytics','button','badge','spacer']):
        continue
    if s not in seen:
        seen.add(s)
        print(f"img{i+1}: {s}")

# Try picture/source tags
srcset_imgs = re.findall(r'<source[^>]+srcset="([^"]+)"', html)
for s in srcset_imgs:
    urls = re.findall(r'(https?://[^\s,]+\.(?:jpg|jpeg|png|webp))', s)
    for u in urls:
        if u not in seen:
            seen.add(u)
            print(f"srcset: {u}")
