"""Synthetic data generator. This output is simulated, not observed climate."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from .config import RANDOM_SEED


def generate_synthetic_data(output_path="data/synthetic_climate_data.csv",
                            start="1980-01-01", end="2025-12-01", seed=RANDOM_SEED):
    dates = pd.date_range(start, end, freq="MS")
    if len(dates) < 24:
        raise ValueError("At least 24 monthly records are required.")
    rng = np.random.default_rng(seed)
    month = dates.month.to_numpy()
    elapsed = (dates.year.to_numpy() - dates.year.min()) + (month - 1) / 12
    temperature = 25 + 5.5*np.sin(2*np.pi*(month-4)/12) + 0.025*elapsed + rng.normal(0, .75, len(dates))
    for index, delta in [(150, 4), (280, -3.5), (410, 4.5), (500, -4)]:
        if index < len(temperature):
            temperature[index] += delta
    precipitation = np.maximum(0, 85 + 50*np.sin(2*np.pi*(month-6)/12) + rng.normal(0, 22, len(dates)))
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"),
                       "temperature": temperature.round(3),
                       "precipitation": precipitation.round(2)})
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/synthetic_climate_data.csv")
    parser.add_argument("--start", default="1980-01-01")
    parser.add_argument("--end", default="2025-12-01")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    args = parser.parse_args()
    df = generate_synthetic_data(args.output, args.start, args.end, args.seed)
    print(f"Wrote {len(df)} synthetic monthly records to {args.output}")


if __name__ == "__main__":
    main()
