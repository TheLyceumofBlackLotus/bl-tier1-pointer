import pandas as pd
import json
from datetime import datetime, timedelta

df = pd.read_excel("symbol_star_dashboard.xlsm", sheet_name="lab_tracker")

df["Lab Complete"] = df["Lab Complete"].astype(str).str.lower().str.strip()
labs_completed = df[df["Lab Complete"].isin(["yes", "✅"])].shape[0]
total_labs = df[df["Lab ID"].notna()].shape[0]
labs_pending = total_labs - labs_completed
efficiency = round((labs_completed / total_labs) * 100, 2) if total_labs > 0 else 0.0

avg_duration = pd.to_numeric(df["Duration (mins)"], errors="coerce").dropna().mean()
avg_quality = pd.to_numeric(df["Execution Quality"], errors="coerce").dropna().mean()
avg_difficulty = pd.to_numeric(df["Difficulty"], errors="coerce").dropna().mean()
anki_total = pd.to_numeric(df["Anki Cards"], errors="coerce").dropna().sum()

gdb_usage = df["GDB Used"].astype(str).str.lower().str.strip().isin(["yes", "true", "1"]).mean() * 100
mem_trace = df["Memory Tracing"].astype(str).str.lower().str.strip().isin(["yes", "true", "1"]).mean() * 100
diagram_use = df["Diagram Made"].astype(str).str.lower().str.strip().isin(["yes", "true", "1"]).mean() * 100

if avg_duration and labs_pending:
    eta_days = (labs_pending * avg_duration) / (60 * 5)
    completion_date = (datetime.now() + timedelta(days=eta_days)).strftime("%Y-%m-%d")
else:
    eta_days = 0
    completion_date = "N/A"

summary = {
    "total_labs": total_labs,
    "labs_completed": labs_completed,
    "labs_pending": labs_pending,
    "efficiency_percent": round(efficiency, 2),
    "average_duration_minutes": round(avg_duration, 2) if not pd.isna(avg_duration) else 0,
    "average_execution_quality": round(avg_quality, 2) if not pd.isna(avg_quality) else 0,
    "average_difficulty": round(avg_difficulty, 2) if not pd.isna(avg_difficulty) else 0,
    "anki_cards_total": int(anki_total),
    "gdb_usage_percent": round(gdb_usage, 2),
    "memory_trace_percent": round(mem_trace, 2),
    "diagram_coverage_percent": round(diagram_use, 2),
    "eta_days": round(eta_days, 2),
    "estimated_completion_date": completion_date
}

with open("summary.json", "w") as f:
    json.dump(summary, f, indent=4)
