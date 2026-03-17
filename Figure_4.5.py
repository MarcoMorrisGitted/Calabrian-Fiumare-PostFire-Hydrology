import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

# =================================================================
# 1. FILE PATHS & COLORS
# =================================================================
FILES = {
    'Fiume 2024': {
        'Good': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_good.xlsx",
        'Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_fair.xlsx",
        'Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_poor.xlsx"
    },
    'Fiume 2025': {
        'Good': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_good.xlsx",
        'Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_fair.xlsx",
        'Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_poor.xlsx"
    },
    'Rossano 2017': {
        'Good': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_good.xlsx",
        'Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_fair.xlsx",
        'Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_poor.xlsx"
    }
}

BASINS = ['Fiume 2024', 'Fiume 2025', 'Rossano 2017']
CONDITIONS = ['Good', 'Fair', 'Poor']
EVENTS = ['100mm', '230mm', '500mm']
COLORS = {'Good': '#66C2A4', 'Fair': '#FDE0C5', 'Poor': '#F08080'}

# =================================================================
# 2. DATA EXTRACTION (ACTUAL VALUES)
# =================================================================
def get_actual_volume(filepath, sheet_name):
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        # Sum Column E (index 4) - RAW VALUE from subbasins
        val = pd.to_numeric(df.iloc[:, 4], errors='coerce').sum()
        return val
    except Exception:
        return 0.0

# =================================================================
# 3. PLOTTING
# =================================================================
def generate_fixed_scale_chart():
    plt.rcParams.update({'font.weight': 'normal', 'font.size': 10})
    # sharey=True ensures all three charts use the same 0-100,000 scale
    fig, axes = plt.subplots(1, 3, figsize=(22, 10), sharey=True)
    
    x = np.arange(len(BASINS))
    width = 0.12 

    for i, event in enumerate(EVENTS):
        ax = axes[i]
        for j, cond in enumerate(CONDITIONS):
            post_vols = [get_actual_volume(FILES[b][cond], event) for b in BASINS]
            pre_vols = [get_actual_volume(FILES[b][cond], event + "(PRE)") for b in BASINS]
            
            # Position offsets for side-by-side grouped bars
            pre_pos = x + (j - 1.5) * (width * 2.2)
            post_pos = pre_pos + width
            
            # Pre-Fire: Hatched
            ax.bar(pre_pos, pre_vols, width, color=COLORS[cond], alpha=0.4, 
                   edgecolor='black', hatch='//', label=f'{cond} (Pre)')
            
            # Post-Fire: Solid
            ax.bar(post_pos, post_vols, width, color=COLORS[cond], 
                   edgecolor='black', label=f'{cond} (Post)')

        ax.set_title(event + " Event", fontsize=16, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(BASINS, fontsize=11)
        ax.grid(axis='y', linestyle=':', alpha=0.5)
        
        # FORMAT Y-AXIS WITH COMMAS
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    # SET FIXED SCALE TO 100,000
    axes[0].set_ylim(0, 100000)
    axes[0].set_ylabel('Total Volume ($m^3$)', fontsize=14)

    # Clean Legend
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles[:6], labels[:6], loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05))

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.show()

if __name__ == "__main__":
    generate_fixed_scale_chart()