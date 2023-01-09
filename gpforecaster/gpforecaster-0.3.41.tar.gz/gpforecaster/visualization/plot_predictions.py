import time

import matplotlib.pyplot as plt
import numpy as np

from gpforecaster import __version__


def plot_predictions_vs_original(
    dataset: str,
    prediction_mean: np.ndarray,
    prediction_std: np.ndarray,
    origin_data: np.ndarray,
    inducing_points: np.ndarray,
    gp_type: str,
    n_series_to_plot: int = 8,
) -> None:
    """
    Plot predictions and original series and store as pdf

    Parameters:
        dataset: dataset to plot
        prediction_mean: prediction mean (n_samples, n_series)
        prediction_std: prediction std (n_samples, n_series)
        origin_data: original dataset with shape (n_samples, n_series)
        inducing_points: inducing points to plot if sparse GP was used
        gp_type: type of GP used (exact, sparse, etc)
        n_series_to_plot: number of series to plot
    """
    has_inducing_points = True
    if has_inducing_points is None:
        has_inducing_points = False
    n = origin_data.shape[0]
    mean = prediction_mean
    upper = prediction_mean + 1.96 * prediction_std
    lower = prediction_mean - 1.96 * prediction_std

    # n_series needs to be even
    if not n_series_to_plot % 2 == 0:
        n_series_to_plot -= 1

    _, ax = plt.subplots(n_series_to_plot // 2, 2, figsize=(20, 10))
    ax = ax.ravel()
    inducing_points = inducing_points.detach().numpy()
    for i, ax_ in enumerate(ax):
        ax_.scatter(np.arange(n), origin_data[:, i], label="Training data")
        ax_.plot(np.arange(n), mean[:, i], label="GP mean")
        ax_.fill_between(
            np.arange(n), lower[:, i], upper[:, i], alpha=0.5, label="GP uncertainty"
        )
        if has_inducing_points:
            ax[i].scatter(
                inducing_points,
                np.zeros((inducing_points.shape[0],)),
                label="Inducing points",
            )
    plt.suptitle(f"Predictions for {dataset} using {gp_type} GPs")
    plt.legend()
    timestamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    plt.savefig(
        f"./plots/gpf_{__version__}_preds_{dataset}_{timestamp}.pdf",
        format="pdf",
        bbox_inches="tight",
    )
    plt.show()
