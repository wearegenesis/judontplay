from __future__ import annotations

import re
import unicodedata


KNOWN_UPPERCASE_SURNAME = re.compile(r"^[A-Z' -]+ [A-Z' -]+$")


def normalize_name(name: str) -> str:
    txt = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    txt = re.sub(r"\s+", " ", txt).strip()
    if KNOWN_UPPERCASE_SURNAME.match(txt):
        parts = txt.title().split(" ")
        return f"{' '.join(parts[1:])} {parts[0]}" if len(parts) >= 2 else txt.title()
    return txt.title()


def normalize_weight(weight: str) -> str:
    txt = weight.lower().replace("kg", "").replace("+", " +").strip()
    txt = re.sub(r"\s+", "", txt)
    if txt.startswith("-"):
        num = txt[1:]
        return f"-{num} kg"
    if txt.startswith("+"):
        num = txt[1:]
        return f"+{num} kg"
    return f"-{txt} kg"
