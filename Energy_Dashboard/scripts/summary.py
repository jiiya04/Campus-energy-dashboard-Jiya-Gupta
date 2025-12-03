# scripts/summary.py
# script to generate output/summary.txt from cleaned_energy_data.csv
# Run: python scripts/summary.py

import pandas as pd
from pathlib import Path
from datetime import datetime

INPUT = Path("output/cleaned_energy_data.csv")
OUT = Path("output")
OUT.mkdir(exist_ok=True)
OUT_FILE = OUT / "summary.txt"

def safe_read_csv(path):
    try:
        return pd.read_csv(path, parse_dates=["timestamp"])
    except Exception as e:
        print("Error reading cleaned CSV:", e)
        return None

def format_number(x):
    try:
        return f"{float(x):.2f}"
    except:
        return str(x)

def main():
    df = safe_read_csv(INPUT)
    if df is None:
        print("Make sure output/cleaned_energy_data.csv exists (run ingest.py).")
        return

    # Ensure kwh numeric
    if "kwh" in df.columns:
        df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce").fillna(0)
    else:
        print("No 'kwh' column found in cleaned data.")
        df["kwh"] = 0

    # 1) Total campus energy
    total_kwh = df["kwh"].sum()

    # 2) Highest-consuming building
    top_building = "N/A"
    top_building_kwh = 0
    if "building" in df.columns:
        grouped = df.groupby("building")["kwh"].sum()
        if not grouped.empty:
            top_building = grouped.idxmax()
            top_building_kwh = grouped.max()

    # 3) Peak day
    peak_day = "N/A"
    peak_day_kwh = 0
    if "timestamp" in df.columns:
        daily = df.set_index("timestamp").resample("D")["kwh"].sum()
        if not daily.empty:
            peak_ts = daily.idxmax()
            peak_day = peak_ts.date().isoformat()
            peak_day_kwh = daily.max()

    # Prepare summary text
    txt = []
    txt.append("Energy Dashboard — Executive Summary")
    txt.append("-----------------------------------")
    txt.append("")
    txt.append(f"Project: Simple Campus Energy Dashboard")
    txt.append(f"Files used: {INPUT.as_posix()}")
    txt.append(f"Date generated: {datetime.now().isoformat(timespec='seconds')}")
    txt.append("")
    txt.append("1) Total campus energy (covered period)")
    txt.append("---------------------------------------")
    txt.append(f"Total campus energy (sum of kWh in cleaned data): {format_number(total_kwh)} kWh")
    txt.append("")
    txt.append("2) Highest-consuming building")
    txt.append("-----------------------------")
    txt.append(f"Building with highest total consumption: {top_building}")
    txt.append(f"Total energy for that building: {format_number(top_building_kwh)} kWh")
    txt.append("")
    txt.append("3) Peak day (highest single-day campus consumption)")
    txt.append("---------------------------------------------------")
    txt.append(f"Date with highest campus consumption: {peak_day}")
    txt.append(f"Campus kWh on that day: {format_number(peak_day_kwh)} kWh")
    txt.append("")
    txt.append("4) Simple observations / notes")
    txt.append("------------------------------")
    txt.append("- Data source: all CSV files placed in the `data/` folder and merged by `ingest.py`.")
    txt.append("- Time resolution: original readings may be hourly; aggregation here is daily.")
    txt.append("- Missing or invalid rows were dropped during ingestion and recorded in `output/ingestion_log.txt`.")
    txt.append("- Building names (if missing) were inferred from filenames where possible.")
    txt.append("")
    txt.append("5) Suggestions / next steps (short)")
    txt.append("-----------------------------------")
    txt.append("- Add more months of raw CSVs to increase analysis period.")
    txt.append("- Create weekly and monthly trend charts to show longer-term patterns.")
    txt.append("- Flag unusually high single-day or single-hour spikes for investigation.")
    txt.append("")
    txt.append("Prepared by: Jiya Gupta")

    # Write file
    OUT_FILE.write_text("\n".join(txt))
    print("Saved summary to:", OUT_FILE)
    print("Summary contents:")
    print("\n".join(txt[:12]) + "\n...")  # print first lines as quick check

if __name__ == "__main__":
    main()
