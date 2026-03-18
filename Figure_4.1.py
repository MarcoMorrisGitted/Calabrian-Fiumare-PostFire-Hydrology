import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# ==========================================
# 1. FILE PATHS & SETUP
# ==========================================
path_good = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_good.xlsx"
path_fair = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_fair.xlsx"
path_poor = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_poor.xlsx"

cols = ["Subbasin", "Area", "Peak_Discharge", "Time", "Vol"]

# ==========================================
# 2. PEAK SEARCH EXTRACTION FUNCTION
# ==========================================
def extract_validation_peak(file_path, sheet_name):
    """
    Scans Column C to find the maximum subbasin peak.
    Filters out the Global Total row to identify the primary stream outlet.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0,1,2,3,4], names=cols)
    df_clean = df.dropna(subset=['Subbasin'])
    
    # Identify and remove the HEC-HMS Global 'Total' or 'Sink' rows
    # This leaves only the individual subbasin peaks
    exclude = 'Total|Global|Sink'
    df_subbasins = df_clean[~df_clean['Subbasin'].astype(str).str.contains(exclude, case=False, na=False)]
    
    # Search for the highest peak discharge value within the subbasin list
    peaks = pd.to_numeric(df_subbasins["Peak_Discharge"], errors='coerce')
    return peaks.max()

# ==========================================
# 3. DATA PROCESSING
# ==========================================
print("Searching datasets for localized peak discharge values...")

# Extract Pre-Fire (Baseline)
pre_100 = [extract_validation_peak(path_good, "100mm(PRE)"), extract_validation_peak(path_fair, "100mm(PRE)"), extract_validation_peak(path_poor, "100mm(PRE)")]
pre_230 = [extract_validation_peak(path_good, "230mm(PRE)"), extract_validation_peak(path_fair, "230mm(PRE)"), extract_validation_peak(path_poor, "230mm(PRE)")]
pre_500 = [extract_validation_peak(path_good, "500mm(PRE)"), extract_validation_peak(path_fair, "500mm(PRE)"), extract_validation_peak(path_poor, "500mm(PRE)")]

# Extract Post-Fire
post_100 = [extract_validation_peak(path_good, "100mm"), extract_validation_peak(path_fair, "100mm"), extract_validation_peak(path_poor, "100mm")]
post_230 = [extract_validation_peak(path_good, "230mm"), extract_validation_peak(path_fair, "230mm"), extract_validation_peak(path_poor, "230mm")]
post_500 = [extract_validation_peak(path_good, "500mm"), extract_validation_peak(path_fair, "500mm"), extract_validation_peak(path_poor, "500mm")]

# ==========================================
# 4. FIGURE 4.1 GENERATION
# ==========================================
labels = ['Good', 'Fair', 'Poor']
x = np.arange(len(labels))
width = 0.35  

fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
# Title removed as requested

scenarios = [
    (pre_100, post_100, '100mm Scenario'),
    (pre_230, post_230, '230mm Scenario'),
    (pre_500, post_500, '500mm Scenario')
]

post_colors = ['#66c2a5', '#ffcc99', '#f08080'] 

for i, ax in enumerate(axes):
    pre_vals, post_vals, title = scenarios[i]
    
    rects1 = ax.bar(x - width/2, pre_vals, width, label='Pre-Fire (Baseline)', color='lightgrey', edgecolor='black')
    rects2 = ax.bar(x + width/2, post_vals, width, color=post_colors, edgecolor='black')
    
    # Add the 97.0 m3/s ARPACAL Estimate line
    ax.axhline(y=97.0, color='blue', linestyle='--', linewidth=2.5)

    ax.set_title(title, fontsize=15, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_ylim(0, 160) 

    for rect in rects1 + rects2:
        height = rect.get_height()
        if pd.notna(height) and height > 0:
            ax.annotate(f'{height:.1f}', 
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10)

axes[0].set_ylabel('Peak Discharge ($m^3/s$)', fontsize=13)

# ==========================================
# 5. LEGEND
# ==========================================
legend_elements = [
    Line2D([0], [0], color='blue', lw=2.5, linestyle='--', label='ARPACAL Estimate (97.0 m³/s)'),
    Patch(facecolor='lightgrey', edgecolor='black', label='Pre-Fire (Baseline)'),
    Patch(facecolor='#66c2a5', edgecolor='black', label='Post-Fire (Good)'),
    Patch(facecolor='#ffcc99', edgecolor='black', label='Post-Fire (Fair)'),
    Patch(facecolor='#f08080', edgecolor='black', label='Post-Fire (Poor)')
]
axes[0].legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=1, edgecolor='black')

plt.tight_layout() 
plt.show()
