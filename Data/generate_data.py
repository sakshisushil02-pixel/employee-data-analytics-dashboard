"""
generate_data.py
-----------------
Creates a synthetic but realistic 'raw' employee dataset with the kinds
of messiness real datasets have: missing values, inconsistent casing,
duplicate rows, mixed date formats. This gives us genuine cleaning work
to do in step 2 -- not just a story we made up for the interview.
"""

import numpy as np # type: ignore
import pandas as pd # type: ignore

np.random.seed(42)

departments = ["Sales", "Engineering", "Marketing", "HR", "Finance", "Support"]
dept_case_variants = {  # to simulate messy real-world entry
    "Sales": ["Sales", "sales", "SALES"],
    "Engineering": ["Engineering", "engineering", "Engg"],
    "Marketing": ["Marketing", "marketing"],
    "HR": ["HR", "hr", "Human Resources"],
    "Finance": ["Finance", "finance"],
    "Support": ["Support", "support"],
}

n = 500
names = [f"Employee_{i}" for i in range(1, n + 1)]
dept_choice = np.random.choice(departments, size=n, p=[0.25, 0.25, 0.15, 0.1, 0.15, 0.1])

# introduce messy department labels
dept_raw = [np.random.choice(dept_case_variants[d]) for d in dept_choice]

# base salary per department (so department-wise analysis is meaningful)
base_salary = {"Sales": 55000, "Engineering": 90000, "Marketing": 60000,
                "HR": 50000, "Finance": 70000, "Support": 45000}
salary = [max(20000, np.random.normal(base_salary[d], 12000)) for d in dept_choice]

# performance score 1-10, correlated loosely with salary + noise
performance = [
    float(np.clip(np.random.normal(6 + (s - base_salary[d]) / 20000, 1.5), 1, 10))
    for s, d in zip(salary, dept_choice)
]

join_dates = pd.date_range("2018-01-01", "2024-06-01", periods=n)
# mix date formats to simulate messy input
date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]
join_date_str = [d.strftime(np.random.choice(date_formats)) for d in join_dates]

ages = np.random.randint(22, 60, size=n)

df = pd.DataFrame({
    "EmployeeID": range(1001, 1001 + n),
    "Name": names,
    "Department": dept_raw,
    "Age": ages,
    "Salary": salary,
    "PerformanceScore": performance,
    "JoinDate": join_date_str,
    "MonthlySales": np.round(np.random.normal(40000, 15000, n), 2),
})

# inject missing values (realistic messiness)
for col in ["Salary", "PerformanceScore", "Age", "MonthlySales"]:
    idx = np.random.choice(df.index, size=int(n * 0.04), replace=False)
    df.loc[idx, col] = np.nan

# inject a few duplicate rows
df = pd.concat([df, df.sample(5, random_state=1)], ignore_index=True)

# inject a few negative/invalid salary and age typos (bad data entry)
bad_idx = np.random.choice(df.index, size=3, replace=False)
df.loc[bad_idx, "Salary"] = -1

df.to_csv(r"C:\Users\sp940\OneDrive\Desktop\Employee_Dashboard\data\employee_data_raw.csv", index=False)
print("Raw dataset created:", df.shape)