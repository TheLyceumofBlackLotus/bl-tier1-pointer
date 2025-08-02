import os
import re

TIERS = {
    "tier1": 1000,
    "tier2": 2000,
    "tier3": 3000,
    "tier4": 2000,
    "tier5": 2000,
}

def parse_status(readme_path):
    with open(readme_path, encoding='utf-8') as f:
        content = f.read()
    if '✅ Passed' in content:
        return 'passed'
    elif '🧨 Mutated' in content:
        return 'mutated'
    return 'unknown'

tier_data = {}
total_passed = total_mutated = 0
TOTAL_GOAL = 250_000

for tier, target in TIERS.items():
    path = f"labs/{tier}"
    passed = mutated = 0

    if os.path.exists(path):
        for lab in os.listdir(path):
            readme = os.path.join(path, lab, "README.md")
            if os.path.isfile(readme):
                status = parse_status(readme)
                if status == 'passed': passed += 1
                elif status == 'mutated': mutated += 1

    pending = target - passed
    tier_data[tier] = {
        "target": target,
        "passed": passed,
        "mutated": mutated,
        "pending": pending,
        "percent_done": round((passed / target) * 100, 2) if target else 0.0,
        "percent_pending": 100 - round((passed / target) * 100, 2) if target else 0.0,
    }

    total_passed += passed
    total_mutated += mutated

# ─────────────────────────────────────────────────────────────
# Write to README.md
with open("README.md", encoding='utf-8') as f:
    readme = f.read()

# Remove previous dashboard if it exists
cleaned = re.sub(r"## 🚀 BlackLotus Lab Execution Dashboard[\s\S]*?(?=\n## |\Z)", "", readme)

# Inject dashboard
table = "## 🚀 BlackLotus Lab Execution Dashboard\n\n"
table += "| Tier | Alias | 🎯 Target | ✅ Uploaded | 🔄 Pending | 🧨 Mutated | 📊 % Complete | 📊 % Pending |\n"
table += "|------|------------------------|-----------|-------------|-------------|--------------|----------------|----------------|\n"

TIER_ALIASES = {
    "tier1": "🧠 *The Pointer Forge*",
    "tier2": "🔩 *The Struct Zone*",
    "tier3": "🔁 *The Stack Crucible*",
    "tier4": "💣 *The Exploit Core*",
    "tier5": "🔥 *The Cognitive Furnace*",
}

total_goal = sum([v["target"] for v in tier_data.values()])
total_pending = total_goal - total_passed
total_percent = round((total_passed / TOTAL_GOAL) * 100, 2)
total_percent_pending = 100 - total_percent

for tier, data in tier_data.items():
    table += f"| {tier.capitalize()} | {TIER_ALIASES[tier]} | {data['target']} | {data['passed']} | {data['pending']} | {data['mutated']} | {data['percent_done']}% | {data['percent_pending']}% |\n"

table += f"| **SUBTOTAL** | — | **{total_goal}** | **{total_passed}** | **{total_pending}** | **{total_mutated}** | **{(total_passed/total_goal)*100:.2f}%** | **{(total_pending/total_goal)*100:.2f}%** |\n"

table += "\n---\n\n"

table += "### 🧬 **Full Execution Goal: 250,000 Labs**\n\n"
table += "| Scope        | ✅ Completed | 🔄 Pending | 📊 % Done | 📊 % Pending |\n"
table += "|--------------|--------------|-------------|-----------|----------------|\n"
table += f"| **TOTAL**    | {total_passed} | {TOTAL_GOAL - total_passed} | {total_percent}% | {total_percent_pending}% |\n"
table += f"| Tier 1 Slice | {tier_data['tier1']['passed']} | {tier_data['tier1']['pending']} | {tier_data['tier1']['percent_done']}% | {tier_data['tier1']['percent_pending']}% |\n"

table += "\n---\n"

table += "## 🧠 **Tier Identity Missions**\n\n"
table += "| Tier | Alias | Focus Symbols | Purpose |\n"
table += "|------|------------------------|-----------------------------|---------|\n"
table += "| Tier 1 | 🧠 *The Pointer Forge* | `*`, `**`, `&`, `malloc` | Build instinct-level pointer mutation and memory navigation |\n"
table += "| Tier 2 | 🔩 *The Struct Zone* | `void*`, `[]`, `.`, `->` | Master complex data structures, pointer-to-structs, array decay traps |\n"
table += "| Tier 3 | 🔁 *The Stack Crucible* | `func ptr`, `recursion`, `ABI` | Dominate call stacks, build symbolic control flow, recursive war zones |\n"
table += "| Tier 4 | 💣 *The Exploit Core* | `format`, `overflow`, `ROP` | Build real-world exploit chains from memory leaks to shell access |\n"
table += "| Tier 5 | 🔥 *The Cognitive Furnace* | symbolic chaos, meta-labs | Auto-mutate labs, build AI-driven symbolic generation pipelines |\n"

table += "\n---\n> 🩸 *Note: Only uploaded, passed, or mutated labs are counted. No hallucinated glory. The war only begins when the byte reaches GitHub.*\n\n"

# Final write
with open("README.md", "w", encoding='utf-8') as f:
    f.write(cleaned.strip() + "\n\n" + table)
