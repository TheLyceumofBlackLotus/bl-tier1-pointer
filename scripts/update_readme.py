import json
from datetime import datetime

# Load summary.json
with open("summary.json", "r") as f:
    summary = json.load(f)

# Build the dashboard table
readme = f"""# 🧠 BlackLotus Lab Dashboard

> Real-time execution stats synced from lab tracker

| Metric                    | Value        |
|---------------------------|--------------|
| ✅ Total Labs Completed   | {summary['total_labs_done']}         |
| 🔄 Labs Remaining         | {summary['labs_remaining']}         |
| ⚡ Efficiency             | {summary['efficiency_percent']}%     |
| ⏱️ Avg Time per Lab       | {summary['average_time_per_lab_mins']} mins |
| 📅 Projected Completion   | {summary['projected_completion_date']} |
| 🕒 Last Updated           | {summary['last_updated']} |

> **Sync Source:** Excel + Python script → JSON → GitHub push  
> **Next Upgrade:** GitHub Actions badge counter + visual heatmap tracker
"""

# Write to README.md
with open("README.md", "w") as f:
    f.write(readme)
