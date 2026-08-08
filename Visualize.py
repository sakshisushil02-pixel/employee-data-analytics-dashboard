"""
visualize.py
------------
Generates the three core visualizations for the dashboard:
1. Department-wise performance
2. Salary distribution
3. Monthly trends (average sales over time)

Interview talking point: explain WHY each chart type was chosen for
the data it's showing (bar for comparing categories, histogram/box
for distribution shape, line for trend over time).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
df = pd.read_csv(r"C:\Users\sp940\OneDrive\Desktop\Employee_Dashboard\data\employee_data_clean.csv", parse_dates=["JoinDate"])

OUT = r"C:\Users\sp940\OneDrive\Desktop\Employee_Dashboard\Charts"

# ---------- 1. Department-wise performance ----------
plt.figure(figsize=(9, 5))
dept_perf = df.groupby("Department")["PerformanceScore"].mean().sort_values(ascending=False)
sns.barplot(x=dept_perf.index, y=dept_perf.values, hue=dept_perf.index, palette="viridis", legend=False)
plt.title("Average Performance Score by Department")
plt.ylabel("Avg Performance Score (1-10)")
plt.xlabel("Department")
plt.tight_layout()
plt.savefig(f"{OUT}/1_department_performance.png", dpi=150)
plt.close()

# ---------- 2. Salary distribution ----------
plt.figure(figsize=(9, 5))
sns.histplot(df["Salary"], bins=30, kde=True, color="steelblue")
plt.title("Salary Distribution Across All Employees")
plt.xlabel("Salary")
plt.tight_layout()
plt.savefig(f"{OUT}/2_salary_distribution.png", dpi=150)
plt.close()

# salary by department (boxplot -> shows spread + outliers per dept)
plt.figure(figsize=(9, 5))
sns.boxplot(data=df, x="Department", y="Salary", hue="Department", palette="Set2", legend=False)
plt.title("Salary Spread by Department")
plt.tight_layout()
plt.savefig(f"{OUT}/2b_salary_by_department.png", dpi=150)
plt.close()

# ---------- 3. Monthly trends ----------
df["JoinMonth"] = df["JoinDate"].dt.to_period("M").dt.to_timestamp()
monthly_sales = df.groupby("JoinMonth")["MonthlySales"].mean()

plt.figure(figsize=(11, 5))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o", linewidth=1.5, color="darkorange")
plt.title("Average Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Avg Monthly Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUT}/3_monthly_sales_trend.png", dpi=150)
plt.close()

# ---------- Bonus: performance band distribution (adds depth) ----------
plt.figure(figsize=(7, 5))
band_counts = df["PerformanceBand"].value_counts()
plt.pie(band_counts, labels=band_counts.index, autopct="%1.1f%%",
        colors=sns.color_palette("pastel"))
plt.title("Employee Distribution by Performance Band")
plt.tight_layout()
plt.savefig(f"{OUT}/4_performance_band_pie.png", dpi=150)
plt.close()

print("All charts saved to", OUT)