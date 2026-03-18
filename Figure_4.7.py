import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. FILE PATHS (100mm Rainfall Scenario)
# ==========================================
path_r_fair = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_fair.xlsx"
path_f_good = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_good.xlsx"
path_f_fair = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_fair.xlsx"
path_f_poor = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_poor.xlsx"

def extract_peak(file_path, sheet_name):
    """Targets Column C and pulls the MAX value (the Peak)."""
    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 2], names=["Name", "Peak"])
    
    df_clean = df.dropna(subset=['Name'])
    exclude = 'Total|Global|Sink|Reach|Junction'
    df_subbasins = df_clean[~df_clean['Name'].astype(str).str.contains(exclude, case=False, na=False)]
    
    # .max() ensures we are getting the PEAK
    peak_val = pd.to_numeric(df_subbasins["Peak"], errors='coerce').max()
    return peak_val

# ==========================================
# 2. DATA EXTRACTION
# ==========================================
# Rossano Baseline
ross_fair_pre = extract_peak(path_r_fair, "500mm(PRE)")

f_good_pre  = extract_peak(path_f_good, "500mm(PRE)")
f_good_post = extract_peak(path_f_good, "500mm")

f_fair_pre  = extract_peak(path_f_fair, "500mm(PRE)")
f_fair_post = extract_peak(path_f_fair, "500mm")

f_poor_pre  = extract_peak(path_f_poor, "500mm(PRE)")
f_poor_post = extract_peak(path_f_poor, "500mm")

# ==========================================
# 3. PLOTTING THE VALIDATION GRAPH
# ==========================================
fig, ax = plt.subplots(figsize=(14, 7))

# Data Grouping
labels = ['Rossano\n(Fair)', 'Fiume\n(Good)', 'Fiume\n(Fair)', 'Fiume\n(Poor)']
pre_peaks = [ross_fair_pre, f_good_pre, f_fair_pre, f_poor_pre]
post_peaks = [0, f_good_post, f_fair_post, f_poor_post]

x = np.arange(len(labels))
width = 0.35

# Plotting Bars
# Rossano Fair Pre-Fire (Hatched Orange)
ax.bar(x[0], pre_peaks[0], width*2, color='#fdae61', hatch='///', edgecolor='black', label='Rossano (Fair Pre-Fire)')

# Fiume Pre-Fire Baselines (Grey)
ax.bar(x[1:] - width/2, pre_peaks[1:], width, color='#d9d9d9', edgecolor='black', label='Fiume Nica (Pre-Fire)')

# Fiume Post-Fire Scenarios (Specific Colors)
ax.bar(x[1] + width/2, post_peaks[1], width, color='#2d4f4f', edgecolor='black', label='Fiume Post-Fire (Good)')
ax.bar(x[2] + width/2, post_peaks[2], width, color='#66c2a5', edgecolor='black', label='Fiume Post-Fire (Fair)')
ax.bar(x[3] + width/2, post_peaks[3], width, color='#f08080', edgecolor='black', label='Fiume Post-Fire (Poor)')

# VALIDATION LINE (Updated to reflect critical analysis)
arpacal_benchmark = 97
ax.axhline(y=arpacal_benchmark, color='blue', linestyle='--', linewidth=2, label=f'ARPACAL Benchmark ({arpacal_benchmark} m³/s)')
ax.text(3.4, arpacal_benchmark + 1.5, f'ARPACAL Benchmark ({arpacal_benchmark} m³/s)', color='blue', fontweight='bold', ha='right')

# Adding the Peak Value Labels on top
for i in range(len(labels)):
    if pre_peaks[i] > 0:
        pos_x = i if i == 0 else i - width/2
        ax.text(pos_x, pre_peaks[i] + 1, f'{pre_peaks[i]:.1f}', ha='center', fontweight='bold')
    if post_peaks[i] > 0:
        ax.text(i + width/2, post_peaks[i] + 1, f'{post_peaks[i]:.1f}', ha='center', fontweight='bold')

# Formatting
ax.set_ylabel('Peak Discharge ($m^3/s$)', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontweight='bold')
ax.set_ylim(0, 115)
ax.grid(axis='y', linestyle=':', alpha=0.5)

# Legend
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, edgecolor='black')

plt.tight_layout()
plt.show()
