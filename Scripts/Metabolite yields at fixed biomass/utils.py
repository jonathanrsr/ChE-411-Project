import cobra
import json

def load_json(path: str) -> dict:
    """
    Load a JSON file.

    Parameters
    ----------
    path: str
        The path to the JSON file.

    Returns
    -------
    dict
        The loaded JSON file.
    """
    with open(path, "r") as file:
        data = json.load(file)

    return data

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

def load_model(strain_data: dict) -> cobra.Model:
    """
    Load a model from the Models directory.

    Parameters
    ----------
    strain: dict
        The strain informations.

    Returns
    -------
    cobra.Model
        The loaded model.
    """
    if strain_data["glgC model"] == True:
        model = cobra.io.read_sbml_model(r"Models\iCTH669_w_GLGC.sbml")
    else:
        model = cobra.io.read_sbml_model(r"Models\iCTH669_wo_GLGC.sbml")

    return model

def update_model(model: cobra.Model, strain_data: dict) -> cobra.Model:
    """
    Update the model with the knockouts or fixed reaction rates.

    Parameters
    ----------
    model: cobra.Model
        The model to update.
    strain_data: dict
        The strain informations.

    Returns
    -------
    cobra.Model
        The updated model.
    """
    # --- Set the cellobiose uptake rate ---
    model.reactions.get_by_id("EXCH_cellb_e").bounds = (-2.92144383597262, -2.92144383597262)
    print(" - Cellobiose uptake successfully set to -2.92144383597262 mmol/(gDW h).")

    # --- Set the biomass yield based on in vivo results within 1.96 std ---
    in_vivo_biomass_yield = strain_data["In vivo yield"]
    in_vivo_biomass_yield_error = strain_data["In vivo yield error"]
    model.reactions[model.reactions.index("BIOMASS")].bounds = (in_vivo_biomass_yield - 1.96*in_vivo_biomass_yield_error,
                                                                in_vivo_biomass_yield + 1.96*in_vivo_biomass_yield_error)
    print(" - Biomass yield successfully set to between " + str(in_vivo_biomass_yield - 1.96*in_vivo_biomass_yield_error) + " and " + str(in_vivo_biomass_yield + 1.96*in_vivo_biomass_yield_error) + " gDW/mol.")

    # --- Knockout the reactions ---
    for reaction in strain_data["Knockouts"]:
        if reaction not in model.reactions:
            print(" - Reaction " + reaction + " not found in the model. Skipping...")
            continue
        model.reactions.get_by_id(reaction).knock_out()
        print(" - Reaction " + reaction + " successfully knocked out.")

    return model

def save_json(data: dict, path: str):
    """
    Save a dictionary to a JSON file.

    Parameters
    ----------
    data: dict
        The dictionary to save.
    path: str
        The path to save the JSON file to.
    """
    with open(path, "w") as file:
        json.dump(data, file, indent=4)