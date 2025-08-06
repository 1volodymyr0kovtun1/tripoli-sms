# etl.py
from tripoli.scrape import fetch_all_crops
from tripoli.clean  import clean_tripoli_df

CROPS = ["yachmen", "kukuruza", "soya",
         "raps", "podsolnechnik", "pshenitsa-2-klass"]

def build_clean_csv(outfile: str = "tripoli_prices_clean.csv") -> str:
    """Парсить сайт, чистить дані й зберігає у CSV. Повертає шлях до файла."""
    raw_df   = fetch_all_crops(CROPS)
    clean_df = clean_tripoli_df(raw_df)
    clean_df.to_csv(outfile, index=False, encoding="utf-8-sig")
    print(f"✅ CSV збережено → {outfile}")
    return outfile          # знадобиться report.py

# Якщо запускати etl.py напряму:
if __name__ == "__main__":
    build_clean_csv()
