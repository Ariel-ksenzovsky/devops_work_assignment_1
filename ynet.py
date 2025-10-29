#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import urllib.request
import xml.etree.ElementTree as ET

RSS_URL = "https://www.ynet.co.il/Integration/StoryRss2.xml"

def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Python RSS fetcher)"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()

def parse_titles(rss_bytes: bytes):
    # מזהה אוטומטית קידוד (ynet שולח UTF-8)
    root = ET.fromstring(rss_bytes)
    # מבנה RSS סטנדרטי: rss/channel/item
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pubdate = (item.findtext("pubDate") or "").strip()
        yield title, link, pubdate

def main():
    try:
        rss = fetch(RSS_URL)
    except Exception as e:
        print(f"שגיאה בהורדת ה-RSS: {e}", file=sys.stderr)
        sys.exit(1)

    print("כותרות Ynet (RSS):\n")
    for i, (title, link, pubdate) in enumerate(parse_titles(rss), start=1):
        print(f"{i}. {title}")
        if link:
            print(f"   {link}")
        if pubdate:
            print(f"   {pubdate}")
        print()

if __name__ == "__main__":
    main()
