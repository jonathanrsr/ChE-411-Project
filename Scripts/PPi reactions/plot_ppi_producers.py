import json
import matplotlib.pyplot as plt

def load_ppi_reactions_data():
    """
    Load the PPI reactions data from the json file.
    
    Returns
    -------
    ppi_reactions (dict): A dictionary containing the PPI reactions data.
    """
    with open(r"Results\PPi production\PPi_reactions.json") as f:
        return json.load(f)
    
ppi_reactions = load_ppi_reactions_data()

strains = list(ppi_reactions.keys())
low_producers = [strain["Number of low PPi producers"] for strain in ppi_reactions.values()]
medium_producers = [strain["Number of medium PPi producers"] for strain in ppi_reactions.values()]
high_producers = [strain["Number of high PPi producers"] for strain in ppi_reactions.values()]

colors = {
    "Low": "#277da1",
    "Medium": "#90be6d",
    "High": "#f94144"
}

plt.figure(figsize=(10, 6))

low_bars = plt.bar(strains, low_producers, label=r"Low $\mathrm{PP}_\mathrm{i}$ producers", color=colors["Low"])
medium_bars = plt.bar(
    strains,
    medium_producers,
    bottom=low_producers,
    label=r"Medium $\mathrm{PP}_\mathrm{i}$ producers",
    color=colors["Medium"]
)
high_bars = plt.bar(
    strains,
    high_producers,
    bottom=[low + medium for low, medium in zip(low_producers, medium_producers)],
    label=r"High $\mathrm{PP}_\mathrm{i}$ producers",
    color=colors["High"]
)

for i, strain in enumerate(strains):
    plt.text(i, low_producers[i] / 2, str(low_producers[i]), ha='center', va='center', color='black', fontsize=9)
    plt.text(i, low_producers[i] + medium_producers[i] / 2, str(medium_producers[i]), ha='center', va='center', color='black', fontsize=9)
    plt.text(
        i,
        low_producers[i] + medium_producers[i] + high_producers[i] / 2,
        str(high_producers[i]),
        ha='center',
        va='center',
        color='black',
        fontsize=9
    )

plt.xlabel("Strain")
plt.ylabel("Number of reactions (counts)")
plt.ylim(0, 70)
plt.title(r"Number of low, medium, and high $\mathrm{PP}_\mathrm{i}$ producers for each strain")

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)
plt.xticks(rotation=45)
plt.tight_layout()

output_path = r"Results\PPi production\Figure 3.svg"
plt.savefig(output_path, format="svg", bbox_inches="tight")