"""Data quality diagnostics."""
import pandas as pd
from .data_loader import load_raw_csv


def build_quality_report(path, monthly):
    raw = load_raw_csv(path)
    dates = raw["date"]
    temps = raw["temperature"]
    expected = pd.date_range(monthly.date.min(), monthly.date.max(), freq="MS")
    missing = expected.difference(pd.DatetimeIndex(monthly.date))
    return {
        "input_rows": int(len(raw)),
        "invalid_date_rows": int(dates.isna().sum()),
        "invalid_temperature_rows": int(temps.isna().sum()),
        "duplicate_source_dates": int(dates[dates.notna()].duplicated().sum()),
        "monthly_rows": int(len(monthly)),
        "start_date": str(monthly.date.min().date()),
        "end_date": str(monthly.date.max().date()),
        "missing_months": int(len(missing)),
        "missing_month_examples": [str(x.date()) for x in missing[:12]],
        "precipitation_available": bool(monthly.precipitation.notna().any()),
        "note": "Check source-specific missing codes, units, station changes and coverage."
    }
