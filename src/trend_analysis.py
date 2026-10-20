"""Exploratory linear trend estimation."""
from scipy import stats


def calculate_trend(annual):
    valid = annual.dropna(subset=["year", "mean_temperature"])
    if len(valid) < 3:
        raise ValueError("At least three annual observations are required.")
    fit = stats.linregress(valid["year"].astype(float), valid["mean_temperature"].astype(float))
    low, high = fit.slope - 1.96*fit.stderr, fit.slope + 1.96*fit.stderr
    return {
        "start_year": int(valid.year.min()), "end_year": int(valid.year.max()),
        "years": int(len(valid)), "slope_c_per_year": float(fit.slope),
        "slope_c_per_decade": float(fit.slope*10), "intercept": float(fit.intercept),
        "r_squared": float(fit.rvalue**2), "p_value_ols": float(fit.pvalue),
        "slope_ci95_c_per_year_approx": [float(low), float(high)],
        "caution": "Exploratory OLS; autocorrelation can make conventional uncertainty unreliable."
    }
