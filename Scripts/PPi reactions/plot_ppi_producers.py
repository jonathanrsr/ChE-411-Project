import json
import matplotlib.pyplot as plt

def load_ppi_reactions_data():
    """
    Load the PPI reactions data from the json file.
    
    Returns
    -------
    ppi_reactions (dict): A dictionary containing the PPI reactions data.
    """
    with open(r"Results\PPi reactions\PPi_reactions.json") as f:
        return json.load(f)
    
def load_ppi_reactions_paper_data():
    """
    Load the PPI reactions data from the paper.
    
    Returns
    -------
    ppi_reactions (dict): A dictionary containing the PPI reactions data.
    """
    data: dict = {
        "AVM003": {
            "Number of low PPi producers": 31,
            "Number of medium PPi producers": 15,
            "Number of high PPi producers": 19
        },
        "AVM008": {
            "Number of low PPi producers": 31,
            "Number of medium PPi producers": 17,
            "Number of high PPi producers": 17
        },
        "AVM051": {
            "Number of low PPi producers": 30,
            "Number of medium PPi producers": 16,
            "Number of high PPi producers": 16
        },
        "AVM052": {
            "Number of low PPi producers": 30,
            "Number of medium PPi producers": 16,
            "Number of high PPi producers": 17
        },
        "AVM053": {
            "Number of low PPi producers": 30,
            "Number of medium PPi producers": 16,
            "Number of high PPi producers": 17
        },
        "AVM056": {
            "Number of low PPi producers": 32,
            "Number of medium PPi producers": 14,
            "Number of high PPi producers": 16
        },
        "AVM059": {
            "Number of low PPi producers": 31,
            "Number of medium PPi producers": 17,
            "Number of high PPi producers": 18
        },
        "AVM060": {
            "Number of low PPi producers": 30,
            "Number of medium PPi producers": 15,
            "Number of high PPi producers": 19
        },
        "AVM061": {
            "Number of low PPi producers": 30,
            "Number of medium PPi producers": 16,
            "Number of high PPi producers": 16
        },
        "LL1004": {
            "Number of low PPi producers": 31,
            "Number of medium PPi producers": 18,
            "Number of high PPi producers": 17
        }
    }

    return data
    
ppi_reactions = load_ppi_reactions_data()
ppi_reactions_paper = load_ppi_reactions_paper_data()

strains = list(ppi_reactions.keys())
low_producers = [strain["Number of low PPi producers"] for strain in ppi_reactions.values()]
medium_producers = [strain["Number of medium PPi producers"] for strain in ppi_reactions.values()]
high_producers = [strain["Number of high PPi producers"] for strain in ppi_reactions.values()]

low_paper = [ppi_reactions_paper[strain]["Number of low PPi producers"] for strain in strains]
medium_paper = [ppi_reactions_paper[strain]["Number of medium PPi producers"] for strain in strains]
high_paper = [ppi_reactions_paper[strain]["Number of high PPi producers"] for strain in strains]

colors = {
    "Low": "#277da1",
    "Medium": "#90be6d",
    "High": "#f94144"
}
colors_paper = {
    "Low": "#577590",
    "Medium": "#43aa8b",
    "High": "#f3722c"
}

width = 0.5  # Adjust bar width
x_indices = range(len(strains))

plt.figure(figsize=(12, 5.5))

plt.bar(
    [x_indices - width/4 for x_indices in x_indices],
    low_paper,
    label=r"Low  (<= 5% min. need) - Paper",
    edgecolor="black",
    color=colors_paper["Low"],
    width=0.25
)
plt.bar(
    [x_indices + width/4 for x_indices in x_indices],
    low_producers,
    label=r"Low  (<= 5% min. need) - This project",
    edgecolor="black",
    color=colors["Low"],
    width=0.25
)

plt.bar(
    [x_indices - width/4 for x_indices in x_indices],
    medium_paper,
    bottom=low_paper,
    label=r"Medium  (<= 70% min. need) - Paper",
    edgecolor="black",
    color=colors_paper["Medium"],
    width=0.25
)
plt.bar(
    [x_indices + width/4 for x_indices in x_indices],
    medium_producers,
    bottom=low_producers,
    label=r"Medium  (<= 70% min. need) - This project",
    edgecolor="black",
    color=colors["Medium"],
    width=0.25
)

plt.bar(
    [x_indices - width/4 for x_indices in x_indices],
    high_paper,
    bottom=[low + medium for low, medium in zip(low_paper, medium_paper)],
    label=r"High  (> 70% min. need) - Paper",
    edgecolor="black",
    color=colors_paper["High"],
    width=0.25
)
plt.bar(
    [x_indices + width/4 for x_indices in x_indices],
    high_producers,
    bottom=[low + medium for low, medium in zip(low_producers, medium_producers)],
    label=r"High  (> 70% min. need) - This project",
    edgecolor="black",
    color=colors["High"],
    width=0.25
)

for i, strain in enumerate(strains):
    plt.text(i + width/4, low_producers[i] / 2, str(low_producers[i]), ha='center', va='center', color='black', fontsize=9)
    plt.text(i - width/4, low_paper[i] / 2, str(low_paper[i]), ha='center', va='center', color='black', fontsize=9)
    plt.text(i + width/4, low_producers[i] + medium_producers[i] / 2, str(medium_producers[i]), ha='center', va='center', color='black', fontsize=9)
    plt.text(i - width/4, low_paper[i] + medium_paper[i] / 2, str(medium_paper[i]), ha='center', va='center', color='black', fontsize=9)
    plt.text(
        i + width/4,
        low_producers[i] + medium_producers[i] + high_producers[i] / 2,
        str(high_producers[i]),
        ha='center',
        va='center',
        color='black',
        fontsize=9
    )
    plt.text(
        i - width/4,
        low_paper[i] + medium_paper[i] + high_paper[i] / 2,
        str(high_paper[i]),
        ha='center',
        va='center',
        color='black',
        fontsize=9
    )

ax = plt.gca()
ax.spines['top'].set_visible(False)   # Remove top border
ax.spines['right'].set_visible(False)  # Remove left border

plt.xlabel("Strain", fontsize=12)
plt.ylabel("Number of reactions (counts)", fontsize=12)
plt.ylim(0, 70)
#plt.title(r"Number of low, medium, and high  for each strain")

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=3, frameon=False)
plt.xticks([x for x in x_indices], strains, rotation=45)
plt.tight_layout()

output_path = r"Results\PPi reactions\Figure 3.png"
plt.savefig(output_path, format="png", bbox_inches="tight")