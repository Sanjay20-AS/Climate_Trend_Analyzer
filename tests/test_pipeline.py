import pandas as pd
import pytest
from src.data_loader import load_climate_data
from src.trend_analysis import calculate_trend
from src.anomaly_detection import calculate_anomalies
from src.forecasting import evaluate_forecasts


def test_monthly_aggregation(tmp_path):
    path=tmp_path/"input.csv"
    pd.DataFrame({"date":["2020-01-01","2020-01-20","2020-02-01"],
                  "temperature":[10,12,14],"precipitation":[2,3,4]}).to_csv(path,index=False)
    result=load_climate_data(path)
    assert len(result)==2
    assert result.iloc[0].temperature==pytest.approx(11)
    assert result.iloc[0].precipitation==pytest.approx(5)


def test_required_columns(tmp_path):
    path=tmp_path/"bad.csv"
    pd.DataFrame({"date":["2020-01-01"],"rain":[2]}).to_csv(path,index=False)
    with pytest.raises(ValueError): load_climate_data(path)


def test_trend_needs_three_years():
    with pytest.raises(ValueError):
        calculate_trend(pd.DataFrame({"year":[2020,2021],"mean_temperature":[20,21]}))


def test_anomaly_columns():
    dates=pd.date_range("2000-01-01",periods=48,freq="MS")
    df=pd.DataFrame({"date":dates,"temperature":[float(d.month) for d in dates]})
    out=calculate_anomalies(df)
    assert "temperature_anomaly" in out and "anomaly_flag" in out


def test_short_series_has_no_forecast_metrics():
    dates=pd.date_range("2020-01-01",periods=18,freq="MS")
    df=pd.DataFrame({"date":dates,"temperature":range(18)})
    metrics,holdout=evaluate_forecasts(df)
    assert metrics.empty and holdout.empty
