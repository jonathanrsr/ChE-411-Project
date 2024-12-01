import matplotlib.pyplot as plt

# Data
strains = ["LL1004", "AVM008", "AVM051", "AVM003", "AVM059", 
           "AVM053", "AVM052", "AVM060", "AVM056", "AVM061"]
values = [2.18572697, 2.72617259, 2.93861716, 2.893825344, 2.72549206,
           2.97872778, 3.06209044, 3.02164887, 1.51885847, 2.54849306]

errors = [0.0] * len(values)  # Error is 0 for all
# Create the plot
plt.figure(figsize=(8, 6))
plt.bar(strains, values, color='lightgreen', yerr=errors, capsize=5, ecolor='black', edgecolor='lightgreen', width = 0.5)

# Add labels and title
plt.xlabel('C. Thermocellum Strain', fontsize=12)
plt.ylabel('Ethanol yield (mmol/mmol cellobiose)', fontsize=12)
plt.title('Ethanol yield iCHT669', fontsize=14)
plt.xticks(rotation=45, fontsize=10)  # Rotate x-axis labels

# Show the plot
plt.tight_layout()
plt.show()