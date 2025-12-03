# Energy Dashboard 

This project demonstrates a simple energy monitoring system built using Python.  
It loads raw CSV energy data, cleans it, aggregates daily usage, visualizes trends, and generates an executive summary.  
The entire solution is designed to be beginner-friendly for first-year B.Tech students.

---

## Project Structure

ENERGY_DASHBOARD/
│
├── data/ # Raw CSV files (input)
├── output/ # Cleaned data, summaries, charts, logs
└── scripts/ # Python scripts for each step
├── ingest.py # Step 1 - Data ingestion & cleaning
├── aggregation.py # Step 2 - Daily and building-level aggregation
├── visualize.py # Step 3 - Daily consumption chart
└── summary.py # Step 4 - Executive summary generator


## Steps to Run the Project

### **Ingest & Clean Data**
Reads all CSV files from the `data/` folder, cleans them, fixes invalid rows, extracts building/month info, and merges into a single dataset.

Run:
python scripts/ingest.py

Outputs:
- `output/cleaned_energy_data.csv`
- `output/ingestion_log.txt`

---

###  ** Aggregate Data**
Calculates:
- Campus daily total kWh  
- Building-wise total energy  
- Building-wise average daily energy  

Run:
python scripts/aggregation.py

Outputs:
- `output/daily_totals_simple.csv`
- `output/building_summary_simple.csv`

---

### **Step 3 — Visualize Trends**
Creates a simple Matplotlib line chart showing daily campus energy usage.

Run:
python scripts/visualize.py

Output:
- `output/dashboard_simple.png`

---

### **Step 4 — Generate Executive Summary**
Automatically creates a short report containing:
- Total campus energy  
- Highest-consuming building  
- Peak usage day  
- Key observations  

Run:
python scripts/summary.py

Output:
- `output/summary.txt`

---

## Requirements

Install required Python libraries:
pip install pandas matplotlib


## Conclusion

This project demonstrates essential Python skills:
- Data ingestion  
- Data cleaning  
- Data aggregation  
- Plotting and visualization  
- Automated reporting  
---

## Prepared By:
Jiya Gupta 
