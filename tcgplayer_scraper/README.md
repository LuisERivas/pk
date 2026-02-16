# TCGplayer price scraper (Python + Playwright)

Scrapes product prices from TCGplayer using product URLs. Uses Playwright so JavaScript-rendered content (prices) is available.

## Setup

1. Create a virtual environment (recommended):
   ```bash
   cd tcgplayer_scraper
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers (one-time):
   ```bash
   playwright install chromium
   ```

## Config

Edit `config.py` and add your TCGplayer product URLs to `PRODUCT_URLS`:

```python
PRODUCT_URLS = [
    "https://www.tcgplayer.com/product/565604/Pokemon-SV08-Surging-Sparks-Surging-Sparks-Booster-Pack",
    # add more...
]
```

Adjust `REQUEST_DELAY` (seconds between requests) if you want to be gentler on the site.

## Run

```bash
python main.py
```

Output is printed to the console (product title and price per URL).

## If prices don't show up

TCGplayer's HTML can change. If the scraper doesn't find a price:

1. Open a product URL in your browser.
2. Right-click the price → **Inspect** and note the element's class or `data-testid`.
3. In `scraper.py`, add that selector to the `PRICE_SELECTORS` list at the top (or put it first in the list).

## Optional next steps

- Write results to CSV or JSON.
- Add a scheduler (e.g. `schedule` or cron) to run periodically.
- Add alerts when price drops below a threshold.
