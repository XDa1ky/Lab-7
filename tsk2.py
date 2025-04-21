from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys
from textwrap import fill

import requests

API_KEY = "627a95e3-60c4-45ee-b02a-8aeff8eb5da3"
URL = (
    "https://www.dictionaryapi.com/api/v3/references/collegiate/"
    "json/{word}?key={key}"
)


def fetch(word: str) -> list | dict:
    resp = requests.get(URL.format(word=word, key=API_KEY), timeout=10)
    resp.raise_for_status()
    return resp.json()


def extract(entry: dict | None, word: str) -> dict:
    if not entry or not isinstance(entry, dict):
        return {
            "word": word,
            "part_of_speech": "—",
            "pronunciation": "—",
            "definition_1": "—",
            "definition_2": "—",
            "total_definitions": 0,
        }

    meta = entry["meta"]
    hwi = entry.get("hwi", {})
    defs = entry.get("shortdef", [])

    return {
        "word": meta["id"].split(":")[0],
        "part_of_speech": entry.get("fl", "—"),
        "pronunciation": hwi.get("prs", [{}])[0].get("mw", "—"),
        "definition_1": defs[0] if defs else "—",
        "definition_2": defs[1] if len(defs) > 1 else "—",
        "total_definitions": len(defs),
    }


def save_json(data: dict, word: str) -> pathlib.Path:
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = pathlib.Path(f"{word}_info_{stamp}.json")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    return path.resolve()


def pretty(block: dict) -> None:
    print("\n" + "=" * 44)
    for k, v in block.items():
        print(f"{k:<18}: {fill(str(v), width=60)}")
    print("=" * 44 + "\n")


def main() -> None:
    print("Введите слово, ENTER — выйти)")
    while True:
        word = input("Введите слово: ").strip()
        if word.lower() in {"", "exit", "quit"}:
            sys.exit()

        try:
            raw = fetch(word)
            entry = raw[0] if raw and isinstance(raw[0], dict) else None
            info = extract(entry, word)
            file_path = save_json(info, word)
            print(f"Saved: {file_path}")
            pretty(info)
        except requests.exceptions.HTTPError as err:
            print("Error:", err, "\n")
        except requests.exceptions.RequestException as err:
            print("Site Error", err, "\n")


if __name__ == "__main__":
    main()
