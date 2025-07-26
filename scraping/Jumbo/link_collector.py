import requests
import re
import time
import os
import yaml
import csv
from requests.exceptions import ReadTimeout

CONFIG_PATH = "config/extended_categories.yml"
BUCKET_NAME = "foodv-scraper-module"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "nl-NL,nl;q=0.5",
    "Connection": "keep-alive"
}
REGEX = r'<a href="/producten/[^"]+'

def safe_get(url, tries=3, wait=5):
    for _ in range(tries):
        try:
            return requests.get(url, headers=HEADERS, timeout=30)
        except ReadTimeout:
            time.sleep(wait)
    return None


def collect_links(cat_name, cat_url):
    all_links = set()
    offset = 0
    max_offset = 2400

    while offset < max_offset:
        url = f"{cat_url}?offSet={offset}"
        resp = safe_get(url)
        print(f"🔎 Fetching {url}")

        if resp.status_code != 200:
            print(f"HTTP {resp.status_code}. Stopping {cat_name}")
            break

        html = resp.text
        matches = re.findall(REGEX, html)
        new_links = set()
        for link in matches:
            link.strip('"')
            full_link = "https://www.jumbo.com" + link.replace('<a href="', '')
            if not full_link.endswith("/"):
                new_links.add(full_link)

        if not new_links.difference(all_links):
            print(f"✅No new links found at offset={offset}. Stopping the search for {url}")
            break

        all_links |= new_links
        offset += 24
        time.sleep(3)

    csv_name = f"product_links/links_{cat_name}.csv"
    with open(csv_name, mode="w", encoding='utf-8', newline="") as f:
        writer = csv.writer(f)
        for link in sorted(all_links):
            writer.writerow([link])


def main():
    with open(CONFIG_PATH, "r", encoding='utf-8') as f:
        data = yaml.safe_load(f)

    categories = data.get("categories", [])
    for cat in categories:
        name = cat['name']
        url = cat['url']
        collect_links(name, url)


if __name__ == "__main__":
    main()

