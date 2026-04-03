#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[20]:


import sys
get_ipython().system('{sys.executable} -m pip install lightkurve')


# In[2]:


import lightkurve as lk
import matplotlib.pyplot as plt

search = lk.search_lightcurve("Kepler-10", author="Kepler", cadence="long")
print(search)


# In[3]:


lc_list = []
for i in range(3):
    try:
        lc_list.append(search[i].download())
        print(f"Quarter {i} downloaded successfully")
    except Exception as e:
        print(f"Quarter {i} failed: {e}")

lc_collection = lk.LightCurveCollection(lc_list)
lc = lc_collection.stitch()
print("Stitch complete. Total points:", len(lc))


# In[4]:


lc_clean = lc.remove_nans().remove_outliers().flatten(window_length=401)
lc_clean.plot()
plt.title("Kepler-10 — 3 Quarters Cleaned")
plt.show()
print("Clean points:", len(lc_clean))


# In[5]:


periodogram = lc_clean.to_periodogram(method="bls", period=[0.5, 2])
periodogram.plot()
plt.title("BLS Periodogram - Kepler-10")
plt.show()

best_period = periodogram.period_at_max_power
t0 = periodogram.transit_time_at_max_power

print("Best period:", best_period)
print("Transit time:", t0)


# In[6]:


search2 = lk.search_lightcurve("Kepler-17", author="Kepler", cadence="long")
lc2 = search2[0].download()
lc2_clean = lc2.remove_nans().remove_outliers().flatten(window_length=401)

periodogram2 = lc2_clean.to_periodogram(method="bls", period=[0.5, 5])
periodogram2.plot()
plt.title("BLS Periodogram - Kepler-17")
plt.show()

best_period2 = periodogram2.period_at_max_power
t02 = periodogram2.transit_time_at_max_power
print("Best period:", best_period2)


# In[7]:


search2 = lk.search_lightcurve("Kepler-17", author="Kepler", cadence="long")
lc2 = search2[0].download()

# Less aggressive flattening
lc2_clean = lc2.remove_nans().remove_outliers().flatten(window_length=1001)

# Narrower search targeting known period range
periodogram2 = lc2_clean.to_periodogram(method="bls", period=[1.0, 2.0])
periodogram2.plot()
plt.title("BLS Periodogram - Kepler-17 (revised)")
plt.show()

best_period2 = periodogram2.period_at_max_power
t02 = periodogram2.transit_time_at_max_power
print("Best period:", best_period2)


# In[8]:


# Force search exactly around Kepler-17b known period of 1.486 days
periodogram3 = lc2_clean.to_periodogram(method="bls", period=[1.4, 1.6])
periodogram3.plot()
plt.title("BLS Periodogram - Kepler-17 (tight range)")
plt.show()

best_period3 = periodogram3.period_at_max_power
t03 = periodogram3.transit_time_at_max_power
print("Best period:", best_period3)


# In[9]:


# Download PDCSAP flux - already corrected by Kepler pipeline
search2 = lk.search_lightcurve("Kepler-17", author="Kepler", cadence="long")
lc2 = search2[0].download()

# Use PDCSAP instead of SAP
lc2_pdcsap = lc2.select_flux("pdcsap_flux").remove_nans().remove_outliers().flatten(window_length=1001)

lc2_pdcsap.plot()
plt.title("Kepler-17 PDCSAP Flux")
plt.show()

periodogram4 = lc2_pdcsap.to_periodogram(method="bls", period=[1.0, 2.0])
periodogram4.plot()
plt.title("BLS Periodogram - Kepler-17 PDCSAP")
plt.show()

best_period4 = periodogram4.period_at_max_power
print("Best period:", best_period4)


# In[10]:


# Flatten more aggressively to remove stellar variability
lc2_flat = lc2.select_flux("pdcsap_flux").remove_nans().remove_outliers().flatten(window_length=101)

lc2_flat.plot()
plt.title("Kepler-17 Flattened")
plt.show()

periodogram5 = lc2_flat.to_periodogram(method="bls", period=[1.0, 2.0])
periodogram5.plot()
plt.title("BLS Periodogram - Kepler-17 Flattened")
plt.show()

