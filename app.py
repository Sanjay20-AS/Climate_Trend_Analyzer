"""Interactive Streamlit dashboard."""
from pathlib import Path
import streamlit as st
import pandas as pd
from src.data_loader import load_climate_data
from src.descriptive_analysis import annual_summary, monthly_climatology
from src.trend_analysis import calculate_trend
from src.anomaly_detection import calculate_anomalies
from src.forecasting import evaluate_forecasts
from src.decomposition import decompose_monthly_series

st.set_page_config(page_title="Climate Trend Analyzer", page_icon="🌍", layout="wide")
st.title("🌍 Climate Trend Analyzer")
st.caption("Educational time-series analysis. The bundled dataset is synthetic.")
upload=st.sidebar.file_uploader("Upload CSV",type=["csv"])
if upload:
    path=Path("outputs/dashboard_upload.csv"); path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(upload.getvalue())
else: path=Path("data/synthetic_climate_data.csv")
try: data=load_climate_data(path)
except Exception as exc: st.error(f"Unable to load data: {exc}"); st.stop()
minimum,maximum=data.date.min().date(),data.date.max().date()
start=st.sidebar.date_input("Start date",minimum,min_value=minimum,max_value=maximum)
end=st.sidebar.date_input("End date",maximum,min_value=minimum,max_value=maximum)
if start>end: st.error("Start date must not be after end date."); st.stop()
df=data[(data.date.dt.date>=start)&(data.date.dt.date<=end)].copy()
annual=annual_summary(df); climatology=monthly_climatology(df); anomalies=calculate_anomalies(df)
a,b,c,d=st.columns(4)
a.metric("Monthly rows",len(df)); b.metric("Years",df.date.dt.year.nunique())
c.metric("Mean temperature",f"{df.temperature.mean():.2f} °C")
d.metric("Anomaly flags",int(anomalies.anomaly_flag.sum()))
left,right=st.columns(2)
with left:
    st.subheader("Monthly temperature"); st.line_chart(df.set_index("date")[["temperature"]])
with right:
    st.subheader("Annual mean temperature"); st.line_chart(annual.set_index("year")[["mean_temperature"]])
st.subheader("Monthly climatology"); st.bar_chart(climatology.set_index("month")[["mean_temperature"]])
if len(annual)>=3:
    trend=calculate_trend(annual)
    x,y,z=st.columns(3); x.metric("OLS slope",f"{trend['slope_c_per_decade']:.3f} °C/decade")
    y.metric("R²",f"{trend['r_squared']:.3f}"); z.metric("OLS p-value",f"{trend['p_value_ols']:.3g}")
    st.warning("Exploratory OLS only: autocorrelation and data quality can affect uncertainty.")
st.subheader("Temperature anomalies")
st.line_chart(anomalies.set_index("date")[["temperature_anomaly"]])
st.dataframe(anomalies[anomalies.anomaly_flag][["date","temperature","temperature_anomaly","robust_z_score"]],use_container_width=True)
with st.expander("STL decomposition"):
    decomp=decompose_monthly_series(df)
    if decomp is None: st.info("Requires at least 24 continuous monthly observations.")
    else: st.line_chart(decomp.set_index("date")[["trend","seasonal","residual"]])
with st.expander("Forecast model comparison"):
    metrics,holdout=evaluate_forecasts(df)
    if metrics.empty: st.info("Use at least 36 monthly observations.")
    else:
        st.dataframe(metrics,use_container_width=True)
        st.line_chart(holdout.set_index("date")[["actual_temperature","seasonal_naive_prediction","random_forest_prediction"]])
        st.caption("Chronological holdout is a demonstration, not an official climate projection.")
with st.expander("Annual summary"): st.dataframe(annual,use_container_width=True)
st.download_button("Download filtered monthly CSV",df.to_csv(index=False).encode(),file_name="climate_monthly.csv",mime="text/csv")
