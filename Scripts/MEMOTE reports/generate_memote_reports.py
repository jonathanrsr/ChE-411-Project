import memote
import os
import subprocess
import typing

def generate_reports(model_names: list[str] = []) -> None:
    """
    Generates MEMOTE reports for models in the Models directory.

    Reports are saved in the Reports directory, with the name of the
    model as the filename and the extension .html. If a report already
    exists for a model, the user is asked if they want to overwrite it.

    Parameters
    ----------
    model_names : list[str]
        A list of model names to generate reports for. If empty, reports
        will be generated for all models in the Models directory.
    
    Returns
    -------
    None
    """
    # If no model names are provided, generate reports for all models
    # in the Models directory
    if [] == model_names:
        model_names = [model.split(".sbml")[0] for 
                       model in os.listdir("Models") if 
                       model.endswith(".sbml")]
    try:
        # Generate reports for each model
        for model_name in model_names:
            # If the report already exists, ask the user if they want to
            # overwrite it
            if os.path.exists("Reports/" + model_name + ".html"):
                overwrite = input("The report for " + model_name + 
                                  " already exists. Do you want to" + 
                                  " overwrite it? (y/n) ")
                if overwrite.lower() != "y":
                    continue # Skip this model
            # Generate the report
            print("Generating report for", model_name, "...")
            # Run memote report snapshot command
            subprocess.run(
                ["memote",
                "report",
                "snapshot",
                "--filename",
                "Reports/" + model_name + ".html",
                "Models/" + model_name + ".sbml"],
                shell=True, capture_output=False, check=True, text=True)
    # Catch any errors that occur during report generation
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e.stderr)

generate_reports()