best_period5 = periodogram5.period_at_max_power
t05 = periodogram5.transit_time_at_max_power
print("Best period:", best_period5)


# In[11]:


# Fold at known Kepler-17b period
folded5 = lc2_flat.fold(period=1.4857)
folded5.scatter()
plt.title("Folded Light Curve - Kepler-17b (known period)")
plt.show()

ax = folded5.scatter()
ax.set_xlim(-0.1, 0.1)
plt.title("Zoomed Transit - Kepler-17b")
plt.show()


# In[12]:


# Find correct epoch by folding and identifying dip center
folded6 = lc2_flat.fold(period=1.4857)

# Transit appears near phase -0.2, which is about -0.2 * 1.4857 = -0.297 days offset
# Correct the epoch
t0_corrected = t05 - 0.2 * 1.4857

folded6_corrected = lc2_flat.fold(period=1.4857, epoch_time=t0_corrected)
folded6_corrected.scatter()
plt.title("Folded Light Curve - Kepler-17b (epoch corrected)")
plt.show()

ax = folded6_corrected.scatter()
ax.set_xlim(-0.1, 0.1)
plt.title("Zoomed Transit - Kepler-17b (centered)")
plt.show()


# In[13]:


periodogram_hires = lc2_flat.to_periodogram(
    method="bls",
    period=[0.5, 2],
    frequency_factor=20
)

periodogram_hires.plot()
plt.title("High-Resolution BLS Periodogram - Kepler-17")
plt.show()

best_period_hires = periodogram_hires.period_at_max_power
print("Best period:", best_period_hires)


# In[14]:


import numpy as np

depth = float(1 - np.min(folded6_corrected.flux))

idx = int(np.argmin(folded6_corrected.flux))
transit_mask = folded6_corrected.flux < (1 - depth * 0.5)
if transit_mask.sum() > 1:
    duration = float(folded6_corrected.time[transit_mask].max().value -
                     folded6_corrected.time[transit_mask].min().value)
else:
    duration = 0.0
print("Transit depth:", round(depth, 5))
print("Transit duration:", round(duration, 5), "days")


# In[15]:


planets = [
    "Kepler-5", "Kepler-6", "Kepler-7", "Kepler-8",
    "Kepler-10", "Kepler-12", "Kepler-13", "Kepler-17",
    "Kepler-18", "Kepler-20"
]
planets += ["Kepler-4", "Kepler-41", "Kepler-44", "Kepler-45"]


# In[16]:


non_transits = [
    "KIC 757076", "KIC 8435766", "KIC 10028792",
    "KIC 1026957", "KIC 11446443", "KIC 10963065",
    "KIC 11395018", "KIC 8394589", "KIC 9098294",
    "KIC 9955598"
]
non_transits += [
    "KIC 3733735", "KIC 4914423", "KIC 5184732",
    "KIC 6521045", "KIC 7199397", "KIC 7871531",
    "KIC 8006161", "KIC 8228742", "KIC 9139151",
    "KIC 9410862", "KIC 10016239", "KIC 10454113",
    "KIC 11253226", "KIC 12009504", "KIC 3427720"
]


# In[17]:


import pandas as pd
import numpy as np

known_periods = {
    "Kepler-5":  3.5485,
    "Kepler-6":  3.2347,
    "Kepler-7":  4.8855,
    "Kepler-8":  3.5225,
    "Kepler-10": 0.8375,
    "Kepler-12": 4.4380,
    "Kepler-13": 1.7636,
    "Kepler-17": 1.4857,
    "Kepler-18": 3.5047,
    "Kepler-20": 3.6961,
    "Kepler-4":  3.2135,
    "Kepler-41": 1.8556,
    "Kepler-44": 3.2469,
    "Kepler-45": 2.4554,
}

REFERENCE_PERIOD = 2.0

