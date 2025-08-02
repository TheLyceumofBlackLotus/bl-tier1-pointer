# ==== begin paste ==================================================
#!/usr/bin/env python3
import pandas as pd, json, os, math, datetime as dt

# === CONFIG ===
EXCEL   = "symbol_star_dashboard.xlsm"
SHEET   = "lab_tracker"
TARGET  = 20_000
OUT     = "docs/summary.json"
DATEFMT = "%Y-%m-%d"
# ==============

df = pd.read_excel(EXCEL, sheet_name=SHEET)
df = df[pd.notna(df["Lab ID"])]               # keep real rows
done = df[df["Lab Complete"].astype(str).str.lower()=="yes"]

completed = len(done)
pending   = max(TARGET - completed, 0)
eff_pct   = round(completed * 100 / TARGET, 2)

# ── Optional extras (columns may be missing) ──
def safe_avg(series_name):
    return round(done[series_name].mean(), 2) if series_name in done else 0

dur  = safe_avg("Duration (mins)")
qual = safe_avg("Execution Quality")
diff = safe_avg("Difficulty")

def ratio(col):
    if col not in df: return 0.0
    yes = df[col].astype(str).str.lower().isin(["y", "yes", "true", "1"]).sum()
    return round(yes * 100 / len(df), 1)

gdb_pct      = ratio("GDB Used")
mem_pct      = ratio("Memory Tracing")
diag_pct     = ratio("Diagram Made")
anki_total   = int(df["Anki Cards"].sum()) if "Anki Cards" in df else 0

# ETA
if completed:
    first_date  = pd.to_datetime(done["Date"].iloc[0])
    today       = pd.Timestamp.now(tz="Asia/Kolkata").normalize()
    days_passed = max((today - first_date).days, 1)
    daily_rate  = completed / days_passed
    eta_days    = math.ceil(pending / daily_rate) if daily_rate else -1
else:
    eta_days = -1
eta_date = (dt.datetime.now() + dt.timedelta(days=eta_days)).strftime(DATEFMT) if eta_days > 0 else "N/A"

out = {
    "target_labs": TARGET,
    "labs_completed": completed,
    "labs_pending": pending,
    "efficiency_percent": eff_pct,
    "average_duration_minutes": dur,
    "average_execution_quality": qual,
    "average_difficulty": diff,
    "anki_cards_total": anki_total,
    "gdb_usage_percent": gdb_pct,
    "memory_trace_percent": mem_pct,
    "diagram_coverage_percent": diag_pct,
    "eta_days": eta_days if eta_days > 0 else "N/A",
    "estimated_completion_date": eta_date
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(out, f, indent=2)

print(f"Wrote {OUT}: {out}")
# ==== end paste ====================================================
