import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu

# ==========================================
# 1. FILE PATHS 
# ==========================================
paths = {
    'R_Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_fair.xlsx",
    'R_Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Ross17_results_poor.xlsx",
    'F_Fair': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_fair.xlsx",
    'F_Poor': r"C:\Localdata\Dissertation\From_Scratch\HEC_Sheets\Fiume24_results_poor.xlsx"
}

# Post-Fire: 1=230, 2=500 | Pre-Fire: 4=230, 5=500
scenarios = {
    '230mm': {'post': 1, 'pre': 4},
    '500mm': {'post': 2, 'pre': 5}
}

def extract_data(path, sheet_idx):
    df = pd.read_excel(path, sheet_name=sheet_idx)
    df_sub = df[df.iloc[:, 0].astype(str).str.contains('Subbasin', case=False, na=False)]
    
    area = pd.to_numeric(df_sub.iloc[:, 1], errors='coerce').values # Col B
    peak = pd.to_numeric(df_sub.iloc[:, 2], errors='coerce').values # Col C
    
    mask = (area >= 0.1) & (~np.isnan(area)) & (~np.isnan(peak))
    abs_peak = peak[mask]
    spec_peak = abs_peak / area[mask]
    
    return abs_peak, spec_peak

def run_mwut(val_f, val_r, label, rain):
    if len(val_f) < 3 or len(val_r) < 3:
        return f"{label:<45}\t{rain:<6}\tERROR: Insufficient Data"
        
    stat, p = mannwhitneyu(val_f, val_r, alternative='two-sided')
    m_f, m_r = np.mean(val_f), np.mean(val_r)
    diff = ((m_r - m_f) / m_f) * 100
    direction = "Fiume Higher" if m_f > m_r else "Rossano Higher"
    
    return f"{label:<45}\t{rain:<6}\t{p:<10.4f}\t{diff:>8.2f}%\t{direction}"

# ==========================================
# 2. EXECUTION
# ==========================================
for mode in ["ABSOLUTE", "SPECIFIC"]:
    print(f"\n--- {mode} PEAK DISCHARGE RESULTS ---")
    print(f"{'COMPARISON SCENARIO':<45}\tRAIN\tP-VALUE\tDIFF\tDIRECTION")
    
    is_spec = (mode == "SPECIFIC")

    for rain, sheets in scenarios.items():
        # 1. FAIR vs FAIR (PRE)
        r_abs, r_spec = extract_data(paths['R_Fair'], sheets['pre'])
        f_abs, f_spec = extract_data(paths['F_Fair'], sheets['pre'])
        print(run_mwut(f_spec if is_spec else f_abs, r_spec if is_spec else r_abs, "Fair vs Fair (PRE-FIRE)", rain))

        # 2. FAIR vs FAIR (POST)
        r_abs, r_spec = extract_data(paths['R_Fair'], sheets['post'])
        f_abs, f_spec = extract_data(paths['F_Fair'], sheets['post'])
        print(run_mwut(f_spec if is_spec else f_abs, r_spec if is_spec else r_abs, "Fair vs Fair (POST-FIRE)", rain))

        # 3. POOR vs POOR (PRE)
        r_abs, r_spec = extract_data(paths['R_Poor'], sheets['pre'])
        f_abs, f_spec = extract_data(paths['F_Poor'], sheets['pre'])
        print(run_mwut(f_spec if is_spec else f_abs, r_spec if is_spec else r_abs, "Poor vs Poor (PRE-FIRE)", rain))

        # 4. POOR vs POOR (POST)
        r_abs, r_spec = extract_data(paths['R_Poor'], sheets['post'])
        f_abs, f_spec = extract_data(paths['F_Poor'], sheets['post'])
        print(run_mwut(f_spec if is_spec else f_abs, r_spec if is_spec else r_abs, "Poor vs Poor (POST-FIRE)", rain))

        # 5. FIUME POOR vs ROSSANO FAIR (PRE)
        r_abs, r_spec = extract_data(paths['R_Fair'], sheets['pre'])
        f_abs, f_spec = extract_data(paths['F_Poor'], sheets['pre'])
        print(run_mwut(f_spec if is_spec else f_abs, r_spec if is_spec else r_abs, "Fiume(Poor PRE) v Ross(Fair PRE)", rain))

        # 6. FIUME POOR vs ROSSANO FAIR (POST)
        r_abs, r_spec = extract_data(paths['R_Fair'], sheets['post'])
        f_abs, f_spec = extract_data(paths['F_Poor'], sheets['post'])
        print(run_mwut(f_spec if is_spec else f_abs, r_spec if is_spec else r_abs, "Fiume(Poor POST) v Ross(Fair POST)", rain))
        
        print("-" * 110)
