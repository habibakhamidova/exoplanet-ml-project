# Results

## Dataset

- Total targets: 39  
- Planets: 14  
- Non-transit stars: 25  
- Excluded: Kepler-17 (outlier)

---

## Model Setup

- Features: **depth, SNR**
- Model: Random Forest
- Split: 70 / 30
- Test size: 12

---

## Performance

| Metric | Value |
|------|------|
| Accuracy (hold-out) | 0.92 |
| Accuracy (5-fold CV) | 0.77 |
| Precision (planets) | 1.00 |
| Recall (planets) | 0.67 |
| F1-score (planets) | 0.80 |

---

## Feature Importance

| Feature | Importance |
|--------|-----------|
| Depth | 0.508 |
| SNR | 0.492 |

---

## Key Observation

There is **significant overlap** between planets and non-transit stars:

- Max SNR (non-transit): **12.06**
- Min SNR (planet): **4.59**

This overlap explains classification errors and indicates a **fundamental detection limitation**.

---

## Visualization

![Depth vs SNR](plots/depth_vs_snr.png)

---

## Notes

- Results are **exploratory** due to small dataset (n=38)
- Cross-validation shows reduced performance vs hold-out split
- Model does not perform transit detection — only evaluates extracted features
