import matplotlib.pyplot as plt
import numpy as np

# Data
strains = ["AVM003", "AVM008", "AVM051", "AVM052", "AVM053", 
           "AVM056", "AVM059", "AVM060", "AVM061", "LL1004"]
values = [0.343383655, 0.351026904, 0.294983609, 0.287282466, 0.294983609,
          0.253001377, 0.351049374, 0.294983609, 0.253001377, 0.351049374]
in_vivo_values = [0.22438, 0.25839, 0.21434, 0.19025, 0.20716,
                  0.20727, 0.25853, 0.19845, 0.17627, 0.28198]

# Calculate positions for bars
x = np.arange(len(strains))  # Position of strains
width = 0.25  # Bar width

# Create the plot
plt.figure(figsize=(12, 5.5))
plt.bar(x - width/2, values, color="#277da1", edgecolor="black", width=width, label="FBA results")
plt.bar(x + width/2, in_vivo_values, color="#90be6d", edgecolor="black", width=width, label="In vivo values")

ax = plt.gca()
ax.spines['top'].set_visible(False)   # Remove top border
ax.spines['right'].set_visible(False)  # Remove left border

# Add labels and title
plt.xlabel('Strain', fontsize=12)
plt.ylabel(r'Biomass yield (g/$\mathrm{g}_\mathrm{cellobiose}$)', fontsize=12)
#plt.title('Maximal predicted biomass yield for each strain')
plt.xticks(x, strains, rotation=45)  # Rotate x-axis labels and assign strain labels
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False)
plt.ylim(0, 0.4)

# Show the plot
plt.tight_layout()

output_path = r"Results\Biomass yields\Biomass yield.png"
plt.savefig(output_path, format="png", bbox_inches="tight")