# Exoplanet Transit Detection (Kepler Data)

Independent project exploring limitations of classical exoplanet detection methods on real Kepler light curve data.

## Overview

This project analyzes Kepler light curve data to detect exoplanet transits and evaluate the reliability of the Box Least Squares (BLS) algorithm on real, noisy datasets.

## What was done

- Tested BLS (Box Least Squares) period detection under multiple configurations  
- Observed consistent BLS failure on noisy real data despite visible transit signals  
- Extracted features: transit depth and duration  
- Built a Random Forest classifier  
- Achieved 83% accuracy on a held-out set of real NASA targets  

## Key insight

BLS failed to recover correct periods on short/noisy Kepler datasets, even when transit signals were visually present. A simple ML model partially recovered the signal, but performance was limited by feature overlap between shallow transits and stellar variability.

## Limitations

- Small dataset (20 targets)  
- Only two features used (depth and duration)  
- No confirmed false positives (e.g., eclipsing binaries)  
- Duration estimation is approximate

## Files
- notebook.ipynb -> full pipeline

## How to run

```bash
pip install lightkurve numpy pandas scikit-learn matplotlib

Run:
notebook.ipynb
