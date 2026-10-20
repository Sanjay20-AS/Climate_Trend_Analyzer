# Methodology

1. Parse dates and numeric columns; remove invalid date/temperature rows; sort and aggregate by calendar month.
2. Calculate annual means and month-of-year climatology. Partial years can affect comparisons.
3. Fit OLS to annual mean temperature versus year. Report °C/decade, R², p-value and approximate 95% interval; autocorrelation can invalidate conventional uncertainty.
4. Define anomaly as temperature minus the mean for that calendar month across the selected record. Use a robust modified z-score based on median absolute deviation to screen unusual values.
5. Use STL with period 12 only when monthly series is continuous and at least 24 observations long.
6. Compare seasonal-naive and Random Forest lag-feature models on a chronological holdout; report MAE/RMSE/R². A single holdout is not strong generalization evidence.
7. Synthetic input is for code demonstration only. No causal attribution or official climate projection is made.
