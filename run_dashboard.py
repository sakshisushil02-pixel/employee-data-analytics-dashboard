"""
run_dashboard.py
-----------------
Single entry point that runs the full pipeline end to end:
raw data -> cleaning -> visualizations -> automated report.

Run with: python3 run_dashboard.py
"""

import subprocess
import sys

steps = [
    ("Generating raw dataset", "Data/generate_data.py"),
    ("Cleaning & preprocessing data", "Data/clean_data.py"),
    ("Generating visualizations", "Visualize.py"),
    ("Generating automated report", "generate_report.py"),
]

for description, script in steps:
    print(f"\n{'='*60}\nSTEP: {description}\n{'='*60}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Failed at step: {description}")
        sys.exit(1)

print("\nDashboard pipeline complete. Check /charts and /outputs folders.")