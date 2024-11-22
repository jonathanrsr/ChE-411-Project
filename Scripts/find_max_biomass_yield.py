from cobra.io import read_sbml_model
import pandas as pd

def calc_max_biomass_yield(model_path: str) -> pd.DataFrame:
    """
    Calculate the maximum biomass yield for multiple strains using a metabolic model.

    This function loads a COBRA model from an SBML file, applies specific reaction knockouts 
    for each strain, calculates the maximum biomass yield using linear optimization, 
    and saves the results to an Excel file.

    Parameters:
    ----------
    model_path : str
        Path to the SBML file containing the metabolic model.

    Returns:
    -------
    pandas.DataFrame
        A DataFrame containing the strain names and their corresponding maximum biomass yields.

    Strain Details:
    ---------------
    - Each strain may have specific reaction knockouts, which are applied before optimization.
    - The reaction bounds for knockouts are set to zero for both lower and upper bounds.
    - The reaction "EXCH_cellb_e" is fixed to simulate a cellobiose uptake rate of 
      -2.92144383597262 mol/gDW/h, which correspond to 1 g/dW/h.
    - Some strains in the original code had the reaction R00925 set to 0, which was deleted in this code since it doesn't appear in the model.

    Notes:
    ------
    - Reaction bounds are reset to defaults (0 to 1000) after each strain's calculations 
      to ensure independence between strains.
    - The Excel file is saved using the openpyxl library; ensure it is installed.
    """
    strains = {
        "LL1004": {},
        "AVM008": {"PPA": 0.0, "PPAna": 0.0},
        "AVM051": {"GLGC": 0.0},
        "AVM003": {"PPDK": 0.0},
        "AVM059": {"PPAKr": 0.0, "PACPT": 0.0, "ACADT": 0.0, "ACADCOAT": 0.0},
        "AVM053": {"PPA": 0.0, "PPAna": 0.0, "GLGC": 0.0},
        "AVM052": {"PPDK": 0.0, "GLGC": 0.0},
        "AVM060": {"PPAKr": 0.0, "PACPT": 0.0, "ACADT": 0.0, "ACADCOAT": 0.0, "GLGC": 0.0},
        "AVM056": {"PPA": 0.0, "PPAna": 0.0, "PPDK": 0.0, "GLGC": 0.0},
        "AVM061": {"PPA": 0.0, "PPAna": 0.0, "PPDK": 0.0, "GLGC": 0.0, 
                   "PPAKr": 0.0, "PACPT": 0.0, "ACADT": 0.0, "ACADCOAT": 0.0},
    }

    # Initialize an empty DataFrame to store results
    results = pd.DataFrame(columns=["Strain", "Max Biomass Yield"])

    # Iterate through each strain
    for strain, knockouts in strains.items():
        # Load the model each time to reset the strain
        model = read_sbml_model(model_path)

        # Set the objective function to biomass
        model.objective = "BIOMASS"

        # Set the cellobiose uptake rate
        model.reactions.get_by_id("EXCH_cellb_e").bounds = (-2.92144383597262, -2.92144383597262)

        # Apply knockouts
        for reaction_id, bound in knockouts.items():
            model.reactions.get_by_id(reaction_id).bounds = (bound, bound)

        # Optimize the model and calculate the biomass yield
        biomass_yield = model.slim_optimize()

        # Save results
        results.loc[len(results)] = {"Strain": strain, "Max Biomass Yield": biomass_yield}

        # Reset reaction bounds to default for the next strain
        for reaction_id in knockouts:
            model.reactions.get_by_id(reaction_id).bounds = (0.0, 1000.0)  # Typical default bounds

    # Save to Excel file
    results.to_excel("Results\\Jonathan\\Figure A.xlsx", index=False)

    # Return the results DataFrame
    return results

model_path = "Models\\iCTH669_w_GLGC.sbml"
biomass_results = calc_max_biomass_yield(model_path)
print(biomass_results)