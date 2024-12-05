from utils import load_json
import matplotlib.pyplot as plt
import numpy as np

pfba_data: dict = load_json(r"Results\Metabolite yields at fixed biomass\metabolite_yields_pFBA.json")
strain_names: list[str] = list(pfba_data.keys())

yield_in_vivo_stdev: np.ndarray[float] = np.array([0.039667, 0.060672, 0.044414, 0.07231, 0.079599, 0.029943, 0.044697, 0.064913, 0.032526, 0.043496])
yield_in_vivo_at_average_biomass_yield: np.ndarray[float] = np.array([0.74902, 0.77221, 0.89255, 0.8148, 0.94992, 0.93805, 0.97154, 0.90584, 0.90042, 0.81067])
yield_in_vivo_at_max_biomass_yield: np.ndarray[float] = yield_in_vivo_at_average_biomass_yield + 1.96*yield_in_vivo_stdev
yield_in_vivo_at_min_biomass_yield: np.ndarray[float] = yield_in_vivo_at_average_biomass_yield - 1.96*yield_in_vivo_stdev

yield_old_model_at_average_biomass_yield: np.ndarray[float] = np.array([3.914248039, 3.9012514, 3.918086881, 3.927292147, 3.920829775, 3.920787443, 3.897517061, 3.921330973, 3.930125187, 3.892235489])

yield_new_model_at_average_biomass_yield: np.ndarray[float] = np.array([2.893825344, 2.709746659, 2.943345261, 3.062090439, 2.978727777, 1.725088314, 2.707906779, 3.021648871, 2.754722908, 1.997270955])


plt.figure(figsize=(12, 5.5))
width = 0.5/4

i = 0
for strain_name, strain_data in pfba_data.items():
    yields_at_max_biomass_yield: float = strain_data["Maximum biomass yield"]["EXCH_etoh_e"]
    yields_at_average_biomass_yield: float = strain_data["Average biomass yield"]["EXCH_etoh_e"]
    yields_at_min_biomass_yield: float = strain_data["Minimum biomass yield"]["EXCH_etoh_e"]

    plt.bar(i - width*1.5,
            yield_in_vivo_at_max_biomass_yield[i],
            yerr=[[yield_in_vivo_at_max_biomass_yield[i] - yield_in_vivo_at_average_biomass_yield[i]],
                  [yield_in_vivo_at_average_biomass_yield[i] - yield_in_vivo_at_min_biomass_yield[i]]],
            color="#277da1",
            edgecolor="black",
            capsize=5,
            align="center",
            width=width,
            label="In vivo" if i == 0 else None)
    
    plt.bar(i - width/2,
            yield_old_model_at_average_biomass_yield[i],
            color="#90be6d",
            edgecolor="black",
            capsize=5,
            align="center",
            width=width,
            label=r"$\it{i}$CBI655" if i == 0 else None)
    
    plt.bar(i + width/2,
            yield_new_model_at_average_biomass_yield[i],
            color="#f9c74f",
            edgecolor="black",
            capsize=5,
            align="center",
            width=width,
            label=r"$\it{i}$CTH669" if i == 0 else None)

    plt.bar(i + width*1.5,
            yields_at_average_biomass_yield, 
            yerr=[[yields_at_average_biomass_yield - yields_at_max_biomass_yield],
                  [yields_at_min_biomass_yield - yields_at_average_biomass_yield]],
            edgecolor="black",
            color="#f94144",
            capsize=5,
            align="center",
            width=width,
            label="This project" if i == 0 else None)
    i += 1
    

ax = plt.gca()
ax.spines['top'].set_visible(False)   # Remove top border
ax.spines['right'].set_visible(False)  # Remove left border

plt.xticks(range(len(strain_names)), strain_names, rotation=45)
plt.xlabel("Strain", fontsize=12)
plt.ylabel(r"Maximum ethanol yield (mmol/$\mathrm{mmol}_\mathrm{cellobiose}$)", fontsize=12)
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=4, frameon=False)
plt.ylim(0, 4)
plt.tight_layout()

output_path = r"Results\Metabolite yields at fixed biomass\Ethanol yields - pFBA.png"
plt.savefig(output_path, format="png", bbox_inches="tight")