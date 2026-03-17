import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1. The Catchment Areas
rossano_area = 276.7  # km²
fiume_area = 168.3    # km²

# 2. Peak Discharges (Q) for 500mm Event (Extracted from Tables 4.1 & 4.2)
# Rossano 
r_pre_good, r_post_good = 78.9, 91.0
r_pre_fair, r_post_fair = 97.4, 109.8
r_pre_poor, r_post_poor = 130.1, 144.4

# Fiumenicà 
f_pre_good, f_post_good = 42.4, 58.4
f_pre_fair, f_post_fair = 50.6, 74.7
f_pre_poor, f_post_poor = 70.3, 104.1

# 3. Calculate Specific Discharge (q = Q / Area)
q_vals = [
    # Rossano (Pre then Post)
    round(r_pre_good / rossano_area, 2), round(r_pre_fair / rossano_area, 2), round(r_pre_poor / rossano_area, 2),
    round(r_post_good / rossano_area, 2), round(r_post_fair / rossano_area, 2), round(r_post_poor / rossano_area, 2),
    # Fiumenicà (Pre then Post)
    round(f_pre_good / fiume_area, 2), round(f_pre_fair / fiume_area, 2), round(f_pre_poor / fiume_area, 2),
    round(f_post_good / fiume_area, 2), round(f_post_fair / fiume_area, 2), round(f_post_poor / fiume_area, 2)
]

# 4. Plotting Setup
# X-axis positioning with gaps between Pre/Post and larger gaps between Catchments
x_pos = [0, 1, 2,   4, 5, 6,     9, 10, 11,   13, 14, 15] 
labels = ['Good', 'Fair', 'Poor'] * 4

fig, ax = plt.subplots(figsize=(15, 8), dpi=300)

# 5. Define Your Custom Color Scheme
c_pre = '#C0C0C0'         # Grey for Pre-Fire
c_good = '#7FFFD4'        # Light Aquamarine
c_fair = 'peachpuff'      # Fair
c_poor = 'lightcoral'     # Poor
edge_color = 'black'

# Map colors to the 12 bars
colors = [
    c_pre, c_pre, c_pre,          # Rossano Pre
    c_good, c_fair, c_poor,       # Rossano Post
    c_pre, c_pre, c_pre,          # Fiume Pre
    c_good, c_fair, c_poor        # Fiume Post
]

# Map hatching (Hatched for Pre-fire, Solid for Post-fire)
hatches = ['//', '//', '//', '', '', '', '//', '//', '//', '', '', '']

# 6. Draw the Bars
for i in range(len(x_pos)):
    ax.bar(x_pos[i], q_vals[i], color=colors[i], edgecolor=edge_color, 
           linewidth=1.2, width=0.8, hatch=hatches[i], zorder=3)

# 7. Add Value Labels on top of bars (Bold formatting removed)
for i in range(len(x_pos)):
    ax.text(x_pos[i], q_vals[i] + 0.005, str(q_vals[i]), ha='center', va='bottom', 
            fontsize=10)

# 8. Formatting and Aesthetics (Bold formatting removed from Y-axis)
ax.set_ylabel('Specific Discharge (m³/s/km²)', fontsize=14)
ax.set_ylim(0, 0.70) # Headroom for the tallest bar (0.62)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, fontsize=11)

# Grouping Labels below the X-axis (Bold formatting removed)
ax.text(1, -0.05, 'PRE-FIRE', ha='center', fontsize=11, color='dimgrey')
ax.text(5, -0.05, 'POST-FIRE', ha='center', fontsize=11, color='black')
ax.text(10, -0.05, 'PRE-FIRE', ha='center', fontsize=11, color='dimgrey')
ax.text(14, -0.05, 'POST-FIRE', ha='center', fontsize=11, color='black')

# Catchment Titles (THESE ARE THE ONLY BOLD TEXT)
ax.text(3, -0.12, 'Rossano 2017', ha='center', fontsize=14, fontweight='bold')
ax.text(12, -0.12, 'Fiumenicà 2024', ha='center', fontsize=14, fontweight='bold')

ax.yaxis.grid(True, linestyle=':', alpha=0.6, zorder=0)

# 9. Custom Legend
patch_pre = mpatches.Patch(facecolor=c_pre, edgecolor=edge_color, hatch='//', label='Pre-Fire Baseline')
patch_good = mpatches.Patch(facecolor=c_good, edgecolor=edge_color, label="Post-Fire ('Good' Soil)")
patch_fair = mpatches.Patch(facecolor=c_fair, edgecolor=edge_color, label="Post-Fire ('Fair' Soil)")
patch_poor = mpatches.Patch(facecolor=c_poor, edgecolor=edge_color, label="Post-Fire ('Poor' Soil)")

ax.legend(handles=[patch_pre, patch_good, patch_fair, patch_poor], loc='upper left', 
          fontsize=11, framealpha=1)

# 10. Display
plt.tight_layout()
plt.subplots_adjust(bottom=0.2) # Make room for the bottom labels
plt.show()