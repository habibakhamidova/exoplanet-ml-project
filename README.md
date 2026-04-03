# Exoplanet Transit Detection (Kepler Data)

This project evaluates the limitations of the Box Least Squares (BLS) algorithm on real Kepler light curve data under constrained conditions.

## Key Findings

- BLS fails to recover correct orbital periods using limited data (2 quarters, 0.5–5 day search range)
- Simple features (transit depth + SNR) achieve:
  - **0.92 hold-out accuracy**
  - **~0.77 cross-validation accuracy**
- Strong overlap between planets and non-transit stars:
  - Some non-transits reach higher SNR than confirmed planets
- Indicates a **fundamental detection limitation**

## Important Note

The model **does NOT detect transits**.

It evaluates features extracted at:
- known orbital periods (planets)
- fixed reference period (non-transits)

## Dataset

- 14 confirmed Kepler planets
- 25 non-transit stars (KIC)
- Total: 39 targets

## Features

- Transit depth
- Signal-to-noise ratio (SNR)

## Results

| Metric | Value |
|------|------|
| Accuracy (hold-out) | 0.92 |
| Accuracy (5-fold CV) | ~0.77 |
| Precision (planets) | 1.00 |
| Recall (planets) | 0.67 |

## Visualization

![Depth vs SNR](plots/depth_vs_snr.png)

## Paper

Full paper available: `paper.pdf`

## Tech Stack

- Python
- Lightkurve
- Scikit-learn
- NumPy / Pandas / Matplotlib

## Goal

To understand real-world limitations of period-based detection methods and evaluate simple feature-based classification under noisy conditions.
