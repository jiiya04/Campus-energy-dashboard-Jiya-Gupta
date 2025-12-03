# ingest_validate.py
# Run: python ingest_validate.py

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CLEANED_CSV = OUTPUT_DIR / "cleaned_energy_data.csv"
LOG_FILE = OUTPUT_DIR / "ingestion_log.txt"

def infer_from_filename(fname):
    p = Path(fname).stem
    p = p.replace("-", "_")
    parts = p.split("_")
    building = parts[0] if parts else None
    month = parts[1] if len(parts) > 1 else None
    return building, month

def read_one(path):
    issues = []
    try:
        df = pd.read_csv(path, on_bad_lines='skip')
    except Exception as e:
        issues.append(f"READ_ERROR: {e}")
        return None, issues

    # normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # parse timestamp if present
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        bad_ts = df["timestamp"].isna().sum()
        if bad_ts:
            issues.append(f"{bad_ts} invalid timestamps -> set to NaT")

    # ensure kwh numeric if present
    if "kwh" in df.columns:
        df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce")
        bad_kwh = df["kwh"].isna().sum()
        if bad_kwh:
            issues.append(f"{bad_kwh} non-numeric kwh -> set to NaN")

    # add building/month from filename if missing
    bld, mon = infer_from_filename(path.name)
    if "building" not in df.columns:
        df["building"] = bld
        issues.append(f"building missing -> filled from filename: {bld}")
    if "month" not in df.columns:
        df["month"] = mon
        if mon is None:
            issues.append("month missing and not inferable from filename")
        else:
            issues.append(f"month missing -> filled from filename: {mon}")

    # drop rows missing timestamp or kwh 
    before = len(df)
    if "timestamp" in df.columns and "kwh" in df.columns:
        df = df.dropna(subset=["timestamp", "kwh"])
        dropped = before - len(df)
        if dropped:
            issues.append(f"Dropped {dropped} rows due to missing timestamp or kwh")
    else:
        issues.append("timestamp or kwh column not present; file may be incomplete")

    df["source_file"] = path.name
    return df, issues

def main():
    all_files = sorted(DATA_DIR.glob("*.csv"))
    if not all_files:
        print("No CSV files found in data/. Put your CSVs inside the data/ folder and run again.")
        return

    cleaned = []
    log_lines = []
    for f in all_files:
        print("Reading", f.name)
        df, issues = read_one(f)
        if df is not None and not df.empty:
            cleaned.append(df)
        else:
            print("  -> no usable rows in", f.name)
        for it in issues:
            line = f"{f.name}: {it}"
            log_lines.append(line)

    if not cleaned:
        print("No data ingested from any file. Check output/ingestion_log.txt for details.")
        Path(LOG_FILE).write_text("\n".join(log_lines))
        return

    df_all = pd.concat(cleaned, ignore_index=True, sort=False)
    # ensure timestamp column exists and sort
    if "timestamp" in df_all.columns:
        df_all = df_all.sort_values("timestamp").reset_index(drop=True)

    df_all.to_csv(CLEANED_CSV, index=False)
    Path(LOG_FILE).write_text("\n".join(log_lines))

    print("Saved cleaned data to:", CLEANED_CSV)
    print("Saved ingestion log to:", LOG_FILE)
    print("Rows in cleaned file:", len(df_all))

if __name__ == "__main__":
    main()
