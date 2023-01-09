# Simple script to run a model and get the results
import pycollimator as collimator

# Your dashboard generated token
token = ""
# Project uuid
project = ""
# Api url of the environment your project is in
api_url = "https://dev.collimator.ai"
# Unique model name from the project
model_name = ""


# Set the global variables used for auth
collimator.set_auth_token(token, project, api_url)

# Fetch model
model = collimator.load_model(model_name)

# Set model parameters for the simulation. Not saved to model by default.
model.set_parameters({"parameter1": 1, "parameter2": 2})

# Set model configuration for the simulation. Not saved to model by default.
model.set_configuration({"stop_time": 10})

# TODO: add find_block example

# Run the simulation
sim = collimator.run_simulation(model, wait=True)

# Get the results
results = sim.results

# Access the results as a pandas dataframe using block path
results.to_pandas()["Submodel_0.Plant_1.out_0"]

# TODO: add results[] example
