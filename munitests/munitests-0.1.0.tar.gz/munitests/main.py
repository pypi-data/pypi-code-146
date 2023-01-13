from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from IPython import get_ipython
from tqdm.auto import trange
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
)
import pandas as pd
import numpy as np
import os
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class ClassificationMetrics:
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    support: float
    classification_report: dict


@dataclass
class IntentErrors:
    incorrect_high_confidence: Optional[pd.DataFrame]
    incorrect_low_confidence: Optional[pd.DataFrame]
    correct_low_confidence: Optional[pd.DataFrame]


def is_notebook() -> bool:
    """Returns whether the code is running in a notebook.

    Returns:
        bool: True if the code is running in a notebook, False otherwise.
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def get_assistant(
    api_key: str, service_url: str = None, version: str = "2018-07-10"
) -> AssistantV1:
    """Returns an instance of the AssistantV1 class.

    Args:
        api_key (str): The API key for the Watson Assistant service.
        service_url (str): The URL for the Watson Assistant service.
        version (str, optional): The version of the Watson Assistant service. Defaults to "2018-07-10".

    Returns:
        AssistantV1: An instance of the AssistantV1 class.
    """
    authenticator = IAMAuthenticator(api_key)
    assistant = AssistantV1(authenticator=authenticator, version=version)
    if service_url is not None:
        assistant.set_service_url(service_url)
    return assistant


def run_blind_test(
    path: str,
    category: str,
    assistant: AssistantV1,
    workspace_id: str,
    threshold: float = 0.5,
    save: bool = False,
    save_path: str = None,
) -> pd.DataFrame:
    """Runs a blind test on the given assistant.

    The results of the blind test can optionally be saved to a file.
    If the file already exists, the results will be overwritten.

    The save path is the path to the file to save the results to.
    If the path is a directory, the file will be saved to the directory with the name "<category>.csv".
    If the path is a file, the results will be saved to that file.

    Args:
        path (str): The path to the test file.
        category (str): The category of the test.
        assistant (AssistantV1): The assistant to test.
        workspace_id (str): The workspace ID for the assistant.
        save (bool, optional): Whether to save the test results. Defaults to False.
        save_path (str, optional): The path to save the test results. Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing the results of the blind test.
    """

    results = []

    print(f"=== {category} BLIND TEST STARTING ===")
    with open(path, "r") as f:
        df = pd.read_csv(f)
        for i in trange(len(df)):

            # Get original text and predicted intent
            text = df["text"][i]
            prediction = df["intent"][i]

            # Get the response from the assistant
            response = assistant.message(
                workspace_id, input={"text": text}, alternate_intents=True
            ).get_result()

            # If the response is empty, print a message and continue
            if response is None:
                print(f"Response is empty for text: {text}")
                continue
            elif isinstance(response, dict):
                intents = response.get("intents", None)
            else:
                intents = response.json().get("intents", None)

            if intents is None:
                print(f"Intents is empty for text: {text}")
                continue

            # Unpack response
            intent1 = intents[0]["intent"]
            intent2 = intents[1]["intent"]
            intent3 = intents[2]["intent"]
            confidence1 = intents[0]["confidence"]
            confidence2 = intents[1]["confidence"]
            confidence3 = intents[2]["confidence"]

            results.append(
                {
                    "original_text": df["text"][i],
                    "predicted_intent": df["intent"][i].strip(),
                    "actual_intent1": intent1.strip(),
                    "actual_confidence1": confidence1,
                    "actual_intent2": intent2.strip(),
                    "actual_confidence2": confidence2,
                    "actual_intent3": intent3.strip(),
                    "actual_confidence3": confidence3,
                }
            )

    print(f"=== {category} BLIND TEST FINISHED ===")

    results = pd.DataFrame.from_records(results)
    results["actual_intent_above_threshold"] = np.where(
        (results["actual_confidence1"] < threshold),
        "BELOW_THRESHOLD",
        results["actual_intent1"],
    )

    if save:
        if save_path is None:
            save_path = category + ".csv"
        elif os.path.isdir(save_path):
            save_path = os.path.join(save_path, category + ".csv")

        results.to_csv(save_path, encoding="utf-8", index=False)

    return results


def get_confusion_matrix(
    df: pd.DataFrame,
    predicted_intent_column: str = "predicted_intent",
    actual_intent_column: str = "actual_intent_above_threshold",
) -> pd.DataFrame:
    """Returns a confusion matrix from the given dataframe.

    Args:
        df (pd.DataFrame): The dataframe to get the confusion matrix from.
        predicted_intent_column (str, optional): The name of the column containing the predicted intent. Defaults to "predicted_intent".
        actual_intent_column (str, optional): The name of the column containing the actual intent. Defaults to "actual_intent_above_threshold".

    Returns:
        pd.DataFrame: The confusion matrix.
    """
    return pd.crosstab(
        df[predicted_intent_column],
        df[actual_intent_column],
        rownames=["Predicted"],
        colnames=["Actual"],
    )


def plot_confusion_matrix(confusion_matrix: pd.DataFrame) -> None:
    """Plots the given confusion matrix.

    Args:
        confusion_matrix (pd.DataFrame): The confusion matrix to plot.
    """
    plt.figure(figsize=(10, 10))
    sns.heatmap(confusion_matrix, annot=True, fmt="d")
    if plt.isinteractive():
        plt.show()
    else:
        plt.savefig("confusion_matrix.png")


def get_classification_metrics(
    df: pd.DataFrame,
    predicted_intent_column: str = "predicted_intent",
    actual_intent_column: str = "actual_intent_above_threshold",
    print_metrics: bool = True,
    zero_division: Union[str, int] = 0,
) -> dict:
    """Returns the classification metrics for the given dataframe.

    Accurary: The accuracy is the fraction of predictions the classifier got right.

    Precision: The precision is the ratio tp / (tp + fp) where tp is the number
        of true positives and fp the number of false positives. The precision is
        intuitively the ability of the classifier not to label a negative sample as positive.

    Recall: The recall is the ratio tp / (tp + fn) where tp is the number of
        true positives and fn the number of false negatives. The recall is
        intuitively the ability of the classifier to find all the positive samples.

    F-Score: The F-beta score can be interpreted as a weighted harmonic mean of the precision and recall,
        where an F-beta score reaches its best value at 1 and worst score at 0.
        The F-beta score weights recall more than precision by a factor of beta.
        beta == 1.0 means recall and precision are equally important.

    Support: The support is the number of occurrences of each class in y_true.

    Args:
        df (pd.DataFrame): The dataframe to get the classification metrics from.
        predicted_intent_column (str, optional): The name of the column containing the predicted intent. Defaults to "predicted_intent".
        actual_intent_column (str, optional): The name of the column containing the actual intent. Defaults to "actual_intent_above_threshold".
        zero_division: “warn”, 0 or 1. Sets the value to return when there is a zero division. If set to “warn”, this acts as 0, but warnings are also raised. Defaults to 0.

    Returns:
        dict: The classification metrics.
    """
    accuracy = accuracy_score(
        df[actual_intent_column].values, df[predicted_intent_column].values
    )
    precision, recall, fscore, support = precision_recall_fscore_support(
        df[actual_intent_column], df[predicted_intent_column], average="weighted"
    )
    _classification_report = classification_report(
        df[actual_intent_column],
        df[predicted_intent_column],
        output_dict=True,
        zero_division=zero_division,
    )

    if print_metrics is True:
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {fscore:.4f}")
        print("Classification Report:")
        print(
            classification_report(
                df[actual_intent_column],
                df[predicted_intent_column],
                zero_division=zero_division,
            )
        )

    return ClassificationMetrics(
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_score=fscore,
        support=support,
        classification_report=_classification_report,
    )


def get_intent_errors(
    df: pd.DataFrame,
    predicted_intent_column: str = "predicted_intent",
    actual_intent_column: str = "actual_intent1",
    confidence_column: str = "actual_confidence1",
    threshold: float = 0.5,
    error_type: str = "all",
) -> IntentErrors:
    """Returns a dataframe containing the rows where the predicted intent is different from the actual intent.

    Args:
        df (pd.DataFrame): The dataframe to get the intent errors from.
        predicted_intent_column (str, optional): The name of the column containing the predicted intent. Defaults to "predicted_intent".
        actual_intent_column (str, optional): The name of the column containing the actual intent. Defaults to "actual_intent1".
        confidence_column (str, optional): The name of the column containing the intent confidence. Defaults to "actual_confidence1".
        threshold (float, optional): The threshold to use to determine if the intent is above or below the threshold. Defaults to 0.5.
        error_type (Optional[str], optional): The type of errors to return. Can be one of 'all', 'incorrect_high_confidence', 'incorrect_low_confidence' or 'correct_low_confidence'. Defaults to "all".

    Returns:
        pd.DataFrame: The dataframe containing the intent errors.
    """

    # Set the intent columns to lowercase and strip any whitespace
    _clean_prediction = df[predicted_intent_column].str.lower().str.strip()
    _clean_actual = df[actual_intent_column].str.lower().str.strip()

    # Create boolean masks for the different types of errors
    is_correct_intent = _clean_prediction == _clean_actual
    is_incorrect_intent = _clean_prediction != _clean_actual
    is_above_threshold = df[confidence_column] >= threshold
    is_below_threshold = df[confidence_column] < threshold

    # Return the dataframe containing the errors
    if error_type == "all":
        return IntentErrors(
            incorrect_high_confidence=df[is_incorrect_intent & is_above_threshold],
            incorrect_low_confidence=df[is_incorrect_intent & is_below_threshold],
            correct_low_confidence=df[is_correct_intent & is_below_threshold],
        )
    elif error_type == "incorrect_high_confidence":
        return IntentErrors(
            incorrect_high_confidence=df[is_incorrect_intent & is_above_threshold]
        )
    elif error_type == "incorrect_low_confidence":
        return IntentErrors(
            incorrect_low_confidence=df[is_incorrect_intent & is_below_threshold]
        )
    elif error_type == "correct_low_confidence":
        return IntentErrors(
            correct_low_confidence=df[is_correct_intent & is_below_threshold]
        )
    else:
        raise ValueError(
            "error_type must be one of 'all', 'incorrect_high_confidence', 'incorrect_low_confidence' or 'correct_low_confidence'"
        )
