import cobra
import os
import json

def load_model(GLGC: bool) -> cobra.Model:
    """
    Load a model from the Models directory.

    Parameters
    ----------
    GLGC: bool
        Whether the model should contain the GLGC reaction.

    Returns
    -------
    cobra.Model
        The loaded model.
    """
    if GLGC == True:
        model = cobra.io.read_sbml_model(r"Models\iCTH669_w_GLGC.sbml")
    else:
        model = cobra.io.read_sbml_model(r"Models\iCTH669_wo_GLGC.sbml")

    return model

def load_strains() -> dict:
    """
    Load the strains from the Strains.json file.

    Returns
    -------
    dict
        The strains dictionary.
    """
    with open(r"Scripts\Strains.json", "r") as file:
        strains = json.load(file)

        return strains

def update_model(model: cobra.Model, knockouts: dict) -> cobra.Model:
    """
    Update the model with the knockouts or fixed reaction rates.

    Parameters
    ----------
    model: cobra.Model
        The model to update.
    knockouts: dict
        The list of reactions to knockout.

    Returns
    -------
    cobra.Model
        The updated model.
    """
    # --- Set the cellobiose uptake rate ---
    model.reactions.get_by_id("EXCH_cellb_e").bounds = (-2.92144383597262, -2.92144383597262)
    print(" - Cellobiose uptake successfully set to -2.92144383597262 mmol/(gDW h).")

    # --- Set the biomass yield based on in vivo results within 1.96 std ---
    model.reactions[model.reactions.index("BIOMASS")].bounds = (keys["In vivo yield"] - 1.96*keys["In vivo yield error"],
                                                                keys["In vivo yield"] + 1.96*keys["In vivo yield error"])
    print(" - Biomass yield successfully set to between " + str(keys["In vivo yield"] - 1.96*keys["In vivo yield error"]) + " and " + str(keys["In vivo yield"] + 1.96*keys["In vivo yield error"]) + " gDW/mol.")

    # --- Knockout the reactions ---
    for reaction in knockouts:
        if reaction not in model.reactions:
            print(" - Reaction " + reaction + " not found in the model. Skipping...")
            continue
        model.reactions.get_by_id(reaction).knock_out()
        print(" - Reaction " + reaction + " successfully knocked out.")

    return model

