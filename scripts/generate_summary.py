#!/usr/bin/env python3
"""
Generate docs/summary.json from symbol_star_dashboard.xlsm
— hardened against missing columns, NaNs, blank dates, etc.
"""

import os, math, json, datetime as dt
import pandas as pd

# ─── CONFIG ──────────────────────────────────────────────────────────────
EXCEL          = "symbol_star_dashboard.xlsm"
SHEET          = "lab_tracker"
TARGET_LABS    = 20_000            # ← change if your master target shifts
JSON_OUT       = os.path.join("docs", "summary.json")
LOCAL_TZ       = "Asia/Kolkata"    # keep metrics in IST
DATE_FMT       = "%Y-%m-%d"
SAFE_TRUE_SET  = {"y", "yes", "true", "1"}
# ─────────────────────────────────────────────────────────────────────────

# ─── Load sheet ──────────────────────────────────────────────────────────
try:
    df = pd.read_excel(EXCEL, sheet_name=SHEET)
except FileNotFoundError:
    raise SystemExit(f"❌  {EXCEL} not found in repo root")

df = df[pd.notna(df.get("Lab ID"))]           # keep real rows only
done = df[df.get("Lab Complete", "").astype(str).str.lower().isin(SAFE_TRUE_SET)]

completed       = len(done)
pending         = max(TARGET_LABS - completed, 0)
efficiency_pct  = round(completed * 100 / TARGET_LABS, 2)

# ─── Helper safe-stats ───────────────────────────────────────────────────
def safe_mean(src, col):
    if col not in src or src[col].dropna().empty:
        return 0
    return round(src[col].dropna().mean(), 2)

def bool_ratio(src, col):
    if col not in src or src.empty:
        return 0.0
    yes = src[col].astype(str).str.lower().isin(SAFE_TRUE_SET).sum()
    return round(yes * 100 / len(src), 1)

avg_duration    = safe_mean(done, "Duration (mins)")
avg_quality     = safe_mean(done, "Execution Quality")
avg_difficulty  = safe_mean(done, "Difficulty")
anki_total      = int(df.get("Anki Cards", pd.Series(dtype=float)).fillna(0).sum())

gdb_pct         = bool_ratio(df,  "GDB Used")
mem_pct         = bool_ratio(df,  "Memory Tracing")
diag_pct        = bool_ratio(df,  "Diagram Made")

# ─── ETA calculation ─────────────────────────────────────────────────────
if completed and "Date" in done and done["Date"].notna().any():
    first_date  = pd.to_datetime(done["Date"].dropna().iloc[0])
    today       = pd.Timestamp.now(tz=LOCAL_TZ).normalize()
    days_passed = max((today - first_date).days, 1)
    daily_rate  = completed / days_passed
    eta_days    = math.ceil(pending / daily_rate) if daily_rate else "N/A"
else:
    eta_days    = "N/A"

eta_date = (
    (dt.datetime.now() + dt.timedelta(days=eta_days)).strftime(DATE_FMT)
    if isinstance(eta_days, int) and eta_days > 0
    else "N/A"
)

# ─── Assemble payload ────────────────────────────────────────────────────
out = {
    "target_labs":              TARGET_LABS,
    "labs_completed":           completed,
    "labs_pending":             pending,
    "efficiency_percent":       efficiency_pct,
    "average_duration_minutes": avg_duration,
    "average_execution_quality":avg_quality,
    "average_difficulty":       avg_difficulty,
    "anki_cards_total":         anki_total,
    "gdb_usage_percent":        gdb_pct,
    "memory_trace_percent":     mem_pct,
    "diagram_coverage_percent": diag_pct,
    "eta_days":                 eta_days,
    "projected_completion_date":eta_date,
    "last_updated":             pd.Timestamp.now(tz=LOCAL_TZ).strftime("%Y-%m-%d %H:%M %Z")
}

# ─── Write json ──────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=4)

print(f"✅  Wrote {JSON_OUT}: {out}")
