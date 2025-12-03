# scripts/aggregation.py
#  aggregation (daily totals and building summary).
# Run: python scripts/aggregation.py

import pandas as pd
from pathlib import Path

INPUT = Path("output/cleaned_energy_data.csv")   # created in Step 1
OUT = Path("output")
OUT.mkdir(exist_ok=True)

def main():
    if not INPUT.exists():
        print("Error: cleaned_energy_data.csv not found. Run Step 1 first.")
        return

    # load cleaned data
    df = pd.read_csv(INPUT, parse_dates=["timestamp"])
    # ensure kwh numeric
    df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce").fillna(0)

    # === 1) Campus daily total ===
    daily = df.set_index("timestamp").resample("D")["kwh"].sum().reset_index()
    daily = daily.rename(columns={"kwh": "campus_kwh"})
    daily_file = OUT / "daily_totals_simple.csv"
    daily.to_csv(daily_file, index=False)
    print("Saved:", daily_file)

    # === 2) Building summary (total kWh and avg daily kWh) ===
    if "building" in df.columns:
        # total kWh per building
        total_build = df.groupby("building")["kwh"].sum().reset_index().rename(columns={"kwh": "total_kwh"})

        # average daily kWh per building
        df2 = df.set_index("timestamp")
        daily_by_build = df2.groupby("building")["kwh"].resample("D").sum().reset_index()
        avg_daily = daily_by_build.groupby("building")["kwh"].mean().reset_index().rename(columns={"kwh": "avg_daily_kwh"})

        summary = pd.merge(total_build, avg_daily, on="building")
        summary_file = OUT / "building_summary_simple.csv"
        summary.to_csv(summary_file, index=False)
        print("Saved:", summary_file)
    else:
        print("No 'building' column found in cleaned data — skipping building summary.")

    # quick printed checks
    print("\nQuick preview:")
    print("Daily totals (first 5 rows):")
    print(daily.head().to_string(index=False))
    if "building" in df.columns:
        print("\nTop buildings by total_kwh:")
        print(summary.sort_values("total_kwh", ascending=False).head(5).to_string(index=False))

if __name__ == "__main__":
    main()

