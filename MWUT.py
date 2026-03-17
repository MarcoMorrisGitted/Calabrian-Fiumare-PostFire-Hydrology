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

sheet_indices = {'230mm': 4, '500mm': 5} # 4=230mm PRE, 5=500mm PRE

def extract_rigorous_data(path, sheet_idx):
    """
    Extracts data, filters out HEC-HMS micro-basin noise (< 0.1 km2), 
    and returns Absolute Peak and Specific Peak arrays.
    """
    df = pd.read_excel(path, sheet_name=sheet_idx)
    
    # Isolate Subbasins only
    df_sub = df[df.iloc[:, 0].astype(str).str.contains('Subbasin', case=False, na=False)]
    
    area = pd.to_numeric(df_sub.iloc[:, 1], errors='coerce').values
    peak = pd.to_numeric(df_sub.iloc[:, 2], errors='coerce').values
    
    # FILTER: Only keep subbasins with Area >= 0.1 km2 and valid peak flows
    mask = (area >= 0.1) & (~np.isnan(area)) & (~np.isnan(peak))
    
    valid_area = area[mask]
    abs_peak = peak[mask]
    
    # Calculate Specific Peak (m3/s/km2)
    spec_peak = abs_peak / valid_area
    
    return abs_peak, spec_peak

def run_proper_mwut(val_f, val_r, label, rain):
    if len(val_f) < 3 or len(val_r) < 3:
        return f"{label:<35}\t{rain:<6}\tERROR: Insufficient Data"
        
    stat, p = mannwhitneyu(val_f, val_r, alternative='two-sided')
    
    m_f = np.mean(val_f)
    m_r = np.mean(val_r)
    diff = ((m_r - m_f) / m_f) * 100
    
    sig = "SIGNIFICANT" if p < 0.05 else "Not Sig"
    direction = "Rossano Higher" if m_r > m_f else "Fiume Higher"
    
    return f"{label:<35}\t{rain:<6}\t{p:<10.4f}\t{diff:>8.2f}%\t{sig}: {direction}"

# ==========================================
# 2. EXECUTION
# ==========================================
print("TABLE 1: ABSOLUTE PEAK DISCHARGE (m3/s) - All Active Subbasins (>= 0.1 km2)")
print("COMPARISON SCENARIO\tRAIN\tP-VALUE\tMEAN DIFF\tRESULT")
for rain, idx in sheet_indices.items():
    rf_abs, _ = extract_rigorous_data(paths['R_Fair'], idx)
    ff_abs, _ = extract_rigorous_data(paths['F_Fair'], idx)
    print(run_proper_mwut(ff_abs, rf_abs, "Fair vs Fair (Natural Baseline)", rain))

for rain, idx in sheet_indices.items():
    rp_abs, _ = extract_rigorous_data(paths['R_Poor'], idx)
    fp_abs, _ = extract_rigorous_data(paths['F_Poor'], idx)
    print(run_proper_mwut(fp_abs, rp_abs, "Poor vs Poor (Degraded Baseline)", rain))

for rain, idx in sheet_indices.items():
    rf_abs, _ = extract_rigorous_data(paths['R_Fair'], idx)
    fp_abs, _ = extract_rigorous_data(paths['F_Poor'], idx)
    print(run_proper_mwut(fp_abs, rf_abs, "Realism: Ross(Fair) v Fiume(Poor)", rain))

print("\n" + "="*80 + "\n")

print("TABLE 2: SPECIFIC PEAK DISCHARGE (m3/s/km2) - All Active Subbasins (>= 0.1 km2)")
print("COMPARISON SCENARIO\tRAIN\tP-VALUE\tMEAN DIFF\tRESULT")
for rain, idx in sheet_indices.items():
    _, rf_spec = extract_rigorous_data(paths['R_Fair'], idx)
    _, ff_spec = extract_rigorous_data(paths['F_Fair'], idx)
    print(run_proper_mwut(ff_spec, rf_spec, "Fair vs Fair (Natural Baseline)", rain))

for rain, idx in sheet_indices.items():
    _, rp_spec = extract_rigorous_data(paths['R_Poor'], idx)
    _, fp_spec = extract_rigorous_data(paths['F_Poor'], idx)
    print(run_proper_mwut(fp_spec, rp_spec, "Poor vs Poor (Degraded Baseline)", rain))

for rain, idx in sheet_indices.items():
    _, rf_spec = extract_rigorous_data(paths['R_Fair'], idx)
    _, fp_spec = extract_rigorous_data(paths['F_Poor'], idx)
    print(run_proper_mwut(fp_spec, rf_spec, "Realism: Ross(Fair) v Fiume(Poor)", rain))