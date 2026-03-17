import pandas as pd
import numpy as np
from scipy.stats import wilcoxon

# ==========================================
# 1. SETUP
# ==========================================
files = {
    'Rossano 2017': {
        'Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_poor.xlsx",
        'Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_fair.xlsx",
        'Good': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_good.xlsx"
    },
    'Fiume 2024': {
        'Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_poor.xlsx",
        'Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_fair.xlsx",
        'Good': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_good.xlsx"
    },
    'Fiume 2025': {
        'Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_poor.xlsx",
        'Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_fair.xlsx",
        'Good': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume25_results_good.xlsx"
    }
}

rainfalls = ['100mm', '230mm', '500mm']
soil_types = ['Poor', 'Fair', 'Good']

print("Analysis Wilcox (Excluding Zeros):\n")
print("=" * 85)
print(f"{'CONDITION / SCENARIO':<35} | {'MEAN INCREASE':<15} | {'P-VALUE (Wilcoxon)'}")
print("=" * 85)

# ==========================================
# 2. PROCESSING
# ==========================================
for catchment, categories in files.items():
    print(f"\n{catchment}:")
    for soil in soil_types:
        print(f"\n--- {catchment.split()[0]} ({soil}) ---")
        path = categories[soil]
        for rain in rainfalls:
            df_pre = pd.read_excel(path, sheet_name=f"{rain}(PRE)", usecols=[0, 2], names=["Name", "Peak"])
            df_post = pd.read_excel(path, sheet_name=rain, usecols=[0, 2], names=["Name", "Peak"])
            
            # Name Matching
            df_pre['Name'] = df_pre['Name'].astype(str).str.strip()
            df_post['Name'] = df_post['Name'].astype(str).str.strip()
            
            # Filter Subbasins
            exclude = 'Total|Global|Sink|Reach|Junction|Outlet'
            df_pre = df_pre[~df_pre['Name'].str.contains(exclude, case=False, na=False)].dropna()
            df_post = df_post[~df_post['Name'].str.contains(exclude, case=False, na=False)].dropna()
            
            merged = pd.merge(df_pre, df_post, on="Name", suffixes=('_pre', '_post'))
            
            if not merged.empty:
                # MEAN INCREASE (Using all subbasins for the mean)
                perc_diffs = ((merged['Peak_post'] - merged['Peak_pre']) / merged['Peak_pre']) * 100
                mean_inc = perc_diffs.replace([np.inf, -np.inf], np.nan).dropna().mean()
                
                # WILCOXON TEST (Excluding Zeros)
                # zero_method='wilcox' discards all pairs where Peak_pre == Peak_post
                # This matches legacy statistical software results
                res = wilcoxon(merged['Peak_pre'], merged['Peak_post'], 
                               zero_method='wilcox', 
                               alternative='two-sided')
                p_val = res.pvalue
                
                label = f"{catchment.split()[0]} ({soil})"
                print(f"{label:<25} {rain:<10} | + {mean_inc:>6.2f}%        | {p_val:.2e} ***")

print("\n" + "=" * 85)