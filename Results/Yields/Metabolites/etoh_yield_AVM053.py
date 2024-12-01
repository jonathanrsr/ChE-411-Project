import cobra
import os
from cobra.flux_analysis import parsimonious

# Load the model
model_path = r"C:\Users\djuki\systems\ChE-411-Project\.Archives\Models\Old\iCTH669_wo_GLGC.sbml"  
model = cobra.io.read_sbml_model(model_path)

# Find max etoh yield
# Define fixed reaction rates
fixed_rates = {
    "PPA":0.0,
    "GLGC":0.0,
    "BIOMASS":0.207158858,
    "EXCH_cellb_e": -2.92144383597262,  # Fix cellobiose uptake rate
}

# Apply fixed rates to the model
for reaction_id, rate in fixed_rates.items():
    reaction = model.reactions.get_by_id(reaction_id)
    reaction.bounds = (rate, rate)  # Fix reaction bounds

# Set the objective to maximize ethanol production
ethanol_reaction = "EXCH_etoh_e"  # Ethanol exchange reaction
model.objective = ethanol_reaction

# Run FBA
solution = model.optimize()

# Ensure the solution is feasible
if solution.status == "optimal":
    # Extract fluxes
    etoh_flux = solution.fluxes[ethanol_reaction]  # Ethanol flux
    biomass_flux = solution.fluxes["BIOMASS"]  # Biomass flux
    cellb_flux = -solution.fluxes["EXCH_cellb_e"]  # Cellobiose uptake (positive for consumption)

    # Calculate yields
    cellb_mass_up = cellb_flux * 342.2965 / 1000  # Convert cellobiose uptake to grams
    biomass_yield = biomass_flux / cellb_mass_up  # Biomass yield (g/g cellobiose)
    etoh_yield = etoh_flux / cellb_flux  # Ethanol yield (mol/mol cellobiose)

    # Print results
    print(f"Objective value (Ethanol flux): {etoh_flux:.8f}")
    print(f"Biomass flux (base): {biomass_flux:.8f}")
    print(f"Cellobiose uptake: {cellb_flux:.8f} mol")
    print(f"Ethanol yield: {etoh_yield:.8f} mol/mol cellobiose")
    print(f"Biomass yield: {biomass_yield:.8f} g/g cellobiose")
else:
    print("No optimal solution found.")


# Run pFBA
solution = parsimonious.optimize_minimal_flux(model)

# Step 4: Analyze pFBA results
if solution.status != "optimal":
    print("pFBA failed to find an optimal solution.")
else:
    # Extract fluxes for key reactions
    print("pFBA solution found.")
    print(f"Objective value (ethanol production): {solution.objective_value:.4f}")

    # Step 5: Calculate yield for products based on cellobiose uptake
    # Get flux of cellobiose uptake
    cellb_flux = -fixed_rates["EXCH_cellb_e"]  # Positive value for uptake
    cellb_mass_up = cellb_flux * 342.2965 / 1000  # Convert to grams

    # Calculate yields for various products
    products = ["EXCH_etoh_e", "EXCH_ac_e", "EXCH_for_e", "EXCH_pyr_e", "EXCH_mal__L_e", "EXCH_lac__L_e"]
    for product in products:
        product_flux = solution.fluxes.get(product, 0)
        yield_value = product_flux / cellb_flux
        print(f"pFBA {product}: {yield_value:.4f} mol product per mol cellobiose")

# Parameters for 95% confidence interval for biomass yield
in_vivo_yield = 0.20716
in_vivo_sd = 0.00548
biomass_weight = 1

# Set biomass bounds to 95% CI
biomass_reaction = model.reactions.get_by_id("BIOMASS")
biomass_reaction.lower_bound = (in_vivo_yield - 1.96 * in_vivo_sd) / biomass_weight
biomass_reaction.upper_bound = (in_vivo_yield + 1.96 * in_vivo_sd) / biomass_weight

print(f"Biomass bounds set to 95% CI: [{biomass_reaction.lower_bound}, {biomass_reaction.upper_bound}]")

# Fixed rates for other constraints
fixed_rates_2 = {
    "PPA":0.0,
    "GLGC":0.0,
    "EXCH_cellb_e": -2.92144383597262 
}

