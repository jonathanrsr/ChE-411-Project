import cobra
from cobra.flux_analysis import flux_variability_analysis
from utils import load_strains, load_model, update_model, save_json

def calc_fva(model: cobra.Model, strain_data: dict) -> dict:
    """
    Calculate the FVA solution for the model.

    Parameters
    ----------
    model: cobra.Model
        The model to calculate the FVA solution for.
    strain_data: dict
        The strain informations.
    objective: str
        The objective to optimize.

    Returns
    -------
    dict
        The FVA solution.
    """
    # Set the objective (fixed rate so no impact of the objective on the FVA)
    model.objective = "EXCH_cellb_e"
    cellobiose_uptake_rate = 2.92144383597262 # mmol/(gDW h)

    # Define the reactions to calculate the FVA for
    reactions: list[str] = ["EXCH_etoh_e", "EXCH_ac_e", "EXCH_for_e", "EXCH_pyr_e", "EXCH_mal__L_e", "EXCH_lac__L_e"]
    results = flux_variability_analysis(model, reaction_list=reactions, fraction_of_optimum=1.0)

    fva_solution = {
        reaction: {
            "min": results.loc[reaction, "minimum"] / cellobiose_uptake_rate,
            "max": results.loc[reaction, "maximum"] / cellobiose_uptake_rate
        }
        for reaction in reactions
    }

    return fva_solution

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

        # Calculate the FVA solution
        print(f"Starting FVA calculation for {strain_name}...")
        fva_solution: dict = calc_fva(model, strain_data)
        print(f"FVA successfully completed for {strain_name}.\n")

        results[strain_name] = fva_solution
    
    # Save the results
    output_path = r"Results\Metabolite yields at fixed biomass\metabolite_yields_FVA.json"
    save_json(results, output_path)
    print(f"Results successfully saved to {output_path}")
        