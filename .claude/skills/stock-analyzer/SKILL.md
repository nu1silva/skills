---
name: stock-price
description: >
  Fetch the latest real-time or most recent closing price for any stock, ETF, index, or
  crypto ticker. Use this skill whenever the user asks for the current price, latest price,
  stock quote, share price, or market value of any security — e.g. "what's Apple trading at?",
  "get me the price of TSLA", "how much is NVDA right now?", "look up $MSFT", "what's the
  price of Bitcoin?". Trigger even if the user just pastes a ticker symbol and asks "price?".
  Always use this skill for live price lookups — do NOT rely on training data for prices.
---

# Stock Price Skill

Fetches the latest price for a given ticker using the most reliable available method.

## Step 1 — Identify the ticker

Extract the ticker symbol from the user's message. If ambiguous (e.g. "Apple" vs "AAPL"),
resolve it yourself — common examples:
- Apple → AAPL, Tesla → TSLA, Google / Alphabet → GOOGL, Amazon → AMZN,
  Microsoft → MSFT, Meta → META, Nvidia → NVDA, Bitcoin → BTC-USD, etc.

If genuinely uncertain, ask the user to confirm before fetching.

## Step 2 — Fetch the price

Use **Method A** first. Fall back to **Method B** only if Method A fails or returns no price.

### Method A — Web search (preferred)

Search for: `<TICKER> stock price`

Extract the current price, currency, and any useful context (change %, market status).
If the market is closed, note that the price shown is the most recent close.

### Method B — Python via yfinance (fallback)

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "--break-system-packages", "-q"])

import yfinance as yf
ticker = yf.Ticker("TICKER")  # replace TICKER
info = ticker.fast_info
print(f"Price: {info.last_price}")
print(f"Currency: {info.currency}")
print(f"Previous close: {info.previous_close}")
```

### Method C — Free public API (last resort)

```bash
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/TICKER?interval=1d&range=1d" \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
result = d['chart']['result'][0]
meta = result['meta']
print(f\"Price: {meta.get('regularMarketPrice', meta.get('chartPreviousClose'))}\")
print(f\"Currency: {meta['currency']}\")
"
```

## Step 3 — Present the result

Present the information clearly. Include:
- **Ticker** and company/asset name
- **Current price** with currency
- **Change** (amount and %) since previous close, if available
- **Market status** (open / closed / pre-market / after-hours), if determinable
- **As of** timestamp or date, if available

Keep the response concise — a few lines is ideal unless the user asks for more detail.

### Example output format

> **AAPL – Apple Inc.**
> $213.49 USD (+1.23 / +0.58%) ▲
> Market: Open | As of 3:42 PM ET

---

## Notes

- For crypto tickers on Yahoo Finance, append `-USD` (e.g. `BTC-USD`, `ETH-USD`)
- For non-US stocks, use the exchange suffix (e.g. `ASML.AS` for Amsterdam, `7203.T` for Tokyo)
- If a user asks for multiple tickers, fetch them all and present in a small table