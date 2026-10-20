# Climate Trend Analyzer 🌍📊
**Modular, end-to-end climate time-series analytics portfolio project**

This version is intentionally organized into multiple focused Python modules instead of concentrating nearly all logic in one file. It includes data generation, ingestion, validation, preprocessing, descriptive analysis, trend estimation, anomaly screening, STL decomposition, forecasting/model evaluation, visualization, report generation, a CLI, a Streamlit dashboard, and tests.

> The included dataset is synthetic and for software demonstration only. It is not observed climate evidence or an official climate forecast.

## Quick start (Windows)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run_analysis.py
pytest -q
streamlit run app.py
```

## CLI examples
```bash
python run_analysis.py
python run_analysis.py --input data/synthetic_climate_data.csv --output outputs/demo
python -m src.data_generator --output data/synthetic_climate_data.csv --start 1990-01-01 --end 2025-12-01
```

## Folder map
```text
Climate_Trend_Analyzer_Professional/
├── app.py
├── run_analysis.py
├── requirements.txt
├── data/
├── docs/
├── outputs/
├── src/
│   ├── config.py
│   ├── data_generator.py
│   ├── data_loader.py
│   ├── data_quality.py
│   ├── preprocessing.py
│   ├── descriptive_analysis.py
│   ├── trend_analysis.py
│   ├── anomaly_detection.py
│   ├── decomposition.py
│   ├── forecasting.py
│   ├── visualization.py
│   ├── reporting.py
│   └── pipeline.py
└── tests/
```

## Features
- Synthetic dataset generator with fixed random seed
- CSV schema validation and monthly aggregation
- Data quality report (invalid rows, duplicate dates, missing months)
- Annual summaries and monthly climatology
- OLS trend slope, p-value, R², approximate interval
- Calendar-month anomalies and robust modified-z-score flags
- STL seasonal decomposition when continuous monthly data are available
- Seasonal-naive and Random Forest lag-feature holdout evaluation
- MAE, RMSE, R² and forecast comparison charts
- Dashboard with date filters, CSV upload and download
- Automated report, CSV/JSON artifacts, unit tests, methodology and interview guide

## Use a public dataset
The CSV loader expects `date`, `temperature`, and optional `precipitation` columns. Document provider, exact URL, retrieval date, license/terms, geographic coverage, units, missing codes, and transformations in `docs/DATA_PROVENANCE_TEMPLATE.md` before publishing real-world findings.

Potential sources to investigate:
- NASA GISTEMP: https://data.giss.nasa.gov/gistemp/
- NOAA Climate Data Online: https://www.ncei.noaa.gov/cdo-web/
- Berkeley Earth: https://berkeleyearth.org/data/
- India Meteorological Department: https://mausam.imd.gov.in/

## Scientific cautions
OLS trend inference may be unreliable under serial correlation. An anomaly flag is not proof of bad data or a climate event. A single chronological holdout is a demonstration, not robust validation. Synthetic results must never be described as observed climate findings.
