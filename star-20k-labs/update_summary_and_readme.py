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

labs_done = sum(1 for lab in data if lab.get("Lab Complete", "").strip().lower() in ["yes", "true", "1"])
labs_remaining = LABS_TOTAL - labs_done
gdb_used = sum(1 for lab in data if lab.get("GDB Used", "").strip().lower() in ["yes", "true", "1"])
anki_count = sum(int(lab.get("Anki Cards", 0)) for lab in data if lab.get("Anki Cards"))

last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# === DASHBOARD MARKDOWN ===
dashboard = f"""\
# ⚔️ Black Lotus Mutation Dashboard v3

**Labs Completed**: `{labs_done}`  
**Labs Remaining**: `{labs_remaining}`  
**GDB Used**: `{gdb_used}`  
**Anki Cards**: `{anki_count}`  

🕒 **Last Updated:** `{last_updated}` IST

---

### 🔣 Symbol Frequency  
_→ Coming soon_

### 🧬 Mutation ID Count  
_→ Coming soon_

### 📚 Topic Breakdown  
_→ Coming soon_
"""

# === WRITE TO README ===
with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(dashboard)

print("✅ README.md updated successfully.")