# Apply fixed rates to the model
for reaction_id, rate in fixed_rates_2.items():
    reaction = model.reactions.get_by_id(reaction_id)
    reaction.lower_bound = rate
    reaction.upper_bound = rate

# Fixing ethanol production to max, calculating min ethanol production
# First, set the ethanol exchange reaction (objective)
objective = "EXCH_etoh_e"
model.objective = model.reactions.get_by_id(objective)

# Minimize ethanol production
model.objective_direction = "min"
solution = model.optimize()

# Get the ethanol yield min
cellb_flux = -fixed_rates_2["EXCH_cellb_e"]  # Positive value for cellobiose uptake
cellb_mol_up = cellb_flux  # Cellobiose molar uptake

# Calculate minimum ethanol yield
min_etoh_yield = solution.fluxes[objective] / cellb_mol_up  # Min ethanol yield

# Max ethanol yield is already pre-calculated
max_etoh_yield = etoh_yield  # Set max ethanol yield

print(f"Min ethanol yield: {min_etoh_yield}")
print(f"Max ethanol yield: {max_etoh_yield}")

# Set the acetate exch reaction as objective

objective = "EXCH_ac_e"
model.objective = model.reactions.get_by_id(objective)

# Minimize acetate production
model.objective_direction = "min"
solution = model.optimize()

# Calculate minimum acetate yield
min_ac_yield = solution.fluxes[objective]/cellb_mol_up

# Maximize acetate production
model.objective_direction = "max"
solution = model.optimize()

# Calculate maximum acetate yield
max_ac_yield = solution.fluxes[objective]/cellb_mol_up

# Set the formate exch reaction as objective

objective = "EXCH_for_e"
model.objective = model.reactions.get_by_id(objective)

# Minimize formate production
model.objective_direction = "min"
solution = model.optimize()

# Calculate minimum formate yield
min_for_yield = solution.fluxes[objective]/cellb_mol_up

# Maximize fromate production
model.objective_direction = "max"
solution = model.optimize()

# Calculate maximum formate yield
max_for_yield = solution.fluxes[objective]/cellb_mol_up

# Set the lactate exch reaction as objective

objective = "EXCH_lac__L_e"
model.objective = model.reactions.get_by_id(objective)

# Minimize lactate production
model.objective_direction = "min"
solution = model.optimize()

# Calculate minimum lactate yield
min_lac_yield = solution.fluxes[objective]/cellb_mol_up

# Maximize lactate production
model.objective_direction = "max"
solution = model.optimize()

# Calculate maximum lactate yield
max_lac_yield = solution.fluxes[objective]/cellb_mol_up

# Set the pyruvate exch reaction as objective

objective = "EXCH_pyr_e"
model.objective = model.reactions.get_by_id(objective)

# Minimize pyruvate production
model.objective_direction = "min"
solution = model.optimize()

# Calculate minimum pyruvate yield
min_pyr_yield = solution.fluxes[objective]/cellb_mol_up

# Maximize pyruvate production
model.objective_direction = "max"
solution = model.optimize()

# Calculate maximum pyruvate yield
max_pyr_yield = solution.fluxes[objective]/cellb_mol_up

# Set the malate exch reaction as objective

objective = "EXCH_mal__L_e"
model.objective = model.reactions.get_by_id(objective)

# Minimize malate production
model.objective_direction = "min"
solution = model.optimize()

# Calculate minimum malate yield
min_mal_yield = solution.fluxes[objective]/cellb_mol_up

# Maximize malate production
model.objective_direction = "max"
solution = model.optimize()

# Calculate maximum malate yield
max_mal_yield = solution.fluxes[objective]/cellb_mol_up

print(f"Min ethanol yield: {min_etoh_yield}")
print(f"Max ethanol yield: {max_etoh_yield}")
print(f"Min acetate yield: {min_ac_yield}")
print(f"Max acetate yield: {max_ac_yield}")
print(f"Min formate yield: {min_for_yield}")
print(f"Max formate yield: {max_for_yield}")
print(f"Min lactate yield: {min_lac_yield}")
print(f"Max lactate yield: {max_lac_yield}")
print(f"Min pyruvate yield: {min_pyr_yield}")
print(f"Max pyruvate yield: {max_pyr_yield}")
print(f"Min malate yield: {min_mal_yield}")
print(f"Max malate yield: {max_mal_yield}")





