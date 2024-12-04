import cobra
from utils import load_strains, load_model, update_model, save_json

def calc_pFBA(model: cobra.Model, strain_data: dict) -> dict:
    """
    Calculate the pFBA solution for the model.

    Parameters
    ----------
    model: cobra.Model
        The model to calculate the pFBA solution for.
    strain_data: dict
        The strain informations.

    Returns
    -------
    dict
        The pFBA solution.
    """
    model.objective = "EXCH_etoh_e"
    cellobiose_uptake_rate = 2.92144383597262 # mmol/(gDW h)

    reactions: list[str] = ["EXCH_etoh_e", "EXCH_ac_e", "EXCH_for_e", "EXCH_pyr_e", "EXCH_mal__L_e", "EXCH_lac__L_e"]

    # Define biomass yield bounds
    in_vivo_biomass_yield: float = strain_data["In vivo yield"]
    in_vivo_biomass_yield_error: float = strain_data["In vivo yield error"]
    yield_bounds: dict = {
        "Maximum biomass yield": in_vivo_biomass_yield + 1.96*in_vivo_biomass_yield_error,
        "Average biomass yield": in_vivo_biomass_yield,
        "Minimum biomass yield": in_vivo_biomass_yield - 1.96*in_vivo_biomass_yield_error
    }

    # Compute solutions for each biomass yield bound
    pfba_solution: dict = {}
    for bound_name, bound_value in yield_bounds.items():
        model.reactions[model.reactions.index("BIOMASS")].bounds = (bound_value, bound_value)
        solution: cobra.Solution = cobra.flux_analysis.parsimonious.optimize_minimal_flux(model)
        pfba_solution[bound_name] = {reaction: float(solution.fluxes.get(reaction, 0))/cellobiose_uptake_rate for reaction in reactions}

    return pfba_solution

if __name__ == "__main__":
    # Load the strains
    strains = load_strains()
    print("Strains successfully loaded.")

    results: dict = {}

    for strain_name, strain_data in strains.items():
        # Load the model
        model = load_model(strain_data)
        print(f"Model successfully loaded for {strain_name}.")

        # Update the model
        model = update_model(model, strain_data)
        print(f"Model successfully updated for {strain_name}.")

        # Calculate the pFBA solution
        print(f"Starting pFBA calculation for {strain_name}...")
        pfba_results: dict = calc_pFBA(model, strain_data)
        print(f"pFBA calculation successfully completed for {strain_name}.\n")

        results[strain_name] = pfba_results

    # Save the results
    output_path = r"Results\Metabolite yields at fixed biomass\metabolite_yields_pFBA.json"
    save_json(results, output_path)
    print(f"Results successfully saved to {output_path}")