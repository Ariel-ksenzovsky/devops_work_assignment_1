#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import urllib.request
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, render_template_string, abort

app = Flask(__name__)

RSS_URL = "https://www.ynet.co.il/Integration/StoryRss2.xml"

def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Python RSS fetcher)"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()

def parse_titles(rss_bytes: bytes):
    root = ET.fromstring(rss_bytes)
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pubdate = (item.findtext("pubDate") or "").strip()
        yield {"title": title, "link": link, "pubDate": pubdate}

PAGE_HTML = """
<!doctype html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>כותרות Ynet (RSS)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, "Noto Sans", "Liberation Sans", sans-serif;
           margin: 2rem; background: #fafafa; color: #111; }
    h1 { margin-bottom: 1rem; }
    .item { background:#fff; border:1px solid #e6e6e6; border-radius:12px; padding:1rem 1.25rem; margin-bottom:0.75rem; }
    .item a { text-decoration: none; color: #0b67c2; }
    .meta { color:#666; font-size:0.9rem; margin-top:0.25rem; }
    .topbar { display:flex; align-items:center; gap:1rem; margin-bottom:1rem; }
    .refresh { font-size:0.9rem; color:#555; }
    .error { color:#b00020; background:#ffe9ec; border:1px solid #ffc1c8; padding:.75rem 1rem; border-radius:10px; }
  </style>
</head>
<body>
  <div class="topbar">
    <h1>כותרות Ynet (RSS)</h1>
    <div class="refresh">🗞️ העמוד נטען ישירות מה-RSS בכל רענון</div>
  </div>

  {% if error %}
    <div class="error">שגיאה בטעינת ה-RSS: {{ error }}</div>
  {% endif %}

  {% for it in items %}
    <div class="item">
      <div><a href="{{ it.link }}" target="_blank" rel="noopener">{{ it.title }}</a></div>
      {% if it.pubDate %}
        <div class="meta">{{ it.pubDate }}</div>
      {% endif %}
    </div>
  {% else %}
    <div>לא נמצאו פריטים.</div>
  {% endfor %}
</body>
</html>
"""

@app.route("/")
def index():
    try:
        rss_bytes = fetch(RSS_URL)
        items = list(parse_titles(rss_bytes))
        return render_template_string(PAGE_HTML, items=items, error=None)
    except Exception as e:
        # Show a friendly page, but keep a non-200 status for monitoring if you prefer
        return render_template_string(PAGE_HTML, items=[], error=str(e)), 502

@app.route("/api/titles")
def api_titles():
    """Simple JSON API endpoint."""
    try:
        rss_bytes = fetch(RSS_URL)
        items = list(parse_titles(rss_bytes))
        return jsonify(items)
    except Exception as e:
        abort(502, description=f"RSS fetch error: {e}")

@app.get("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    # Local dev: python app.py
    # Open http://127.0.0.1:8080
    app.run(host="0.0.0.0", port=8081, debug=True)
