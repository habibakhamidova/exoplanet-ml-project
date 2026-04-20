# BLS Period Recovery Failure and Feature-Based Transit Classification (Kepler Data)

This project investigates a specific failure mode of the Box Least Squares (BLS) algorithm under short-baseline Kepler conditions, and evaluates whether simple photometric features can partially compensate for this limitation.

## Key Findings

- BLS fails to recover correct orbital periods using limited data (2 quarters, 0.5 to 5 day search range)
- Simple features (transit depth and SNR) achieve:
  - **0.92 hold-out accuracy**
  - **0.77 cross-validation accuracy**
- Strong overlap between planets and non-transit stars
- Indicates a **fundamental detection limitation**

## Important Note

This model does NOT perform transit detection.
It evaluates features extracted at known orbital periods (for confirmed planets) and fixed reference periods (for non-transit stars). The goal is to study feature separability under conditions where traditional period recovery methods fail.

## Dataset

- 14 confirmed Kepler planets
- 25 non-transit stars (KIC)
- Total: 39 targets
- Excluded from training: Kepler-17 (outlier)

## Features

- Transit depth
- Signal-to-noise ratio (SNR)

## Results

| Metric | Value |
|------|------|
| Accuracy (hold-out) | 0.92 |
| Accuracy (5-fold CV) | 0.77 |
| Precision (planets) | 1.00 |
| Recall (planets) | 0.67 |
| F1-score (planets) | 0.80 |

## Repository Structure

- `notebooks/` for data analysis and experiments
- `paper.pdf` for the full research note
- `README.md` for project overview

## Tech Stack

- Python
- Lightkurve
- Scikit-learn
- NumPy
- Pandas
- Matplotlib

## Goal

To understand real-world limitations of period-based detection methods and evaluate simple feature-based classification under noisy conditions.
