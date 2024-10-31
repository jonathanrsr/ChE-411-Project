import memote
import os
import subprocess
import typing

def generate_reports(model_names: list[str] = []) -> None:
    if [] == model_names:
        model_names = [model.split(".sbml")[0] for 
                       model in os.listdir("Models") if 
                       model.endswith(".sbml")]
    try:
        for model_name in model_names:
            # If the report already exists, ask the user if they want to
            # overwrite it
            if os.path.exists("Reports/" + model_name + ".html"):
                overwrite = input("The report for " + model_name + 
                                  " already exists. Do you want to" + 
                                  " overwrite it? (y/n) ")
                if overwrite.lower() != "y":
                    continue

            print("Generating report for", model_name, "...")
            subprocess.run(
                ["memote",
                "report",
                "snapshot",
                "--filename",
                "Reports/" + model_name + ".html",
                "Models/" + model_name + ".sbml"],
                shell=True, capture_output=False, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e.stderr)

model_names = ["iCTH669_wo_GLGC"]

generate_reports()