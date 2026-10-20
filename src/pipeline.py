"""Orchestrate the modular analysis components."""
from pathlib import Path
from .data_loader import load_climate_data
from .data_quality import build_quality_report
from .descriptive_analysis import annual_summary, monthly_climatology
from .trend_analysis import calculate_trend
from .anomaly_detection import calculate_anomalies
from .decomposition import decompose_monthly_series
from .forecasting import evaluate_forecasts
from .visualization import save_figures
from .reporting import write_json, write_report


def run_pipeline(input_path="data/synthetic_climate_data.csv", output_dir="outputs"):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    monthly = load_climate_data(input_path)
    quality = build_quality_report(input_path, monthly)
    annual = annual_summary(monthly)
    climatology = monthly_climatology(monthly)
    trend = calculate_trend(annual)
    anomalies = calculate_anomalies(monthly)
    decomposition = decompose_monthly_series(monthly)
    metrics, holdout = evaluate_forecasts(monthly)

    annual.to_csv(out/"annual_summary.csv", index=False)
    climatology.to_csv(out/"monthly_climatology.csv", index=False)
    anomalies.to_csv(out/"anomalies.csv", index=False)
    metrics.to_csv(out/"forecast_metrics.csv", index=False)
    holdout.to_csv(out/"forecast_holdout.csv", index=False)
    if decomposition is not None: decomposition.to_csv(out/"stl_decomposition.csv", index=False)
    write_json(out/"trend_summary.json", trend)
    write_json(out/"data_quality.json", quality)
    save_figures(monthly, annual, anomalies, holdout, decomposition, out/"figures")
    write_report(out/"report.md", monthly, annual, quality, trend, anomalies, metrics)
    return {"monthly":monthly,"annual":annual,"climatology":climatology,"trend":trend,
            "quality":quality,"anomalies":anomalies,"decomposition":decomposition,
            "metrics":metrics,"holdout":holdout}
