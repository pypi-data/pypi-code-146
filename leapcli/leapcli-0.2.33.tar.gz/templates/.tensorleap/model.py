from pathlib import Path

'''
For more information, see: https://docs.tensorleap.ai/quickstart-using-cli#model-integration
'''


def leap_save_model(target_file_path: Path):
    # Load your model
    # Save it to the path supplied as an argument.

    print(f'Saving the model as {target_file_path}. Safe to delete this print.')
