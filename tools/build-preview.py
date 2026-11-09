"""Build the review copy at /preview/ from the v2 pages.

Run from the repo root on the v2 branch:  python tools/build-preview.py <out-dir>
Copies index/checkin/dashboard into <out-dir>, marking them noindex, dropping the analytics beacon (so reviews
aren't counted as visits) and giving browser storage its own prefix (so preview drafts and tokens never reach
the live pages). The pages pick the preview API themselves from the /preview/ path.
"""
import os, re, sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for name in ("index.html", "checkin.html", "dashboard.html"):
    s = open(name, encoding="utf-8").read()
    if 'name="robots"' not in s:
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
    s = re.sub(r"<!-- Cloudflare Web Analytics -->.*?<!-- End Cloudflare Web Analytics -->\n?", "", s, flags=re.S)
    s = s.replace('"grotto_', '"grotto_preview_')
    s = re.sub(r"<title>", "<title>[Preview] ", s, count=1)
    open(os.path.join(out, name), "w", encoding="utf-8", newline="").write(s)
    print("built", os.path.join(out, name))
