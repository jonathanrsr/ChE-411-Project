import json
import matplotlib.pyplot as plt

def load_json(file: str) -> dict:
    """
    Load a JSON file.

    Parameters
    ----------
    file: str
        The file to load.

    Returns
    -------
    dict
        The loaded JSON file.
    """
    with open(file, "r") as f:
        data = json.load(f)

    return data

metabolite_yields = load_json(r"Results\Metabolite yields at fixed biomass\metabolite_yields.json")

strains: list = list(metabolite_yields.keys())

metabolites: list = ["Ethanol", "Acetate", "Formate", "Pyruvate", "Malate", "Lactate"]

colors: dict = {
    "Ethanol": "#277da1",
    "Acetate": "#4d908e",
    "Formate": "#90be6d",
    "Pyruvate": "#f9c74f",
    "Malate": "#f8961e",
    "Lactate": "#f94144"
}

plt.figure(figsize=(12, 5.5))

width = 0.5/len(metabolites)

for i, strain in enumerate(strains):
    for j, metabolite in enumerate(metabolite_yields[strain].keys()):
        plt.bar(
            i + (j-2)*width - width/2,  # Center the bars
            metabolite_yields[strain][metabolite]["max"],
            color=colors[metabolites[j]],
            edgecolor="black",
            width=width,
            label=metabolites[j] if i == 0 else None
        )

ax = plt.gca()
ax.spines['top'].set_visible(False)   # Remove top border
ax.spines['right'].set_visible(False)  # Remove left border

plt.xticks(range(len(strains)), strains, rotation=45)
plt.xlabel("Strain", fontsize=12)
plt.ylabel(r"Yield (g/$\mathrm{g}_\mathrm{cellobiose}$)", fontsize=12)
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False)
plt.ylim(0, 14)
plt.tight_layout()

output_path = r"Results\Metabolite yields at fixed biomass\Metabolite yields.png"
plt.savefig(output_path, format="png", bbox_inches="tight")