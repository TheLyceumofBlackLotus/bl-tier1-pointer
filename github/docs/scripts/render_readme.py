# --- append to your existing render script ---
from pathlib import Path
import json, math, datetime

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "summary.json").read_text(encoding="utf-8"))
tmpl = (ROOT / "README.template.md").read_text(encoding="utf-8")

def bar(p, width=20):
    filled = int(p * width)
    return "█"*filled + "░"*(width-filled)

goal = data["goal"]
uploaded = sum(t["uploaded"] for t in data["tiers"])
mutated  = sum(t["mutated"]  for t in data["tiers"])
comp_pct = (uploaded/goal) if goal else 0.0

rows = ["| Tier | Alias | Target | Uploaded | Mutated | Complete | Progress |",
        "|-----:|:------|-------:|---------:|--------:|---------:|:---------|"]
for t in data["tiers"]:
    pct = (t["uploaded"]/t["target"]) if t["target"] else 0.0
    rows.append(f"| {t['tier']} | {t['alias']} | {t['target']} | {t['uploaded']} | {t['mutated']} | {pct*100:5.1f}% | {bar(pct)} |")
table = "\n".join(rows)

ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
updated_at = datetime.datetime.now(tz=ist).strftime("%Y-%m-%d %H:%M:%S")

out = (tmpl.replace("{{GOAL}}", f"{goal:,}")
            .replace("{{UPLOADED}}", f"{uploaded:,}")
            .replace("{{MUTATED}}", f"{mutated:,}")
            .replace("{{COMP_PCT}}", f"{comp_pct*100:0.2f}%")
            .replace("{{TIER_TABLE}}", table)
            .replace("{{UPDATED_AT}}", updated_at))

(ROOT / "README.md").write_text(out, encoding="utf-8")

# --- live Shields badges (keeps your existing gh-pages setup) ---
badges = ROOT / "docs" / "badges"
badges.mkdir(parents=True, exist_ok=True)
def badge(label, message, color): return {"schemaVersion":1,"label":label,"message":message,"color":color}
def color_for(p): return "red" if p<0.1 else "orange" if p<0.25 else "yellow" if p<0.5 else "green"

with open(badges/"total.json","w",encoding="utf-8") as f:
    f.write(json.dumps(badge("labs", f"{uploaded}/{goal} ({comp_pct*100:0.1f}%)", color_for(comp_pct))))
with open(badges/"mutated.json","w",encoding="utf-8") as f:
    mut_pct = mutated / (sum(t["target"] for t in data["tiers"]) or 1)
    f.write(json.dumps(badge("mutations", f"{mutated} mutated", color_for(mut_pct))))
with open(badges/"completion.json","w",encoding="utf-8") as f:
    f.write(json.dumps(badge("completion", f"{comp_pct*100:0.1f}%", color_for(comp_pct))))
