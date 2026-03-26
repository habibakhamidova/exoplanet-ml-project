# Exoplanet Transit Detection (Kepler Data)

This project analyzes Kepler light curve data to detect exoplanet transits.

## What was done
- Tested BLS (Box Least Squares) period detection
- Demonstrated BLS failure on noisy real data
- Extracted features: transit depth and duration
- Built ML classifier (Random Forest)
- Achieved 83% accuracy on real NASA targets

## Key insight
BLS fails on short/noisy datasets, while simple ML features can partially recover signal.

## Files
- notebook.ipynb — full pipeline
