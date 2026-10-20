"""Command-line entry point."""
import argparse
from pathlib import Path
from src.config import DEFAULT_INPUT, DEFAULT_OUTPUT
from src.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Run Climate Trend Analyzer.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="CSV containing date, temperature, optional precipitation.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Directory for outputs.")
    args = parser.parse_args()
    result = run_pipeline(args.input, args.output)
    print("Analysis complete.")
    print(f"Monthly observations: {len(result['monthly'])}")
    print(f"Coverage: {result['monthly'].date.min().date()} to {result['monthly'].date.max().date()}")
    print(f"Exploratory trend: {result['trend']['slope_c_per_decade']:.4f} °C/decade")
    if not result["metrics"].empty: print(result["metrics"].to_string(index=False))
    print(f"Results saved to: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
