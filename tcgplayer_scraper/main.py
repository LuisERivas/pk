"""
Run the TCGplayer price scraper for URLs defined in config.
"""

from config import PRODUCT_URLS, REQUEST_DELAY
from scraper import scrape_urls


def main():
    if not PRODUCT_URLS:
        print("Add product URLs to config.PRODUCT_URLS in config.py")
        return

    print(f"Scraping {len(PRODUCT_URLS)} product(s)...\n")
    results = scrape_urls(PRODUCT_URLS, request_delay=REQUEST_DELAY, headless=True)

    for r in results:
        if r["error"]:
            print(f"  ERROR: {r['url']}\n    {r['error']}")
        else:
            title = r["title"] or "(no title)"
            price = r["raw_price"] or r["price"] or "—"
            print(f"  {title}")
            print(f"    Price: {price}")
            print(f"    URL:   {r['url']}\n")

    print("Done.")


if __name__ == "__main__":
    main()
