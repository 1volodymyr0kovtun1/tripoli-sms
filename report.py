# report.py
from pathlib import Path
import os, textwrap

import pandas as pd
from dotenv import load_dotenv
from twilio.rest import Client

from etl import build_clean_csv  # ← твій модуль ETL

# ---------------------------------------------------------------------
EMOJI = {
    "yachmen": "🌾", "kukuruza": "🌽", "soya": "🫘",
    "raps": "🌼", "podsolnechnik": "🌻", "pshenitsa-2-klass": "🌾",
}

NBSP = "\u202F"  # narrow no-break space


# ---------------------------------------------------------------------
def generate_summary(csv_path: str,
                     outfile: str = "price_summary.txt") -> str:
    df = pd.read_csv(csv_path)

    stats = (df.groupby("crop")["price"]
             .agg(["mean", "min", "max"])
             .round(2)
             .reset_index())

    blocks = []
    for _, row in stats.iterrows():
        crop = row["crop"]
        emoji = EMOJI.get(crop, "🌱")
        avg = f"{row['mean']:.2f}{NBSP}$"
        rng = f"{row['min']:.2f}{NBSP}–{NBSP}{row['max']:.2f}{NBSP}$"

        blocks.append(
            f"{emoji} {crop}\n"
            f"   ▸ середня: {avg}\n"
            f"   ▸ розбіг : {rng}"
        )

    text = "\n\n".join(blocks)  # порожній рядок між культурами
    Path(outfile).write_text(text, encoding="utf-8")
    print(f"✅ Звіт збережено → {outfile}")
    return outfile

# ---------------------------------------------------------------------


def send_sms(file_path: str) -> None:
    """Надсилає вміст файла SMS-повідомленнями через Twilio."""
    load_dotenv()  # читаємо .env у корені проєкту
    sid = os.getenv("TWILIO_SID")
    token = os.getenv("TWILIO_TOKEN")
    from_ = os.getenv("TWILIO_FROM")
    to = os.getenv("TWILIO_TO")

    if not all([sid, token, from_, to]):
        raise RuntimeError("❌ Перевір .env — не всі змінні заповнені")

    client = Client(sid, token)
    text = Path(file_path).read_text(encoding="utf-8")

    # Twilio приймає до ~1600 символів; дробимо на шматки по 1500.
    for chunk in textwrap.wrap(text, width=1500):
        msg = client.messages.create(body=chunk, from_=from_, to=to)
        print(f"📨 SMS надіслано (SID={msg.sid})")


# ---------------------------------------------------------------------
if __name__ == "__main__":
    csv_file = build_clean_csv()  # 1️⃣ ETL
    summary_path = generate_summary(csv_file)  # 2️⃣ звіт
    send_sms(summary_path)  # 3️⃣ SMS
