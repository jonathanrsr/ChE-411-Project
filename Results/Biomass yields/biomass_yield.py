import matplotlib.pyplot as plt
import numpy as np

# Data
strains = ["AVM003", "AVM008", "AVM051", "AVM052", "AVM053", 
           "AVM056", "AVM059", "AVM060", "AVM061", "LL1004"]
values = [0.343383655, 0.351026904, 0.294983609, 0.287282466, 0.294983609,
          0.253001377, 0.351049374, 0.294983609, 0.253001377, 0.351049374]
in_vivo_values = [0.22438, 0.25839, 0.21434, 0.19025, 0.20716,
                  0.20727, 0.25853, 0.19845, 0.17627, 0.28198]
in_vivo_std = np.array([0.00567, 0.01256, 0.0061 , 0.00774, 0.00548, 0.00365, 0.00618, 0.01467, 0.00396, 0.01401])
in_vivo_max = in_vivo_values + 1.96*in_vivo_std
in_vivo_min = in_vivo_values - 1.96*in_vivo_std

old = np.array([2.869887338, 2.312024591, 2.869887338, 2.869887338, 
                   2.312024591, 2.312024591, 2.869887338, 2.869887338, 
                   1.750691765, 2.869887338])

new = np.array([0.337259026, 0.345197903, 0.301076787, 0.29338626, 
                   0.301076787, 0.259210812, 0.345220044, 0.301076787, 
                   0.259210812, 0.345220044])

# Calculate positions for bars
x = np.arange(len(strains))  # Position of strains
width = 0.5/4  # Bar width

# Create the plot
plt.figure(figsize=(12, 5.5))
plt.bar(x - width*1.5, in_vivo_values, yerr=[in_vivo_values - in_vivo_min, in_vivo_max - in_vivo_values],color="#277da1", edgecolor="black", width=width, label="In vivo values", capsize=5)
plt.bar(x - width/2, old, color="#90be6d", edgecolor="black", width=width, label=r"$\it{i}$CBI655")
plt.bar(x + width/2, new, color="#f9c74f", edgecolor="black", width=width, label=r"$\it{i}$CTH669")
plt.bar(x + width*1.5, values, color="#f94144", edgecolor="black", width=width, label="FBA results")

ax = plt.gca()
ax.spines['top'].set_visible(False)   # Remove top border
ax.spines['right'].set_visible(False)  # Remove left border

# Add labels and title
plt.xlabel('Strain', fontsize=12)
plt.ylabel(r'Biomass yield (g/$\mathrm{g}_\mathrm{cellobiose}$)', fontsize=12)
#plt.title('Maximal predicted biomass yield for each strain')
plt.xticks(x, strains, rotation=45)  # Rotate x-axis labels and assign strain labels
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=4, frameon=False)
plt.ylim(0, 3)

# Show the plot
plt.tight_layout()

output_path = r"Results\Biomass yields\Biomass yield.png"
plt.savefig(output_path, format="png", bbox_inches="tight")