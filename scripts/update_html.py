import json
from datetime import datetime

# Load the JSON summary
with open("summary.json", "r") as f:
    data = json.load(f)

# Generate HTML content
html = f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🧠 BlackLotus Lab Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #0d1117; color: #c9d1d9; padding: 2em; }}
        h1 {{ color: #58a6ff; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 2em; }}
        th, td {{ padding: 12px; border: 1px solid #30363d; text-align: left; }}
        th {{ background-color: #161b22; }}
        td {{ background-color: #161b22; }}
        .footer {{ margin-top: 3em; font-size: 0.9em; color: #8b949e; }}
    </style>
</head>
<body>
    <h1>🧠 BlackLotus Lab Dashboard</h1>
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>✅ Total Labs Completed</td><td>{data['total_labs_done']}</td></tr>
        <tr><td>🔄 Labs Remaining</td><td>{data['labs_remaining']}</td></tr>
        <tr><td>⚡ Efficiency</td><td>{data['efficiency_percent']}%</td></tr>
        <tr><td>⏱️ Avg Time per Lab</td><td>{data['average_time_per_lab_mins']} mins</td></tr>
        <tr><td>📅 Projected Completion</td><td>{data['projected_completion_date']}</td></tr>
        <tr><td>🕒 Last Updated</td><td>{data['last_updated']}</td></tr>
    </table>

    <div class="footer">
        Powered by: BlackLotus Tracker v1.0 | Auto-generated from <code>summary.json</code>
    </div>
</body>
</html>
"""

# Save to docs/dashboard.html
with open("docs/dashboard.html", "w") as f:
    f.write(html)
