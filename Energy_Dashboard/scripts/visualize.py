# scripts/visualize.py
# Step 3: one-line plot of campus daily consumption.
# Run: python scripts/visualize.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

IN = Path("output/daily_totals_simple.csv")
OUT = Path("output")
OUT.mkdir(exist_ok=True)
OUT_FILE = OUT / "dashboard_simple.png"

def main():
    if not IN.exists():
        print("Error: run scripts/aggregation.py first to create daily_totals_simple.csv")
        return

    df = pd.read_csv(IN, parse_dates=["timestamp"])
    if df.empty:
        print("The daily totals file is empty.")
        return

    plt.figure(figsize=(10,4))
    plt.plot(df["timestamp"], df["campus_kwh"], marker="o", linestyle="-")
    plt.title("Campus Daily Energy Consumption")
    plt.xlabel("Date")
    plt.ylabel("kWh")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUT_FILE)
    plt.close()
    print("Saved plot to:", OUT_FILE)

if __name__ == "__main__":
    main()
