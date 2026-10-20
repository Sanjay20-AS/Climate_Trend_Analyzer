"""Descriptive summaries."""
import pandas as pd


def annual_summary(df):
    work = df.copy()
    work["year"] = work["date"].dt.year
    return work.groupby("year", as_index=False).agg(
        mean_temperature=("temperature", "mean"),
        min_temperature=("temperature", "min"),
        max_temperature=("temperature", "max"),
        total_precipitation=("precipitation", "sum"),
        months_observed=("temperature", "count"))


def monthly_climatology(df):
    work = df.copy()
    work["month"] = work["date"].dt.month
    return work.groupby("month", as_index=False).agg(
        mean_temperature=("temperature", "mean"),
        std_temperature=("temperature", "std"),
        mean_precipitation=("precipitation", "mean"),
        observations=("temperature", "count"))


def descriptive_statistics(df):
    return df[["temperature", "precipitation"]].describe().to_dict()
