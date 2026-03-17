import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# ==========================================
# 1. SETUP
# ==========================================
files = {
    '2017 Rossano': {
        'Good': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_good.xlsx",
        'Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_fair.xlsx",
        'Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_poor.xlsx"
    },
    '2024 Fiume': {
        'Good': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_good.xlsx",
        'Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_fair.xlsx",
        'Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_poor.xlsx"
    },
    '2025 Fiume': {
        'Good': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_good.xlsx",
        'Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_fair.xlsx",
        'Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_poor.xlsx"
    }
}

rainfalls = ['100mm', '230mm', '500mm']
soil_types = ['Good', 'Fair', 'Poor']
colors = ['#fde0dd', '#fa9fb5', '#c51b8a']

fig, axes = plt.subplots(1, 3, figsize=(22, 10), sharey=True)

# ==========================================
# 2. DATA EXTRACTION (STRICT MATCHING)
# ==========================================
for ax_idx, (catchment, categories) in enumerate(files.items()):
    ax = axes[ax_idx]
    ax.set_title(catchment, fontsize=16, fontweight='bold', pad=15)
    
    catchment_plot_data = []
    
    for rain in rainfalls:
        for soil in soil_types:
            path = categories[soil]
            
            # Read sheets
            df_pre = pd.read_excel(path, sheet_name=f"{rain}(PRE)", usecols=[0, 2], names=["Name", "Peak"])
            df_post = pd.read_excel(path, sheet_name=rain, usecols=[0, 2], names=["Name", "Peak"])
            
            # 1. Clean names to ensure matching works
            df_pre['Name'] = df_pre['Name'].astype(str).str.strip()
            df_post['Name'] = df_post['Name'].astype(str).str.strip()
            
            # 2. Filter out non-subbasins (Totals, Sinks, Reaches)
            exclude = 'Total|Global|Sink|Reach|Junction|Outlet'
            df_pre = df_pre[~df_pre['Name'].str.contains(exclude, case=False, na=False)].dropna()
            df_post = df_post[~df_post['Name'].str.contains(exclude, case=False, na=False)].dropna()
            
            # 3. STRICT INNER MERGE (Ensures we only compare the same subbasin)
            merged = pd.merge(df_pre, df_post, on="Name", suffixes=('_pre', '_post'))
            
            if not merged.empty:
                # % Increase = (Post - Pre) / Pre * 100
                perc = ((merged['Peak_post'] - merged['Peak_pre']) / merged['Peak_pre']) * 100
                # Filter out mathematical errors (Inf/NaN)
                perc = perc.replace([np.inf, -np.inf], np.nan).dropna()
                catchment_plot_data.append(perc.values)
            else:
                catchment_plot_data.append(np.array([]))

    # Positions for groups
    pos = [1, 2, 3, 5, 6, 7, 9, 10, 11]
    
    # 4. PLOTTING
    # Setting showfliers=True to match your original's blue dots
    bp = ax.boxplot(catchment_plot_data, positions=pos, widths=0.7, 
                    patch_artist=True, showfliers=False, zorder=3)

    for i, (data, patch) in enumerate(zip(catchment_plot_data, bp['boxes'])):
        patch.set_facecolor(colors[i % 3])
        patch.set_alpha(0.7)
        
        # Add the Jitter Dots (The individual subbasin points)
        if len(data) > 0:
            x_jit = np.random.normal(pos[i], 0.06, size=len(data))
            ax.scatter(x_jit, data, alpha=0.3, s=4, color='royalblue', zorder=2)
            
        plt.setp(bp['medians'][i], color='darkorange', linewidth=2)

    # Scale and Formatting
    ax.axhline(0, color='black', linewidth=1, zorder=1)
    ax.set_xticks([2, 6, 10])
    ax.set_xticklabels(rainfalls, fontsize=12)
    ax.set_ylim(-5, 350) # Matching your full range
    ax.grid(axis='y', linestyle=':', alpha=0.5)

axes[0].set_ylabel('% Increase in Peak Discharge', fontsize=14, fontweight='bold')
legend_elements = [Patch(facecolor=colors[i], label=f'{soil_types[i]} Soil', edgecolor='black') for i in range(3)]
fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.95), title="Soil Condition")

plt.tight_layout(rect=[0, 0, 0.95, 1])
plt.show()