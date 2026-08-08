# Employee Data Analytics Dashboard

A Python-based analytics pipeline that cleans raw employee data and 
generates visual insights and an automated summary report — built to 
simulate a real HR/operations reporting workflow.

## Tech Stack
Python · Pandas · NumPy · Matplotlib · Seaborn

## What it does
- Cleans messy raw data: inconsistent department labels, missing values, 
  duplicate rows, mixed date formats
- Generates visualizations: department-wise performance, salary 
  distribution, monthly trends, performance bands
- Automates report generation: average salary, employee distribution, 
  top-performing departments

## How to run
```bash
pip install -r requirements.txt
python run_dashboard.py
```

## Sample output

![Department Performance](charts/1_department_performance.png)
![Salary Distribution](charts/2_salary_distribution.png)

## Project structure
```
├── data/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── employee_data_raw.csv
│   └── employee_data_clean.csv
├── charts/          # generated visualizations
├── outputs/         # generated report
├── visualize.py
├── generate_report.py
└── run_dashboard.py
```