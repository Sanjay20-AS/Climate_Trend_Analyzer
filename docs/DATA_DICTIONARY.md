# Data dictionary

Input: `date` (date), `temperature` (numeric °C), optional `precipitation` (numeric mm; only sum it if source semantics support that).

Outputs:
- `data_quality.json`: invalid rows, duplicates, missing months and date range
- `annual_summary.csv`: annual mean/min/max temperature, precipitation sum, coverage
- `monthly_climatology.csv`: month-of-year means and spread
- `anomalies.csv`: calendar-month anomaly and robust modified z-score
- `forecast_metrics.csv`: time-ordered holdout MAE/RMSE/R²
- `forecast_holdout.csv`: actual and predicted temperatures
- `stl_decomposition.csv`: observed, trend, seasonal and residual components
- `trend_summary.json`: slope, R², p-value, approximate confidence interval
- `report.md`: automated summary
