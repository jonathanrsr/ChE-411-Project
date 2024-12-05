from utils import load_json, load_csv
from matplotlib import pyplot as plt
import numpy as np

pfba_data: dict = load_json("Results/Metabolite yields at fixed biomass/metabolite_yields_pFBA.json")
fva_data = load_json("Results/Metabolite yields at fixed biomass/metabolite_yields_FVA.json")
strain_names: list[str] = list(pfba_data.keys())
metabolites_names: list[str] = list(pfba_data[strain_names[0]]["Average biomass yield"].keys())

# Skip ethanol
j = 0
for metabolite_name in metabolites_names[1:]:
    plt.figure(figsize=(12, 5.5))
    width = 0.5/4
    y_height = np.array([4, 5, 4, 2, 4])

    i = 0
    for strain_name, strain_data in pfba_data.items():
        pfba_yields_at_max_biomass_yield: float = strain_data["Maximum biomass yield"][metabolite_name]
        if pfba_yields_at_max_biomass_yield <= 0:
            pfba_yields_at_max_biomass_yield = 0
        pfba_yields_at_mean_biomass_yield: float = strain_data["Average biomass yield"][metabolite_name]
        if pfba_yields_at_mean_biomass_yield <= 0:
            pfba_yields_at_mean_biomass_yield = 0
        pfba_yields_at_min_biomass_yield: float = strain_data["Minimum biomass yield"][metabolite_name]
        if pfba_yields_at_min_biomass_yield <= 0:
            pfba_yields_at_min_biomass_yield = 0

        fva_max_yield: float = fva_data[strain_name][metabolite_name]["max"]
        fva_min_yield: float = fva_data[strain_name][metabolite_name]["min"]
        
        metabolite_data = load_csv(f"Scripts\\Metabolite yields at fixed biomass\Data\\{metabolite_name}.csv")

        metabolite_in_vivo_yield = metabolite_data.loc[metabolite_data["strain"] == strain_name, "mean in vivo yield"].values[0]
        metabolite_in_vivo_std = metabolite_data.loc[metabolite_data["strain"] == strain_name, "stdev in vivo yield"].values[0]
        metabolite_in_vivo_max = metabolite_in_vivo_yield + 1.96*metabolite_in_vivo_std
        metabolite_in_vivo_min = metabolite_in_vivo_yield - 1.96*metabolite_in_vivo_std

        metabolite_old_model_pfba_yield = metabolite_data.loc[metabolite_data["strain"] == strain_name, "pFBA yield (old model)"].values[0]
        metabolite_old_model_fva_max_yield = metabolite_data.loc[metabolite_data["strain"] == strain_name, "maximum yield (old model)"].values[0]
        metabolite_old_model_fva_min_yield = metabolite_data.loc[metabolite_data["strain"] == strain_name, "minimum yield (old model)"].values[0]

        metabolite_new_model_pfba_yield = metabolite_data.loc[metabolite_data["strain"] == strain_name, "pFBA yield (new model)"].values[0]
        metabolite_new_model_fva_max_yield = metabolite_data.loc[metabolite_data["strain"] == strain_name, "maximum yield (new model)"].values[0]
        metabolite_new_model_fva_min_yield = metabolite_data.loc[metabolite_data["strain"] == strain_name, "minimum yield (new model)"].values[0]

        if pfba_yields_at_max_biomass_yield > pfba_yields_at_min_biomass_yield:
            if pfba_yields_at_mean_biomass_yield > pfba_yields_at_max_biomass_yield:
                pfba_yields_at_max_biomass_yield = pfba_yields_at_mean_biomass_yield
            if pfba_yields_at_mean_biomass_yield < pfba_yields_at_min_biomass_yield:
                pfba_yields_at_min_biomass_yield = pfba_yields_at_mean_biomass_yield
            low_value = pfba_yields_at_mean_biomass_yield - pfba_yields_at_min_biomass_yield
            high_value = pfba_yields_at_max_biomass_yield - pfba_yields_at_mean_biomass_yield
        else:
            if pfba_yields_at_mean_biomass_yield < pfba_yields_at_max_biomass_yield:
                pfba_yields_at_max_biomass_yield = pfba_yields_at_mean_biomass_yield
            if pfba_yields_at_mean_biomass_yield > pfba_yields_at_min_biomass_yield:
                pfba_yields_at_min_biomass_yield = pfba_yields_at_mean_biomass_yield
            low_value = pfba_yields_at_mean_biomass_yield - pfba_yields_at_max_biomass_yield
            high_value = pfba_yields_at_min_biomass_yield - pfba_yields_at_mean_biomass_yield

        plt.bar(i - width*1.5,
            metabolite_in_vivo_yield,
            yerr=[[metabolite_in_vivo_yield - metabolite_in_vivo_min],
                [metabolite_in_vivo_max - metabolite_in_vivo_yield]],
            color="#277da1",
            edgecolor="black",
            capsize=4,
            align="center",
            width=width,
            label="In vivo" if i == 0 else None)
        
        plt.bar(i - width/2,
            metabolite_old_model_pfba_yield,
            yerr=[[0], [0]],
            capsize=4,
            align="center",
            width=0)
        plt.bar(i - width/2,
            metabolite_old_model_fva_max_yield - metabolite_old_model_fva_min_yield,
            color="#90be6d",
            edgecolor="black",
            align="center",
            width=width,
            label=r"$\it{i}$CBI655" if i == 0 else None,
            bottom=metabolite_old_model_fva_min_yield)
        
        plt.bar(i + width/2,
            metabolite_new_model_pfba_yield,
            yerr=[[0], [0]],
            capsize=4,
            align="center",
            width=0)
        plt.bar(i + width/2,
            metabolite_new_model_fva_max_yield - metabolite_new_model_fva_min_yield,
            color="#f9c74f",
            edgecolor="black",
            align="center",
            width=width,
            label=r"$\it{i}$CTH669" if i == 0 else None)

        plt.bar(i + width*1.5,
                pfba_yields_at_mean_biomass_yield,
                yerr=[[low_value], [high_value]],
                capsize=4,
                align="center",
                width=0)
        plt.bar(i + width*1.5,
                fva_max_yield - fva_min_yield,
                color="#f94144",
                edgecolor="black",
                align="center",
                width=width,
                label="This project" if i == 0 else None,
                bottom=fva_min_yield)
        i += 1
    
    ax = plt.gca()
    ax.spines['top'].set_visible(False)   # Remove top border
    ax.spines['right'].set_visible(False)  # Remove left border

    metabolites_list = ["Acetate", "Formate", "Pyruvate", "Maltate", "Lactate"]

    plt.xticks(range(len(strain_names)), strain_names, rotation=45)
    plt.xlabel("Strain", fontsize=12)
    plt.ylabel(metabolites_list[j] + r" yield (mmol/$\mathrm{mmol}_\mathrm{cellobiose}$)", fontsize=12)
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=4, frameon=False)
    plt.ylim(0, y_height[j])
    plt.tight_layout()

    output_path = f"Results/Metabolite yields at fixed biomass/{metabolites_list[j]} yields - pFBA.png"
    plt.savefig(output_path, format="png", bbox_inches="tight")
    j += 1