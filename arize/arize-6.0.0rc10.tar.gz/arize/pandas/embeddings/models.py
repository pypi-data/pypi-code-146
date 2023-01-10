import pandas as pd

NLP_PRETRAINED_MODELS = [
    "bert-base-cased",
    "bert-base-uncased",
    "bert-large-cased",
    "bert-large-uncased",
    "distilbert-base-cased",
    "distilbert-base-uncased",
    "xlm-roberta-base",
    "xlm-roberta-large",
]

CV_PRETRAINED_MODELS = [
    "google/vit-base-patch16-224-in21k",
    "google/vit-base-patch16-384",
    "google/vit-base-patch32-224-in21k",
    "google/vit-base-patch32-384",
    "google/vit-large-patch16-224-in21k",
    "google/vit-large-patch16-384",
    "google/vit-large-patch32-224-in21k",
    "google/vit-large-patch32-384",
]


def list_supported_pretrained_models():
    data = {
        "Task": ["NLP" for _ in NLP_PRETRAINED_MODELS]
        + ["CV" for _ in CV_PRETRAINED_MODELS],
        "Architecture": [
            __parse_model_arch(model)
            for model in NLP_PRETRAINED_MODELS + CV_PRETRAINED_MODELS
        ],
        "Model Name": NLP_PRETRAINED_MODELS + CV_PRETRAINED_MODELS,
    }
    df = pd.DataFrame(data)
    df.sort_values(by=[col for col in df.columns], ascending=True, inplace=True)
    df.set_index(["Task", "Architecture"], inplace=True)
    return df


def __parse_model_arch(model_name):
    if "gpt" in model_name.lower():
        return "GPT"
    elif "bert" in model_name.lower():
        return "BERT"
    else:
        return "other"