def extract_features(target):
    try:
        search = lk.search_lightcurve(target, author="Kepler", cadence="long")
        lc = search[:2].download_all().stitch()
        lc_clean = lc.remove_nans().remove_outliers().flatten(window_length=401).normalize()

        if target in known_periods:
            period = known_periods[target]
        else:
            period = REFERENCE_PERIOD

        folded = lc_clean.fold(period=period)

        depth = float(1 - np.min(folded.flux))
        idx = int(np.argmin(folded.flux))

        # --- improved duration ---
        try:
            flux = folded.flux.value
            time = folded.time.value
            window = 7
            flux_smooth = np.convolve(flux, np.ones(window)/window, mode='same')
            idx_min = int(np.argmin(flux_smooth))
            flux_min = flux_smooth[idx_min]
            baseline = np.median(flux_smooth)
            half_level = baseline - (baseline - flux_min) / 2

            left = idx_min
            while left > 0 and flux_smooth[left] < half_level:
                left -= 1

            right = idx_min
            while right < len(flux_smooth) - 1 and flux_smooth[right] < half_level:
                right += 1

            duration = float(time[right] - time[left])
            if duration <= 0 or duration > 1.0:
                duration = np.nan

        except:
            duration = np.nan

        # --- SNR ---
        try:
            transit_mask = folded.flux.value < (1 - depth / 2)
            out_of_transit = folded.flux.value[~transit_mask]
            if len(out_of_transit) > 10:
                noise_std = np.std(out_of_transit)
            else:
                noise_std = np.std(folded.flux.value)
            snr = float(depth / noise_std) if noise_std > 0 else 0.0
        except:
            snr = 0.0

        print(f"{target}: depth={round(depth,5)}, duration={round(duration,5) if not np.isnan(duration) else 'NaN'}, snr={round(snr,2)}")
        return depth, duration, snr

    except Exception as e:
        print(f"Error with {target}: {e}")
        return None, None, None

rows = []

for t in planets:
    depth, duration, snr = extract_features(t)
    if depth is not None:
        rows.append([t, depth, duration, snr, 1])

for t in non_transits:
    depth, duration, snr = extract_features(t)
    if depth is not None:
        rows.append([t, depth, duration, snr, 0])

df_real = pd.DataFrame(rows, columns=["target", "depth", "duration", "snr", "label"])
print("\n", df_real)
print("\nSNR stats by class:")
print(df_real.groupby("label")["snr"].describe())


# In[25]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df_model = df_real[
    df_real["target"] != "Kepler-17"
].copy()

X = df_model[["depth", "snr"]]
y = df_model["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model_real = RandomForestClassifier(random_state=42)
model_real.fit(X_train, y_train)

pred_real = model_real.predict(X_test)
print("Test size:", len(X_test))
print(classification_report(y_test, pred_real))
print("Feature importances:")
print("depth:", round(model_real.feature_importances_[0], 3))
print("snr:", round(model_real.feature_importances_[1], 3))
print("Note: exploratory result due to dataset size.")
print("\nTargets used in model:", len(df_model))
print("Excluded (Kepler-17 outlier):", len(df_real) - len(df_model))

from sklearn.model_selection import cross_val_score

scores = cross_val_score(model_real, X, y, cv=5)
print("CV accuracy:", round(scores.mean(), 3))


# In[19]:


import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 5))
labels_used = []

for _, row in df_real.iterrows():
    color = "steelblue" if row["label"] == 1 else "tomato"
    label = "Planet" if row["label"] == 1 else "Non-transit"
    if label not in labels_used:
        ax.scatter(row["depth"], row["duration"],
                   color=color, label=label, s=80, zorder=3)
        labels_used.append(label)
    else:
        ax.scatter(row["depth"], row["duration"],
                   color=color, s=80, zorder=3)

ax.set_xlabel("Transit Depth")
ax.set_ylabel("Transit Duration (days)")
ax.set_title("Feature Space: Planets vs. Non-Transits")
ax.legend()
plt.tight_layout()
plt.show()


# In[23]:


plt.figure(figsize=(7,5))

plt.scatter(planets["depth"], planets["snr"],
            s=70, alpha=0.85, label="Planets")

plt.scatter(non["depth"], non["snr"],
            s=70, alpha=0.85, label="Non-transits")

plt.xlabel("Transit Depth")
plt.ylabel("SNR")
plt.title("Depth vs SNR (Kepler Data)")

plt.legend(frameon=False)
plt.grid(alpha=0.1)

plt.tight_layout()
plt.savefig("plots/depth_vs_snr.png", dpi=300)
plt.show()


# In[ ]:




