"""STL decomposition utilities."""
import pandas as pd
from statsmodels.tsa.seasonal import STL


def decompose_monthly_series(df, period=12, minimum_points=24):
    if len(df) < minimum_points:
        return None
    series = df.set_index("date")["temperature"].asfreq("MS")
    if series.isna().any():
        return None
    result = STL(series, period=period, robust=True).fit()
    return pd.DataFrame({"date": series.index, "observed": series.to_numpy(),
                         "trend": result.trend.to_numpy(), "seasonal": result.seasonal.to_numpy(),
                         "residual": result.resid.to_numpy()})
