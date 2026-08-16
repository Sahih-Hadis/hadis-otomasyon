"""
CSV listesinden sıradaki hadisi okur, HTML şablonuna yerleştirir,
1080x1350 boyutunda bir PNG görsel üretir ve docs/latest.png olarak kaydeder.
Sıradaki index bilgisini state.json içinde tutar, liste bitince başa döner.
"""
import csv
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "hadisler.csv"
TEMPLATE_PATH = BASE_DIR / "templates" / "hadis_template.html"
STATE_PATH = BASE_DIR / "state.json"
OUTPUT_DIR = BASE_DIR / "docs"
OUTPUT_IMAGE = OUTPUT_DIR / "latest.png"
OUTPUT_CAPTION = OUTPUT_DIR / "latest_caption.txt"


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"last_index": -1}


def save_state(state):
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def load_hadisler():
    with open(CSV_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_caption(row):
    lines = [
        row["meal"],
        "",
        f"— {row['ravi']}" if row.get("ravi") else "",
        row["kaynak"],
        "",
        "#hadis #sünnet #islam #dua #hadisişerif",
    ]
    return "\n".join(line for line in lines if line != "")


def main():
    hadisler = load_hadisler()
    if not hadisler:
        raise SystemExit("hadisler.csv boş görünüyor.")

    state = load_state()
    next_index = (state["last_index"] + 1) % len(hadisler)
    row = hadisler[next_index]

    template_html = TEMPLATE_PATH.read_text(encoding="utf-8")
    filled_html = (
        template_html
        .replace("{{ARAPCA}}", row["arapca"])
        .replace("{{MEAL}}", row["meal"])
        .replace("{{RAVI}}", row.get("ravi", ""))
        .replace("{{KAYNAK}}", row["kaynak"])
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    temp_html_path = BASE_DIR / "_render.html"
    temp_html_path.write_text(filled_html, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        page.goto(f"file://{temp_html_path}")
        page.screenshot(path=str(OUTPUT_IMAGE))
        browser.close()

    temp_html_path.unlink()

    OUTPUT_CAPTION.write_text(build_caption(row), encoding="utf-8")

    state["last_index"] = next_index
    save_state(state)

    print(f"Üretildi: sıra {next_index} -> {row['kaynak']}")


if __name__ == "__main__":
    main()
