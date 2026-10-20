"""Calendar-month anomalies and robust outlier screening."""
import numpy as np


def calculate_anomalies(df, threshold=3.5):
    out = df.copy()
    out["calendar_month"] = out.date.dt.month
    grouped = out.groupby("calendar_month")["temperature"]
    means, medians = grouped.mean(), grouped.median()
    mads = grouped.apply(lambda s: np.median(np.abs(s - np.median(s))))
    out["calendar_month_mean"] = out.calendar_month.map(means)
    out["temperature_anomaly"] = out.temperature - out.calendar_month_mean
    out["month_median"] = out.calendar_month.map(medians)
    out["month_mad"] = out.calendar_month.map(mads)
    scale = 1.4826*out["month_mad"].replace(0, np.nan)
    out["robust_z_score"] = (out.temperature-out.month_median)/scale
    out["anomaly_flag"] = out.robust_z_score.abs() >= threshold
    return out.drop(columns=["month_median", "month_mad"])
