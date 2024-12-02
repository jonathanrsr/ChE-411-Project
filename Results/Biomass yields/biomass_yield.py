import matplotlib.pyplot as plt

# Data
strains = ["LL1004", "AVM008", "AVM051", "AVM003", "AVM059", 
           "AVM053", "AVM052", "AVM060", "AVM056", "AVM061"]
values = [0.351049374, 0.351026904, 0.294983609, 0.343383655, 0.351049374, 
          0.294983609, 0.287282466, 0.294983609, 0.253001377, 0.253001377]

# Create the plot
plt.figure(figsize=(8, 6))
plt.bar(strains, values, color='gold', edgecolor='gold', width = 0.5)

# Add labels and title
plt.xlabel('C. Thermocellum Strain', fontsize=12)
plt.ylabel('Biomass yield (g/g cellobiose)', fontsize=12)
plt.title('Biomass yield iCHT669', fontsize=14)
plt.xticks(rotation=45, fontsize=10)  # Rotate x-axis labels

# Show the plot
plt.tight_layout()
plt.show()