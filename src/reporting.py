"""Write machine-readable and human-readable project outputs."""
from pathlib import Path
import json


def write_json(path, payload):
    Path(path).write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def write_report(path, monthly, annual, quality, trend, anomalies, metrics):
    metric_text = "No metrics available for this record length."
    if not metrics.empty:
        metric_text = metrics.to_string(index=False)
    report = f"""# Climate Trend Analyzer — Automated Run Report

> Synthetic-data warning: when using the bundled dataset, all numerical findings below are software-demo results, not observed climate evidence.

## Coverage and quality
- Monthly observations: {len(monthly)}
- Period: {monthly.date.min().date()} to {monthly.date.max().date()}
- Years represented: {len(annual)}
- Missing months in date range: {quality['missing_months']}
- Input rows: {quality['input_rows']}

## Exploratory trend
- OLS slope: {trend['slope_c_per_decade']:.4f} °C/decade
- R²: {trend['r_squared']:.3f}
- OLS p-value: {trend['p_value_ols']:.4g}
- Approximate 95% interval: {trend['slope_ci95_c_per_year_approx'][0]*10:.4f} to {trend['slope_ci95_c_per_year_approx'][1]*10:.4f} °C/decade

## Anomaly screening
- Flagged months: {int(anomalies.anomaly_flag.sum())}
- Rule: absolute robust modified z-score >= 3.5
- Flags are review prompts, not proof of errors or climate events.

## Forecast holdout metrics
```text
{metric_text}
```
A single holdout is not robust validation. Use rolling-origin backtesting before making model-performance claims.

## Limitations
OLS uncertainty can be affected by serial correlation; source definitions and missingness matter. Synthetic data must not be described as observed climate. Neither forecasting approach is an official climate projection.
"""
    Path(path).write_text(report, encoding="utf-8")
