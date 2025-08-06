# scrape.py
import re, requests, pandas as pd
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

def get_tripoli_prices(crop: str, currency: str = "dollar", cc: int = 1) -> pd.DataFrame:
    url = f"https://tripoli.land/ua/{crop}?c={currency}&cc={cc}"
    html = requests.get(url, headers=HEADERS, timeout=15).text
    soup = BeautifulSoup(html, "lxml")

    records = []
    for a in soup.select('a[rel="nofollow"][href^="/ua/companies/"]'):
        m = re.match(r"(\d+(?:[.,]\d+)?)\s*[$USDгрн]+\s*(.*)", a.get_text(strip=True))
        if not m:
            continue
        price = float(m.group(1).replace(",", "."))
        note  = m.group(2).strip()
        port_a = a.find_previous("a")
        port   = port_a.get_text(" ", strip=True) if port_a else None
        records.append(
            {"crop": crop, "port": port, "price": price,
             "currency": "$" if currency == "dollar" else "₴", "note": note}
        )
    return pd.DataFrame(records)

def fetch_all_crops(crops: list[str]) -> pd.DataFrame:
    dfs = [
        get_tripoli_prices(crop, cc=5 if crop == "yachmen" else 1)
        for crop in crops
    ]
    return pd.concat(dfs, ignore_index=True)
