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

def find_ppi_reactions(strain_model: cobra.Model) -> dict:
    """
    Find the PPi reactions in the model and calculate the min and max flux/turnover and stoichiometric coefficient.

    Parameters
    strain_model: cobra.Model
        The model to check the reaction in.

    Returns
    -------
    dict
        The dictionary containing the reaction ID, max and min flux, max and min production, and stoichiometric coefficient.
    """
    ppi_reactions: dict = {} 
    
    n_ppi_reactions = 0
    n_ppi_producers = 0
    n_ppi_consumers = 0
    n_ppi_bidirectional = 0
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
                if ppi_min_turnover > 0:
                    type: str = "Producer"
                    n_ppi_producers += 1
                elif ppi_max_turnover < 0:
                    type: str = "Consumer"
                    n_ppi_consumers += 1
                else:
                    type: str = "Bidirectional"
                    n_ppi_bidirectional += 1
                
                ppi_reactions["Number of PPi reactions"] = n_ppi_reactions
                ppi_reactions["Number of PPi producers"] = n_ppi_producers
                ppi_reactions["Number of PPi consumers"] = n_ppi_consumers
                ppi_reactions["Number of PPi bidirectional"] = n_ppi_bidirectional
                ppi_reactions[reaction.id] = {"Max flux": ppi_max_flux, "Max production": ppi_max_turnover, 
                                                        "Min flux": ppi_min_flux, "Min production": ppi_min_turnover,
                                                        "Stoichiometry": ppi_stoichiometry, "Type": type}
                
                n_ppi_reactions += 1
                break # Break the loop since the PPi metabolite was found

    print(f" - {n_ppi_reactions} PPi reactions found in the model ({n_ppi_producers} producers, {n_ppi_consumers} consumers and {n_ppi_bidirectional} bidirectionnal).")
    return ppi_reactions

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
    ppi_reactions: dict = find_ppi_reactions(strain_model)
    strain_results["PPi reactions"] = ppi_reactions
    results[strain] = strain_results
    print("PPi reactions successfully calculated for " + strain + ".\n")

# --- Save the results ---
with open(r"Results\PPi production\PPi_reactions.json", "w") as file:
    json.dump(results, file, indent=4)
print("Results successfully saved.")