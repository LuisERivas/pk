"""
TCGplayer product price scraper using Playwright.
Loads product URLs, waits for JS, and extracts price (and optional product name).
"""

import re
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


# Selectors to try for price (in order). Update these after inspecting the live page.
# TCGplayer often shows "From $X.XX" or similar; adjust if the site structure changes.
PRICE_SELECTORS = [
    '[data-testid="price"]',
    '.product-details__price',
    '[class*="price"]',
    'span:has-text("From")',  # "From $X.XX"
]

# Optional: selector for product title.
TITLE_SELECTOR = "h1"


def get_price_for_url(page, url: str, timeout: int = 15000) -> dict:
    """
    Open a TCGplayer product URL and extract price (and optionally title).
    Returns dict with keys: url, title (or None), price (float or None), raw_price (str or None), error (str or None).
    """
    result = {"url": url, "title": None, "price": None, "raw_price": None, "error": None}
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        page.wait_for_load_state("networkidle", timeout=timeout)

        # Try to get product title.
        try:
            el = page.query_selector(TITLE_SELECTOR)
            if el:
                result["title"] = el.inner_text().strip()
        except Exception:
            pass

        # Try each price selector until one works.
        raw_price = None
        for selector in PRICE_SELECTORS:
            try:
                el = page.query_selector(selector)
                if el:
                    raw_price = el.inner_text().strip()
                    if raw_price and re.search(r"\d+\.?\d*", raw_price):
                        break
            except Exception:
                continue

        if not raw_price:
            # Fallback: find any element that looks like a price ($X.XX).
            try:
                text = page.inner_text("body")
                match = re.search(r"\$(\d+\.?\d*)", text)
                if match:
                    raw_price = f"${match.group(1)}"
            except Exception:
                pass

        result["raw_price"] = raw_price
        if raw_price:
            num_match = re.search(r"(\d+\.?\d*)", raw_price.replace(",", ""))
            if num_match:
                result["price"] = float(num_match.group(1))
    except PlaywrightTimeout:
        result["error"] = "Timeout loading page"
    except Exception as e:
        result["error"] = str(e)

    return result


def scrape_urls(urls: list[str], request_delay: float = 3.0, headless: bool = True) -> list[dict]:
    """
    Scrape a list of TCGplayer product URLs and return a list of result dicts.
    """
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        try:
            for i, url in enumerate(urls):
                if i > 0:
                    time.sleep(request_delay)
                results.append(get_price_for_url(page, url))
        finally:
            browser.close()
    return results
