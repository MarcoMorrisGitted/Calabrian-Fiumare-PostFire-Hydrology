# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

# =================================================================
# 1. FILE PATHS
# =================================================================
PATH_2017 = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Hydrographs_2017.xlsx"
PATH_2024 = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Hydrographs_2024.xlsx"
PATH_2025 = r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Hydrographs_2025.xlsx"

# =================================================================
# 2. HELPER FUNCTIONS
# =================================================================
def clean_plot_subplot(ax, df, date_idx, time_idx, val_idx, label, color, style='-', width=2, alpha=1.0):
    """
    Combines Date and Time to calculate cumulative hours and plots to a specific axis.
    """
    dates = pd.to_datetime(df.iloc[:, date_idx], errors='coerce')
    times = pd.to_timedelta(df.iloc[:, time_idx].astype(str), errors='coerce')
    combined_dt = dates + times
    
    start_time = combined_dt.min()
    hours_data = (combined_dt - start_time).dt.total_seconds() / 3600.0
    val_data = pd.to_numeric(df.iloc[:, val_idx], errors='coerce')
    
    temp_df = pd.DataFrame({'x': hours_data, 'y': val_data}).dropna()
    temp_df = temp_df.drop_duplicates(subset=['x']).sort_values(by='x')
    
    ax.plot(temp_df['x'], temp_df['y'], label=label, color=color, 
            linestyle=style, linewidth=width, alpha=alpha)

# =================================================================
# 3. MAIN CONSOLIDATED PLOTTING
# =================================================================
def generate_consolidated_figure():
    # Create 2 rows (Fair, Poor) and 3 columns (Rainfall Intensities)
    fig, axes = plt.subplots(2, 3, figsize=(20, 14), sharey=True)
    
    conditions = [('fair', 'A'), ('poor', 'B')]
    scenarios = [
        {"title": "100mm Rainfall", "pre_idx": (0,1,2), "post_idx": (9,10,11)},
        {"title": "230mm Rainfall", "pre_idx": (3,4,5), "post_idx": (12,13,14)},
        {"title": "500mm Rainfall", "pre_idx": (6,7,8), "post_idx": (15,16,17)}
    ]

    for row_idx, (cond, letter) in enumerate(conditions):
        # Load Data explicitly for this row
        df_24 = pd.read_excel(PATH_2024, sheet_name=cond)
        df_25 = pd.read_excel(PATH_2025, sheet_name=cond)
        df_17 = pd.read_excel(PATH_2017, sheet_name=cond)

        for col_idx, scen in enumerate(scenarios):
            ax = axes[row_idx, col_idx]
            
            # Plot data using your successful clean_plot logic
            clean_plot_subplot(ax, df_24, *scen["pre_idx"], 'Fiume: Pre-Fire Baseline', 'darkcyan', style='--', width=1.5)
            clean_plot_subplot(ax, df_24, *scen["post_idx"], 'Fiume 2024: Post-Fire', 'turquoise', width=2)
            clean_plot_subplot(ax, df_25, *scen["post_idx"], 'Fiume 2025: Post-Fire', 'lightseagreen', width=2)
            clean_plot_subplot(ax, df_17, *scen["pre_idx"], 'Rossano: Pre-Fire Baseline', 'indianred', style='--', width=1.5)
            clean_plot_subplot(ax, df_17, *scen["post_idx"], 'Rossano 2017: Post-Fire', 'lightcoral', width=2)

            # --- Formatting ---
            # Title only on the top row
            if row_idx == 0:
                ax.set_title(scen["title"], fontsize=16, fontweight='bold', pad=20)
            
            # X-label only on the bottom row
            if row_idx == 1:
                ax.set_xlabel('Time (Hours)', fontsize=13)
            
            ax.set_xlim(0, 36)
            ax.set_ylim(0, 5000)
            ax.grid(True, linestyle=':', alpha=0.4)
            ax.set_xticks(range(0, 37, 6))

        # Add Row Labels A and B
        axes[row_idx, 0].text(-0.2, 1.05, letter, transform=axes[row_idx, 0].transAxes, 
                              fontsize=30, fontweight='bold', va='top', ha='right')

    # Shared Y-axis label
    fig.text(0.01, 0.5, 'Discharge ($m^3/s$)', va='center', rotation='vertical', fontsize=15, fontweight='bold')

    # Shared Legend
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=5, bbox_to_anchor=(0.5, 0.02), 
               frameon=True, shadow=True, fontsize=12)

    plt.tight_layout(rect=[0.03, 0.08, 1, 0.95])
    
    # Save the consolidated figure
    plt.savefig('Figure_4_4_Consolidated_Hydrographs.png', dpi=300, bbox_inches='tight')
    print("✅ Consolidated Figure 4.4 generated: Figure_4_4_Consolidated_Hydrographs.png")

if __name__ == "__main__":
    generate_consolidated_figure()