from typing import Tuple, Dict
import random

from gpforecaster.model.gpf import GPF
from gpforecaster.utils.logger import Logger


def optimize_hyperparameters(
    dataset_name: str,
    hierarchical_data: Dict,
    num_trials: int = 20,
    learning_rates: Tuple[float] = (1e-2, 1e-3),
    weight_decays: Tuple[float] = (1e-3, 1e-4, 1e-5),
    scheduler_types: Tuple[str] = ("step", "exponential", "cosine", "none"),
    gamma_rates: Tuple[float] = (0.1, 0.9, 0.95, 0.8),
    inducing_points_percs: Tuple[float] = (0.75,),
) -> Tuple[float, float, str, float, float]:
    """
    Performs a random search to optimize the hyperparameters of the model.

    Parameters
        dataset: Dataset to run hyperparameter tuning
        hierarchical_data: Dict containing data and metadata
        num_trials: Number of trials to perform
        inducing_points_percs: Number of inducing points as a percentage of the original points

    Returns
        best_hyperparameters : A tuple containing the optimal learning rate,
            weight decay, and scheduler type
    """
    logger_tuning = Logger("hyperparameter_tuning", dataset=f"{dataset_name}_hypertuning", to_file=True)

    results = []

    for trial in range(num_trials):
        # Sample hyperparameters randomly
        learning_rate = random.choice(learning_rates)
        weight_decay = random.choice(weight_decays)
        scheduler_type = random.choice(scheduler_types)
        gamma_rate = random.choice(gamma_rates)
        inducing_points_perc = random.choice(inducing_points_percs)

        # Evaluate the performance with the sampled hyperparameters
        gpf = GPF(
            dataset=dataset_name,
            groups=hierarchical_data,
            inducing_points_perc=inducing_points_perc,
        )

        model, _ = gpf.train(
            lr=learning_rate,
            weight_decay=weight_decay,
            scheduler_type=scheduler_type,
            gamma_rate=gamma_rate,
        )

        val_loss = gpf.validate(model)

        results.append(
            (learning_rate, weight_decay, scheduler_type, gamma_rate, inducing_points_perc, val_loss)
        )

    results.sort(key=lambda x: x[5])
    best_hyperparameters = results[0]

    logger_tuning.info(
        f"Best hyperparameters: learning rate = {best_hyperparameters[0]}, "
        f"weight decay = {best_hyperparameters[1]}, "
        f"scheduler = {best_hyperparameters[2]}, "
        f"gamma = {best_hyperparameters[3]}, "
        f"inducing points percentage = {best_hyperparameters[4]}"
    )
    logger_tuning.info(f"Validation loss: {best_hyperparameters[4]}")

    return best_hyperparameters
