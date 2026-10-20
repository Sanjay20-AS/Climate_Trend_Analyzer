"""Time-ordered baseline and Random Forest forecast evaluation."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def build_lag_features(df, lags=(1, 2, 3, 6, 12)):
    out = df[["date", "temperature"]].copy()
    for lag in lags:
        out[f"lag_{lag}"] = out.temperature.shift(lag)
    month = out.date.dt.month
    out["month_sin"] = np.sin(2*np.pi*month/12)
    out["month_cos"] = np.cos(2*np.pi*month/12)
    return out.dropna().reset_index(drop=True)


def evaluate_forecasts(df, holdout_months=12):
    if len(df) < 36:
        return pd.DataFrame(), pd.DataFrame()
    holdout = min(holdout_months, max(6, len(df)//5))
    split_date = df.date.iloc[-holdout]
    train, test = df[df.date < split_date].copy(), df[df.date >= split_date].copy()
    if len(train) < 24:
        return pd.DataFrame(), pd.DataFrame()
    actual = test[["date", "temperature"]].rename(columns={"temperature":"actual_temperature"}).copy()
    lookup = df.set_index("date")["temperature"]
    preds = []
    for dt in test.date:
        prev = dt - pd.DateOffset(months=12)
        preds.append(float(lookup.loc[prev]) if prev in lookup.index else np.nan)
    actual["seasonal_naive_prediction"] = preds

    features = build_lag_features(df)
    train_f, test_f = features[features.date < split_date], features[features.date >= split_date]
    columns = [c for c in features.columns if c.startswith("lag_") or c in ("month_sin", "month_cos")]
    if len(train_f) >= 20 and len(test_f) == len(test):
        model = RandomForestRegressor(n_estimators=250, max_depth=8, min_samples_leaf=2,
                                      random_state=42, n_jobs=-1)
        model.fit(train_f[columns], train_f.temperature)
        actual["random_forest_prediction"] = model.predict(test_f[columns])
    else:
        actual["random_forest_prediction"] = np.nan

    rows = []
    for name, col in [("Seasonal naive", "seasonal_naive_prediction"),
                      ("Random Forest", "random_forest_prediction")]:
        valid = actual.dropna(subset=["actual_temperature", col])
        if valid.empty:
            continue
        y, p = valid.actual_temperature, valid[col]
        rows.append({"model":name, "n_test_months":len(valid),
                     "mae":mean_absolute_error(y,p),
                     "rmse":float(np.sqrt(mean_squared_error(y,p))),
                     "r2":r2_score(y,p) if len(valid)>1 else np.nan})
    return pd.DataFrame(rows), actual
