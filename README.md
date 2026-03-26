# Exoplanet Transit Detection (Kepler Data)
Independent project exploring limitations of classical exoplanet detection methods on real Kepler data.

This project analyzes Kepler light curve data to detect exoplanet transits.

## What was done
- Tested BLS (Box Least Squares) period detection
- Demonstrated BLS failure on noisy real data
- Extracted features: transit depth and duration
- Built ML classifier (Random Forest)
- Achieved 83% accuracy on real NASA targets

## Key insight
BLS failed to recover correct periods on short/noisy Kepler datasets, even when transit signals were visually present. A simple ML model partially recovered the signal, but performance was limited by feature overlap between shallow transits and stellar variability.

## Limitations
- Small dataset (20 targets)
- Only two features used (depth and duration)
- No confirmed false positives (e.g., eclipsing binaries)
- Duration estimation is approximate

## How to Run

pip install lightkurve numpy pandas scikit-learn matplotlib

Run:
notebook.ipynb

## Files
- notebook.ipynb -> full pipeline
