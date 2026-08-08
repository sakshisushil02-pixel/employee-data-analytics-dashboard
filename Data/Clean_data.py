"""
clean_data.py
-------------
Cleans and preprocesses the raw employee dataset.

Interview talking point: walk through EACH step and WHY you did it,
not just what function you called.
"""

import pandas as pd # type: ignore
import numpy as np # type: ignore

df = pd.read_csv(r"C:\Users\sp940\OneDrive\Desktop\Employee_Dashboard\data\employee_data_raw.csv")
print("Raw shape:", df.shape)

# 1. Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows")

# 2. Standardize the Department column (fix inconsistent casing / naming)
dept_map = {
    "sales": "Sales", "SALES": "Sales", "Sales": "Sales",
    "engineering": "Engineering", "Engg": "Engineering", "Engineering": "Engineering",
    "marketing": "Marketing", "Marketing": "Marketing",
    "hr": "HR", "HR": "HR", "Human Resources": "HR",
    "finance": "Finance", "Finance": "Finance",
    "support": "Support", "Support": "Support",
}
df["Department"] = df["Department"].map(dept_map)

# 3. Parse JoinDate despite mixed formats
def parse_date(val):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df["JoinDate"] = df["JoinDate"].apply(parse_date)

# 4. Fix invalid values: negative salaries are impossible -> treat as missing
df.loc[df["Salary"] < 0, "Salary"] = np.nan

# 5. Handle missing values
#    - Numeric columns: impute with the department-wise median (more meaningful
#      than a single global median, since salary/performance vary by department)
for col in ["Salary", "PerformanceScore", "MonthlySales"]:
    df[col] = df.groupby("Department")[col].transform(lambda x: x.fillna(x.median()))

#    - Age: no strong department relationship, use overall median
df["Age"] = df["Age"].fillna(df["Age"].median())

# 6. Feature engineering (derived columns used later in analysis)
df["TenureYears"] = ((pd.Timestamp("2025-01-01") - df["JoinDate"]).dt.days / 365).round(1)
df["PerformanceBand"] = pd.cut(
    df["PerformanceScore"], bins=[0, 4, 7, 10],
    labels=["Low", "Medium", "High"]
)

# 7. Final sanity checks
assert df["Department"].isna().sum() == 0
assert df.duplicated().sum() == 0
print("Missing values after cleaning:\n", df.isna().sum())

df.to_csv(r"C:\Users\sp940\OneDrive\Desktop\Employee_Dashboard\data\employee_data_clean.csv", index=False)
print("\nCleaned shape:", df.shape)
print(df.head())