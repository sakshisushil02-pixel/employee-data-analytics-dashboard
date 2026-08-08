"""
generate_report.py
-------------------
Automates the insight-extraction step: instead of someone manually
opening the spreadsheet and eyeballing numbers, this script computes
and writes out the key metrics automatically.

This is the piece that maps directly to the resume line:
"Automated report generation by extracting insights such as average
salary, employee distribution, and top-performing departments."
"""

import pandas as pd
from datetime import datetime

df = pd.read_csv(r"C:\Users\sp940\OneDrive\Desktop\Employee_Dashboard\data\employee_data_clean.csv", parse_dates=["JoinDate"])

lines = []
lines.append(f"EMPLOYEE ANALYTICS REPORT")
lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
lines.append(f"Total Employees Analyzed: {len(df)}")
lines.append("=" * 50)

# --- Overall metrics ---
lines.append("\n1. OVERALL METRICS")
lines.append(f"   Average Salary: ${df['Salary'].mean():,.2f}")
lines.append(f"   Median Salary: ${df['Salary'].median():,.2f}")
lines.append(f"   Average Performance Score: {df['PerformanceScore'].mean():.2f}/10")
lines.append(f"   Average Tenure: {df['TenureYears'].mean():.1f} years")

# --- Employee distribution by department ---
lines.append("\n2. EMPLOYEE DISTRIBUTION BY DEPARTMENT")
dist = df["Department"].value_counts()
for dept, count in dist.items():
    pct = count / len(df) * 100
    lines.append(f"   {dept:<12}: {count:>4} employees ({pct:.1f}%)")

# --- Top-performing departments ---
lines.append("\n3. TOP-PERFORMING DEPARTMENTS (by avg performance score)")
top_depts = df.groupby("Department")["PerformanceScore"].mean().sort_values(ascending=False)
for i, (dept, score) in enumerate(top_depts.items(), 1):
    lines.append(f"   #{i} {dept:<12}: {score:.2f}/10")

# --- Salary by department ---
lines.append("\n4. AVERAGE SALARY BY DEPARTMENT")
salary_by_dept = df.groupby("Department")["Salary"].mean().sort_values(ascending=False)
for dept, sal in salary_by_dept.items():
    lines.append(f"   {dept:<12}: ${sal:,.2f}")

# --- High performers needing attention (low performers) ---
lines.append("\n5. PERFORMANCE BAND SUMMARY")
band_dist = df["PerformanceBand"].value_counts()
for band, count in band_dist.items():
    lines.append(f"   {band:<8}: {count} employees")

report_text = "\n".join(lines)
print(report_text)

with open(r"C:\Users\sp940\OneDrive\Desktop\Employee_Dashboard\Outputs\employee_report.txt", "w") as f:
    f.write(report_text)

print("\n\nReport saved to outputs/employee_report.txt")