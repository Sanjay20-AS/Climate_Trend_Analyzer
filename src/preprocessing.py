"""Reusable transformations and calendar features."""
import numpy as np
import pandas as pd


def add_calendar_features(df):
    out = df.copy()
    out["year"] = out["date"].dt.year
    out["month"] = out["date"].dt.month
    out["month_sin"] = np.sin(2*np.pi*out["month"]/12)
    out["month_cos"] = np.cos(2*np.pi*out["month"]/12)
    return out


def add_rolling_statistics(df, window=12):
    out = df.sort_values("date").copy()
    out[f"rolling_mean_{window}"] = out["temperature"].rolling(window, min_periods=max(3, window//2)).mean()
    out[f"rolling_std_{window}"] = out["temperature"].rolling(window, min_periods=max(3, window//2)).std()
    return out


def find_missing_months(df):
    expected = pd.date_range(df["date"].min(), df["date"].max(), freq="MS")
    return expected.difference(pd.DatetimeIndex(df["date"]))
