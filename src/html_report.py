import csv
from datetime import datetime


# Read drift report
report_file = "reports/drift_report.csv"

with open(report_file, "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)


# Count risk levels
high_count = sum(1 for row in data if row["Risk"] == "HIGH")
medium_count = sum(1 for row in data if row["Risk"] == "MEDIUM")
low_count = sum(1 for row in data if row["Risk"] == "LOW")

total_drift = len(data)


# Create table rows
table_rows = ""

for row in data:

    risk = row["Risk"]

    if risk == "HIGH":
        risk_class = "high"
    elif risk == "MEDIUM":
        risk_class = "medium"
    else:
        risk_class = "low"

    table_rows += f"""
    <tr>
        <td>{row["Environment"]}</td>
        <td>{row["Configuration"]}</td>
        <td>{row["Expected"]}</td>
        <td>{row["Actual"]}</td>
        <td><span class="risk {risk_class}">{risk}</span></td>
    </tr>
    """


# Generate HTML
html = f"""
<!DOCTYPE html>
<html>

<head>

<title>Environment Drift Detection Dashboard</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background-color: #f4f6f8;
    margin: 0;
    padding: 30px;
}}

h1 {{
    text-align: center;
}}

.subtitle {{
    text-align: center;
    color: #666;
}}

.cards {{
    display: flex;
    gap: 20px;
    justify-content: center;
    margin: 30px 0;
}}

.card {{
    background: white;
    padding: 20px;
    width: 180px;
    text-align: center;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

.card h2 {{
    margin: 0;
    font-size: 30px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

th, td {{
    padding: 14px;
    text-align: center;
    border-bottom: 1px solid #ddd;
}}

th {{
    background-color: #343a40;
    color: white;
}}

.risk {{
    padding: 6px 12px;
    border-radius: 5px;
    font-weight: bold;
}}

.high {{
    background-color: #ffcccc;
    color: #b30000;
}}

.medium {{
    background-color: #ffe5b4;
    color: #cc6600;
}}

.low {{
    background-color: #ccffcc;
    color: #006600;
}}

.footer {{
    text-align: center;
    margin-top: 30px;
    color: #777;
}}

</style>

</head>


<body>

<h1>Environment Drift Detection Dashboard</h1>

<p class="subtitle">
Automated Multi-Stage DevOps Environment Monitoring
</p>


<div class="cards">

<div class="card">
<h2>{total_drift}</h2>
<p>Total Drift</p>
</div>

<div class="card">
<h2>{high_count}</h2>
<p>High Risk</p>
</div>

<div class="card">
<h2>{medium_count}</h2>
<p>Medium Risk</p>
</div>

<div class="card">
<h2>{low_count}</h2>
<p>Low Risk</p>
</div>

</div>


<h2>Detected Configuration Drift</h2>


<table>

<tr>
<th>Environment</th>
<th>Configuration</th>
<th>Expected</th>
<th>Actual</th>
<th>Risk</th>
</tr>

{table_rows}

</table>


<div class="footer">

Generated automatically on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

</div>

</body>

</html>
"""


# Save HTML report
output_file = "reports/drift_dashboard.html"

with open(output_file, "w") as file:
    file.write(html)


print("\nHTML dashboard generated successfully!")
print(f"Dashboard saved to: {output_file}")