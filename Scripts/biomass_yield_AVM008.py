import cobra
import os

# Load the model
model_path = r"C:\Users\djuki\systems\ChE-411-Project\.Archives\Models\Old\iCTH669_w_GLGC.sbml"  
model = cobra.io.read_sbml_model(model_path)

# Set biomass weight 
biomass_weight = 10.247910703070335

# Define fixed reaction rates 
fixed_rates = {
    "PPA": 0.0, 
    "PPAna": 0.0,
    "EXCH_cellb_e": -2.92144383597262
}

# Apply fixed rates to the model
for reaction_id, rate in fixed_rates.items():
    reaction = model.reactions.get_by_id(reaction_id)
    reaction.bounds = (rate, rate)

# Set the objective to maximize biomass production
biomass_reaction = "BIOMASS"  
model.objective = biomass_reaction

# Run FBA
solution = model.optimize()

# Calculate biomass yield
cellb_mol_up = -solution.fluxes["EXCH_cellb_e"]  # Cellobiose uptake in mol
cellb_mass_up = cellb_mol_up * 342.2965 / 1000  # Convert to grams
biomass_flux = solution.fluxes[biomass_reaction]
biomass_yield = (biomass_flux * biomass_weight) / cellb_mass_up

# Print results
print(f"Objective value (Biomass flux): {biomass_flux}")
print(f"Biomass yield: {biomass_yield} g/g cellobiose")
