"""CSV ingestion and monthly aggregation."""
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {"date", "temperature"}


def load_raw_csv(path):
    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(sorted(missing))}")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    if "precipitation" not in df:
        df["precipitation"] = np.nan
    else:
        df["precipitation"] = pd.to_numeric(df["precipitation"], errors="coerce")
    return df


def aggregate_monthly(raw):
    valid = raw.dropna(subset=["date", "temperature"]).sort_values("date").copy()
    if valid.empty:
        raise ValueError("No valid rows remain after date/temperature parsing.")
    valid["period"] = valid["date"].dt.to_period("M")
    monthly = valid.groupby("period", as_index=False).agg(
        date=("date", "min"),
        temperature=("temperature", "mean"),
        precipitation=("precipitation", lambda s: s.sum(min_count=1)),
        source_rows=("temperature", "size"))
    monthly["date"] = monthly["period"].dt.to_timestamp()
    return monthly.drop(columns="period").sort_values("date").reset_index(drop=True)


def load_climate_data(path):
    return aggregate_monthly(load_raw_csv(path))
