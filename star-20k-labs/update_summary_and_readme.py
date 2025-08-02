# -*- coding: utf-8 -*-
import json
from datetime import datetime
from pathlib import Path

# === CONFIG ===
LABS_TOTAL = 20000
SUMMARY_PATH = Path(__file__).parent / "summary.json"
README_PATH = Path(__file__).parent / "README.md"

# === LOAD SUMMARY ===
try:
    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ summary.json not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"❌ summary.json format error: {e}")
    exit(1)

# === METRICS ===
labs_done = sum(1 for lab in data if lab.get("Lab Complete", "").strip().lower() in ["yes", "true", "1"])
labs_remaining = max(0, LABS_TOTAL - labs_done)

gdb_used = sum(1 for lab in data if lab.get("GDB Used", "").strip().lower() in ["yes", "true", "1"])

anki_count = 0
for lab in data:
    try:
        anki_count += int(lab.get("Anki Cards", 0))
    except ValueError:
        pass

last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# === DASHBOARD CONTENT ===
dashboard = f"""\
# 🧠 Black Lotus Tier 1 — Execution Status

**Labs Completed:** `{labs_done}`  
**Labs Remaining:** `{labs_remaining}`  
**GDB Used:** `{gdb_used}`  
**Anki Cards:** `{anki_count}`  

🕒 **Last Updated:** `{last_updated}` IST

---

### 🔣 Symbol Frequency  
_Coming soon_

### 🧬 Mutation ID Count  
_Coming soon_

### 📚 Topic Breakdown  
_Coming soon_
"""

# === WRITE TO README.md (Windows-safe) ===
try:
    with open(README_PATH, "w", encoding="utf-8", errors="ignore") as f:
        f.write(dashboard)
    print("✅ README.md updated successfully.")
except Exception as e:
    print(f"❌ Failed to write README.md: {e}")
