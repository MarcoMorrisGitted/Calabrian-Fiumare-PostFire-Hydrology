import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# 1. FILE PATHS
path_good = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_good.xlsx"
path_fair = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_fair.xlsx"
path_poor = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_poor.xlsx"

cols = ["Subbasin", "Area", "Peak_Discharge", "Time", "Vol"]

def extract_scenario_peak(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0,1,2,3,4], names=cols)
    df_clean = df.dropna(subset=['Subbasin'])
    exclude = 'Total|Global|Sink|Reach|Junction'
    df_subbasins = df_clean[~df_clean['Subbasin'].astype(str).str.contains(exclude, case=False, na=False)]
    peaks = pd.to_numeric(df_subbasins["Peak_Discharge"], errors='coerce')
    return peaks.max()

# Data Extraction
pre_100 = [extract_scenario_peak(path_good, "100mm(PRE)"), extract_scenario_peak(path_fair, "100mm(PRE)"), extract_scenario_peak(path_poor, "100mm(PRE)")]
post_100 = [extract_scenario_peak(path_good, "100mm"), extract_scenario_peak(path_fair, "100mm"), extract_scenario_peak(path_poor, "100mm")]
pre_230 = [extract_scenario_peak(path_good, "230mm(PRE)"), extract_scenario_peak(path_fair, "230mm(PRE)"), extract_scenario_peak(path_poor, "230mm(PRE)")]
post_230 = [extract_scenario_peak(path_good, "230mm"), extract_scenario_peak(path_fair, "230mm"), extract_scenario_peak(path_poor, "230mm")]
pre_500 = [extract_scenario_peak(path_good, "500mm(PRE)"), extract_scenario_peak(path_fair, "500mm(PRE)"), extract_scenario_peak(path_poor, "500mm(PRE)")]
post_500 = [extract_scenario_peak(path_good, "500mm"), extract_scenario_peak(path_fair, "500mm"), extract_scenario_peak(path_poor, "500mm")]

# 2. PLOT GENERATION
labels = ['Good', 'Fair', 'Poor']
x = np.arange(len(labels))
width = 0.35  

fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
fig.suptitle('Fiumenicà 2025: Pre vs Post-Fire Peak Discharge', fontsize=18, fontweight='bold', y=0.98)

scenarios = [(pre_100, post_100, '100mm Scenario'), (pre_230, post_230, '230mm Scenario'), (pre_500, post_500, '500mm Scenario')]
post_colors = ['#66c2a5', '#ffcc99', '#f08080'] 

for i, ax in enumerate(axes):
    pre_vals, post_vals, title = scenarios[i]
    rects1 = ax.bar(x - width/2, pre_vals, width, label='Pre-Fire', color='lightgrey', edgecolor='black')
    rects2 = ax.bar(x + width/2, post_vals, width, color=post_colors, edgecolor='black')
    
    ax.set_title(title, fontsize=15, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    
    # ADD NUMBERS ON TOP
    for rect in rects1 + rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

axes[0].set_ylabel('Peak Discharge ($m^3/s$)', fontsize=13)

# 3. LEGEND
legend_elements = [
    Patch(facecolor='lightgrey', edgecolor='black', label='Pre-Fire (Baseline)'),
    Patch(facecolor='#66c2a5', edgecolor='black', label='Post-Fire (Good)'),
    Patch(facecolor='#ffcc99', edgecolor='black', label='Post-Fire (Fair)'),
    Patch(facecolor='#f08080', edgecolor='black', label='Post-Fire (Poor)')
]
axes[0].legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=1, edgecolor='black')

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.show()