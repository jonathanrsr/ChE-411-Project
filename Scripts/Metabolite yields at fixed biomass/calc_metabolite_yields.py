import cobra
import json
from cobra.flux_analysis import flux_variability_analysis

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

if __name__ == '__main__':

    strains: dict = load_strains()
    results: dict = {}

    for strain, keys in strains.items():
        # --- Load the model ---
        model: cobra.Model = load_model(keys["glgC model"])
        print("Model successfully loaded for " + strain + ".")

        # --- Update the model for the strain ---
        strain_model: cobra.Model = update_model(model, keys["Knockouts"])
        print("Model successfully updated for " + strain + ".")

        strain_model.objective = "EXCH_cellb_e"

        reactions = ["EXCH_etoh_e", "EXCH_ac_e", "EXCH_for_e", "EXCH_pyr_e", "EXCH_mal__L_e", "EXCH_lac__L_e"]
        fva_results = flux_variability_analysis(strain_model, reaction_list=reactions, fraction_of_optimum=1.0)
        print("FVA successfully completed for " + strain + ".")

        results[strain] = {
            reaction: {"min": fva_results.loc[reaction, "minimum"]/2.92144383597262, "max": fva_results.loc[reaction, "maximum"]/2.92144383597262} for reaction in reactions
        }

    with open(r"Results\Yields\Metabolites\metabolite_yields.json", "w") as file:
        json.dump(results, file, indent=4)