# Exoplanet Transit Detection — Kepler Data

## Overview
This project evaluates whether simple features derived from Kepler light curves can distinguish transiting exoplanets from non-transit stars.

## Dataset
- 38 targets total
  - Confirmed exoplanets (Kepler catalog)
  - Non-transit stars (KIC)
- Light curves: Kepler long cadence (2 quarters)

## Preprocessing
- Removed NaNs and outliers  
- Flattened light curves (window=401)  
- Normalized flux  

## Methodology

### Period Handling
- Planets: known orbital periods (NASA archive)
- Non-transits: fixed reference period (2.0 days)

### Feature Extraction
- **Depth** — minimum flux drop  
- **SNR** — depth / noise standard deviation  

### Features Tested and Rejected
- **Duration** — unstable under threshold and smoothing methods  
- **Symmetry** — introduced noise and reduced model performance  

### Model
- Random Forest classifier  
- Train/test split: 70/30  
- Final features: **depth + SNR**

## Results
- Accuracy: **0.92**
- Recall (planets): **0.67**

Feature importance:
- Depth: 0.508  
- SNR: 0.492  

## Key Findings
- BLS often fails to recover correct orbital periods  
- Transit duration is not a stable feature under simple extraction  
- Depth + SNR provide partial separation  
- Significant overlap remains between classes  

## Conclusion
Simple feature-based approaches are insufficient for reliable transit detection. More advanced representations (e.g., shape modeling or time-series learning) are required.

## Repository Structure
- `notebook.ipynb` — full pipeline  
- `data/` — optional outputs  
- `plots/` — scatter plots  

## Author
Habiba Khamidova
