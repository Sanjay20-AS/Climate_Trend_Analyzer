"""Save figures to disk; charts are reproducible outputs of the pipeline."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def save_figures(monthly, annual, anomalies, holdout, decomposition, output_dir):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11,5))
    ax.plot(monthly.date, monthly.temperature, lw=.8, label="Monthly mean")
    ax.plot(monthly.date, monthly.temperature.rolling(12,min_periods=6).mean(), lw=2, label="12-month rolling mean")
    ax.set(title="Monthly temperature and rolling mean", xlabel="Date", ylabel="Temperature (°C)")
    ax.legend(); fig.tight_layout(); fig.savefig(out/"temperature_timeseries.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(annual.year, annual.mean_temperature, marker="o", label="Annual mean")
    if len(annual)>=3:
        slope, intercept = np.polyfit(annual.year, annual.mean_temperature, 1)
        ax.plot(annual.year, slope*annual.year+intercept, "--", label="OLS trend")
    ax.set(title="Annual mean temperature and linear trend", xlabel="Year", ylabel="Temperature (°C)")
    ax.legend(); fig.tight_layout(); fig.savefig(out/"annual_temperature_trend.png", dpi=150); plt.close(fig)

    clim=monthly.assign(month=monthly.date.dt.month).groupby("month").temperature.mean()
    fig, ax=plt.subplots(figsize=(9,4.5)); ax.bar(clim.index,clim.values)
    ax.set(title="Monthly climatology",xlabel="Calendar month",ylabel="Temperature (°C)",xticks=range(1,13))
    fig.tight_layout(); fig.savefig(out/"monthly_climatology.png",dpi=150); plt.close(fig)

    fig, ax=plt.subplots(figsize=(11,4.5)); ax.axhline(0,lw=1)
    ax.plot(anomalies.date,anomalies.temperature_anomaly,lw=.8)
    flags=anomalies[anomalies.anomaly_flag]
    if len(flags): ax.scatter(flags.date,flags.temperature_anomaly,label="Robust flag"); ax.legend()
    ax.set(title="Temperature anomalies and robust flags",xlabel="Date",ylabel="Anomaly (°C)")
    fig.tight_layout(); fig.savefig(out/"temperature_anomalies.png",dpi=150); plt.close(fig)

    if decomposition is not None:
        fig,axes=plt.subplots(4,1,figsize=(11,8),sharex=True)
        for ax,col in zip(axes,["observed","trend","seasonal","residual"]):
            ax.plot(decomposition.date,decomposition[col],lw=.8); ax.set_ylabel(col)
        axes[0].set_title("STL decomposition")
        fig.tight_layout(); fig.savefig(out/"stl_decomposition.png",dpi=150); plt.close(fig)

    if not holdout.empty:
        fig,ax=plt.subplots(figsize=(11,4.5))
        ax.plot(holdout.date,holdout.actual_temperature,marker="o",label="Actual")
        for col,label in [("seasonal_naive_prediction","Seasonal naive"),("random_forest_prediction","Random Forest")]:
            if col in holdout and holdout[col].notna().any(): ax.plot(holdout.date,holdout[col],marker=".",label=label)
        ax.set(title="Chronological holdout evaluation",xlabel="Date",ylabel="Temperature (°C)")
        ax.legend(); fig.tight_layout(); fig.savefig(out/"forecast_holdout.png",dpi=150); plt.close(fig)