def find_ppi_reactions(strain_model: cobra.Model, strain_miniumum_ppi_need) -> dict:
    """
    Find the PPi reactions in the model and calculate the min and max flux/turnover and stoichiometric coefficient.

    Parameters
    strain_model: cobra.Model
        The model to check the reaction in.
    strain_miniumum_ppi_need: float
        The minimum amount of PPi needed in the model.

    Returns
    -------
    dict
        The dictionary containing the reaction ID, max and min flux, max and min production, and stoichiometric coefficient.
    n_ppi_reactions: int
        The number of PPi reactions found in the model.
    n_ppi_producers: int
        The number of PPi producers found in the model.
    n_ppi_low_producers: int
        The number of low PPi producers found in the model.
    n_ppi_medium_producers: int
        The number of medium PPi producers found in the model.
    n_ppi_high_producers: int
        The number of high PPi producers found in the model.
    n_ppi_consumers: int
        The number of PPi consumers found in the model.
    n_ppi_low_consumers: int
        The number of low PPi consumers found in the model.
    n_ppi_medium_consumers: int
        The number of medium PPi consumers found in the model.
    n_ppi_high_consumers: int
        The number of high PPi consumers found in the model.
    n_ppi_bidirectionals: int
        The number of PPi bidirectional found in the model.
    """
    ppi_reactions: dict = {} 
    
    n_ppi_reactions = 0
    n_ppi_producers = 0
    n_ppi_low_producers = 0
    n_ppi_medium_producers = 0
    n_ppi_high_producers = 0
    n_ppi_consumers = 0
    n_ppi_low_consumers = 0
    n_ppi_medium_consumers = 0
    n_ppi_high_consumers = 0
    n_ppi_bidirectionals = 0
    for reaction in strain_model.reactions:
        reaction_metabolites: list = reaction.reactants + reaction.products # Get the metabolites in the reaction
        for metabolite in reaction_metabolites:
            if metabolite.id == "ppi_c": # Check if the reaction involves PPi
                ppi_stoichiometry: float = reaction.get_coefficient("ppi_c")
                strain_model.objective = reaction.id
                ppi_max_flux: float = strain_model.optimize("maximize").objective_value
                ppi_min_flux: float = strain_model.optimize("minimize").objective_value

                if (ppi_max_flux == 0 and ppi_min_flux == 0) or ppi_stoichiometry == 0: # Skip the reaction if the flux or stoichiometry is 0
                    continue

                # Check which turnover is the minimum and maximum (it can changes depending on the sign of the stoichiometry)
                if ppi_max_flux*ppi_stoichiometry >= ppi_min_flux*ppi_stoichiometry:
                    ppi_min_turnover: float = ppi_min_flux*ppi_stoichiometry
                    ppi_max_turnover: float = ppi_max_flux*ppi_stoichiometry
                else:
                    ppi_min_turnover: float = ppi_max_flux*ppi_stoichiometry
                    ppi_max_turnover: float = ppi_min_flux*ppi_stoichiometry

                # Check the type of reaction (Producer, Consumer, or Bidirectional)
                if ppi_min_turnover >= 0:
                    type: str = "Producer"
                    n_ppi_producers += 1
                    n_ppi_reactions += 1

                    if ppi_max_turnover/strain_miniumum_ppi_need <= 0.05:
                        n_ppi_low_producers += 1
                    elif ppi_max_turnover/strain_miniumum_ppi_need <= 0.7:
                        n_ppi_medium_producers += 1
                    else:
                        n_ppi_high_producers += 1

                elif ppi_max_turnover <= 0:
                    type: str = "Consumer"
                    n_ppi_consumers += 1
                    n_ppi_reactions += 1

                    if ppi_min_turnover/strain_miniumum_ppi_need >= -0.05:
                        n_ppi_low_consumers += 1
                    elif ppi_min_turnover/strain_miniumum_ppi_need >= -0.7:
                        n_ppi_medium_consumers += 1
                    else:
                        n_ppi_high_consumers += 1
                else:
                    type: str = "Bidirectional"
                    n_ppi_bidirectionals += 1
                    n_ppi_producers
                    n_ppi_consumers
                    n_ppi_reactions += 1

                    if ppi_max_turnover/strain_miniumum_ppi_need <= 0.05:
                        n_ppi_low_producers += 1
                    elif ppi_max_turnover/strain_miniumum_ppi_need <= 0.7:
                        n_ppi_medium_producers += 1
                    else:
                        n_ppi_high_producers += 1
                    if ppi_min_turnover/strain_miniumum_ppi_need >= -0.05:
                        n_ppi_low_consumers += 1
                    elif ppi_min_turnover/strain_miniumum_ppi_need >= -0.7:
                        n_ppi_medium_consumers += 1
                    else:
                        n_ppi_high_consumers += 1
                
                ppi_reactions[reaction.id] = {"Max flux": ppi_max_flux, "Max production": ppi_max_turnover, 
                                                        "Min flux": ppi_min_flux, "Min production": ppi_min_turnover,
                                                        "Stoichiometry": ppi_stoichiometry, "Type": type}
                
                break # Break the loop since the PPi metabolite was found

    print(f" - {n_ppi_reactions} PPi reactions found in the model ({n_ppi_producers} producers, {n_ppi_consumers} consumers and {n_ppi_bidirectionals} bidirectionnals).")
    return ppi_reactions, n_ppi_reactions, n_ppi_producers, n_ppi_low_producers, n_ppi_medium_producers, n_ppi_high_producers, n_ppi_consumers, n_ppi_low_consumers, n_ppi_medium_consumers, n_ppi_high_consumers, n_ppi_bidirectionals

strains: dict = load_strains()
results: dict = {}

for strain, keys in strains.items():
    # --- Load the model ---
    model: cobra.Model = load_model(keys["glgC model"])
    print("Model successfully loaded for " + strain + ".")

    # --- Update the model for the strain ---
    strain_model: cobra.Model = update_model(model, keys["Knockouts"])
    print("Model successfully updated for " + strain + ".")

    # --- Find the PPi reactions and calculate the min and max flux/turnover and stoichiometric coefficient ---
    strain_results: dict = {}
    ppi_reactions, n_ppi_reactions, n_ppi_producers, n_ppi_low_producers, n_ppi_medium_producers, n_ppi_high_producers, n_ppi_consumers, n_ppi_low_consumers, n_ppi_medium_consumers, n_ppi_high_consumers, n_ppi_bidirectionals = find_ppi_reactions(strain_model, keys["Minimum PPi need"])
    strain_results["Number of PPi reactions"] = n_ppi_reactions
    strain_results["Number of PPi producers"] = n_ppi_producers
    strain_results["Number of low PPi producers"] = n_ppi_low_producers
    strain_results["Number of medium PPi producers"] = n_ppi_medium_producers
    strain_results["Number of high PPi producers"] = n_ppi_high_producers
    strain_results["Number of PPi consumers"] = n_ppi_consumers
    strain_results["Number of low PPi consumers"] = n_ppi_low_consumers
    strain_results["Number of medium PPi consumers"] = n_ppi_medium_consumers
    strain_results["Number of high PPi consumers"] = n_ppi_high_consumers
    strain_results["Number of PPi bidirectional"] = n_ppi_bidirectionals
    strain_results["PPi reactions"] = ppi_reactions
    results[strain] = strain_results
    print("PPi reactions successfully calculated for " + strain + ".\n")

# --- Save the results ---
with open(r"Results\PPi production\PPi_reactions.json", "w") as file:
    json.dump(results, file, indent=4)
print("Results successfully saved.")