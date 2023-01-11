from collections import defaultdict
from enum import Enum
import json
import random
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as plt
from nltk.corpus import brown
import numpy as np
import pandas as pd
from sklearn import metrics
import torch
import torch.nn as nn
from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer
from transformers import PreTrainedTokenizer

from truera.client.util.python_utils import import_optional
from truera.nlp.fairness.output_metrics import disparity_wrapper
from truera.nlp.fairness.output_metrics import OutputMetrics


class WordGroup(Enum):
    MALE = "male_class"
    FEMALE = "female_class"
    OCCUPATION = "gender_stereotype_pairs"


class Corpus(Enum):
    WORD2VEC = 1
    BROWN = 2


CLASSES_DICT = None


def load_model(
    model_name: Optional[str] = "bert-base-cased"
) -> Union["gensim.models.KeyedVectors", list]:
    '''
    get HuggingFace or Gensim model given model name
    Args:
        model_name: (string) the name of the HuggingFace or Gensim model
    Return:
        embedder: (KeyedVectors) return gensim model if model_name is gensim
        embedder: (list) return [Tokenizer, Model] if model_name is HuggingFace
        
    '''
    if "word2vec" in model_name or "glove" in model_name:
        gensim = import_optional(
            "gensim",
            "word2vec and glove vectors. gensim cannot be imported or installed via truera due to GPL license, it must be installed manually before calling truera."
        )
        return gensim.downloader.load(model_name)
    return [
        AutoTokenizer.from_pretrained(model_name),
        AutoModelForMaskedLM.from_pretrained(model_name)
    ]


def get_word_embedding_for_transformers(
    token_embeddings: torch.Tensor, attention_mask: torch.Tensor
) -> torch.Tensor:
    '''
    apply attention mask to token embeddings and mean pool to produce word embedding
    Args:
        token_embeddings: (torch.Tensor) the word embeddings produced by embedding model, shape [num_tokens, token_dim]
        attention_mask: (torch.Tensor) binary attention mask for each token, shape [num_tokens]
    Return:
        word_embeddings: (torch.Tensor) mean pool across num_tokens dimension of token_embeddings*attention_mask, shape [token_dim]
    '''
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(
        token_embeddings.size()
    ).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


def get_word_embedding(
    word: str,
    embedder: Union["gensim.models.KeyedVectors", list],
    avg_embedding: Optional[torch.Tensor] = None
) -> torch.Tensor:
    '''
    apply an embedder to a word to get word embedding
    Args:
        word: (string) the input word 
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]
        avg_embedding: (torch.Tensor) an average corpus embedding to recenter word_embedding
    Return:
        word_embedding: (torch.Tensor) word_embedding for the input word
    '''
    if isinstance(embedder, list):
        tokenizer, model = embedder
        encoded_input = tokenizer(word, return_tensors='pt')
        model_output = model(**encoded_input)
        token_embeddings = model_output[0]
        word_embedding = get_word_embedding_for_transformers(
            token_embeddings, encoded_input['attention_mask']
        )

    else:
        word_embedding = torch.Tensor(embedder[word]).unsqueeze(dim=0)
    if avg_embedding is not None:
        return word_embedding - avg_embedding
    return word_embedding


def get_class_embedding(
    class_name: str,
    embedder: Union["gensim.models.KeyedVectors", list],
    mean_pool: Optional[bool] = False,
    avg_embedding: Optional[torch.Tensor] = None
) -> torch.Tensor:
    '''
    get class embedding by averaging word embeddings for all words in a given class
    Args
        class_name: (string) name of a class in classes.json
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]
        mean_pool: (bool) whether or not mean pool embeddings
        avg_embedding: (torch.Tensor) an average corpus embedding to recenter word_embedding
    Return:
        class_embedding: (torch.Tensor) averaging word embedding for all words in a given class
    '''
    class_words = get_class(class_name)
    sample_embedding = get_word_embedding(
        class_words[0], embedder, avg_embedding
    )
    embeddings = torch.zeros(len(class_words), sample_embedding.shape[-1])
    for i, w in enumerate(class_words):
        embeddings[i] = get_word_embedding(w, embedder, avg_embedding)
    if mean_pool:
        return embeddings.mean(dim=0).unsqueeze(dim=0)
    return embeddings


def get_embedding(
    word_or_class_name: Union[str, WordGroup],
    embedder: Union["gensim.models.KeyedVectors", list],
    avg_embedding: Optional[torch.Tensor] = None
) -> torch.Tensor:
    '''
    get embedding for a word or average class embedding for all words in a given class
    Args:
        word_or_class_name: (string or WordGroup) either a word or the enum WordGroup of a class in classes.json
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]
        avg_embedding: (torch.Tensor) an average corpus embedding to recenter word_embedding
    Return:
        word_embedding: get word embedding if input is just word, 
                        otherwise get average of word embeddings in the class if input is a class_name  
    '''
    if isinstance(word_or_class_name, WordGroup):
        return get_class_embedding(
            word_or_class_name.value, embedder, True, avg_embedding
        )
    return get_word_embedding(word_or_class_name, embedder, avg_embedding)


def get_word_list(
    corpus: Corpus, size: int, embedder: Union["gensim.models.KeyedVectors",
                                               list]
) -> Sequence[str]:
    '''
    get list of words from a given text corpus
    Args:
        corpus: (Corpus enum) enum for describing which vocab corpus to use
        size: (int) number of words to sample from the corpus
        embedder: (Gensim KeyedVector)  gensim embedder when fetching word2vec vocab
    Return:
        word_list: (list) of size-many words from corpus  
    '''
    word_list = []
    if corpus.value == 1:
        # embedder to be gensim to use index_to_key
        assert (embedder is not None)
        word_list = embedder.index_to_key
        random.shuffle(word_list)
        word_list[:size]
        return word_list
    elif corpus.value == 2:
        brown_words = brown.words(categories='news')
        word_idxs = set(random.sample(range(0, len(brown_words)), size))
        word_list = []
        for idx, word in enumerate(brown_words):
            if idx in word_idxs:
                word_list.append(word)
    return word_list


def get_average_embedding(
    word_list: Sequence[str], embedder: Union["gensim.models.KeyedVectors",
                                              list]
) -> torch.Tensor:
    '''
    get average  embedding for all words in a given list of words
    Args:
        word_list: (list) of size-many words from corpus  
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]
    Return:
        avg_embedding: (torch.Tensor) average of word embeddings from word_list  
    '''
    embedding = get_embedding(word_list[0], embedder)

    avg_embedding = torch.Tensor(len(word_list), *embedding.shape)
    avg_embedding[0] = embedding

    for i in range(1, len(word_list)):
        avg_embedding[i] = get_embedding(word_list[0], embedder)

    return avg_embedding.mean(dim=0)


def get_gender_word_pairs(
    include_occupations: bool
) -> Sequence[Union[Tuple[str], Sequence[str]]]:
    '''
    get list of gender word pairs
    Args:
        include_occupations: (bool) whether to add occupation word pairs or not  
    Return:
        word_pairs: (List[Tuple or List]) of gender word pairs 
    '''
    male_class = get_class(WordGroup.MALE)
    female_class = get_class(WordGroup.FEMALE)
    if len(male_class) == len(female_class):
        word_pairs = zip(male_class, female_class)
    else:

        pairs_len = min(len(male_class), len(female_class))
        word_pairs = []
        for i in range(pairs_len):
            word_pairs.append((male_class[i], female_class[i]))

    if include_occupations:
        word_pairs += get_class(WordGroup.OCCUPATION)
    return word_pairs


def average_word_pair_operator(
    word_pairs: Sequence[Union[Tuple[str], Sequence[str]]],
    embedder: Union["gensim.models.KeyedVectors", list],
    operator: Callable[[torch.Tensor, torch.Tensor], torch.Tensor]
) -> torch.Tensor:
    '''
    a helper method used to operate on list of word pairs
    Args:
        word_pairs: (List[Tuple or List]) of gender word pairs 
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]
        operator: (lamdba) a function that accepts two torch.Tensors as input and returns a torch.Tensor as output
    Return:
        output_embedding: (torch.Tensor) average of outputs from operating on each word pair's tensors
    '''
    embedding = get_embedding(word_pairs[0][0], embedder)
    output_embedding = torch.Tensor(len(word_pairs), *embedding.shape)

    for idx, pair in enumerate(word_pairs):
        class_1_word, class_2_word = pair
        class_1_vector = get_embedding(class_1_word, embedder)
        class_2_vector = get_embedding(class_2_word, embedder)
        output_embedding[idx] = operator(class_1_vector, class_2_vector)

    return output_embedding.mean(dim=0)


def get_average_word_pair_difference(
    word_pairs: Sequence[Union[Tuple[str], Sequence[str]]],
    embedder: Union["gensim.models.KeyedVectors", list]
) -> torch.Tensor:
    '''
    get difference between embeddings from each word pair, average the results
    Args:
        word_pairs: (List[Tuple or List]) of gender word pairs 
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]
    Return:
        avg_difference_embedding: (torch.Tensor) average difference embedding between each word pair's embeddings
    '''
    operator = lambda vector_1, vector_2: vector_1 - vector_2
    return average_word_pair_operator(word_pairs, embedder, operator)


# Needs main features dimension to be of size 3
def get_average_word_pair_cross_product(
    word_pairs: Sequence[Union[Tuple[str], Sequence[str]]],
    embedder: Union["gensim.models.KeyedVectors", list]
) -> torch.Tensor:
    '''
    get a cross product of each embeddings from each word pair, average the results
    NOT FUNCTIONAL since embeddings must have size 3
    Args:
        word_pairs: (List[Tuple or List]) of gender word pairs 
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]
    Return:
        avg_cross_product_embedding: (torch.Tensor) average embedding of cross_products of each word pair's embeddings
    '''
    operator = lambda vector_1, vector_2: torch.cross(
        vector_1.unsqueeze(0), vector_2.unsqueeze(0)
    )[0]
    return average_word_pair_operator(word_pairs, embedder, operator)


def open_json(path: str) -> Dict[Any, Any]:
    '''
    given a path, open a json
    Args:
        path: (string) path to a given json (e.g. classes.json)
    Return:
        json: (json) the corresponding json dictionary
    '''
    with open(path) as f:
        return json.load(f)


def open_csv(path: str) -> pd.DataFrame:
    '''
    given a path, open a csv
    Args:
        path: (string) path to a given csv (e.g. crows_pairs_anonymized.csv)
    Return:
        dataframe: (pd.df) the corresponding pandas dataframe
    '''
    return pd.read_csv(path)


def convert_to_string_list(delim: str, raw_string: str) -> Sequence[str]:
    '''
    split a list of words in string format into an actual list based on a delimeter
    Args:
        delim: (str) delimeter to split by
        raw_string: (str) raw string to split
    Return:
        string_list: (list) corresponding list of strings
    '''
    return [word.strip() for word in raw_string.split(delim)]


def get_class(class_name: Union[str, WordGroup]) -> Sequence[str]:
    '''
    given a path, open a csv
    Args:
        class_name: (string or WordGroup) name of a class in classes.json
    Return:
        class_list: (Sequence[str]) corresponding list of class words
    '''
    global CLASSES_DICT
    if CLASSES_DICT is None:
        CLASSES_DICT = open_json('truera/nlp/fairness/data/classes.json')

    if class_name in CLASSES_DICT:
        if not isinstance(CLASSES_DICT[class_name], list):
            CLASSES_DICT[class_name] = convert_to_string_list(
                ",", CLASSES_DICT[class_name]
            )
        return CLASSES_DICT[class_name]
    else:
        return CLASSES_DICT[class_name.value]


def cosine_similarity(
    vector_1: torch.Tensor, vector_2: torch.Tensor
) -> torch.Tensor:
    '''
    return cosine similarity between two input vectors
    Args:
        vector_1: (torch.Tensor) input vector with shape [1, D]
        vector_2: (torch.Tensor) input vector [1, D]
    Return:
        similarity: (torch.Tensor) the cosine similarity (-1 to 1) between the vectors
    '''
    return nn.CosineSimilarity()(vector_1, vector_2)


def angular_similarity(
    vector_1: torch.Tensor, vector_2: torch.Tensor
) -> torch.Tensor:
    '''
    return angular similarity between two input vectors
    Args:
        vector_1: (torch.Tensor) input vector with shape [1, D]
        vector_2: (torch.Tensor) input vector [1, D]
    Return:
        similarity: (torch.Tensor) the angular similarity (-1 to 1) between the vectors
    '''
    cos_sim = cosine_similarity(vector_1, vector_2)
    pi = torch.acos(torch.zeros(1))
    return 1 - torch.arccos(cos_sim) / pi


def l2_similarity(
    vector_1: torch.Tensor, vector_2: torch.Tensor
) -> torch.Tensor:
    '''
    return 1 - eucldian distance between two input vectors
    Args:
        vector_1: (torch.Tensor) input vector with shape [1, D]
        vector_2: (torch.Tensor) input vector [1, D]
    Return:
        similarity: (torch.Tensor) the l2 similarity (0 to 1) between the vectors
    '''
    vector_1 = nn.functional.normalize(vector_1)
    vector_2 = nn.functional.normalize(vector_2)
    return 1 - torch.dist(vector_1, vector_2)


def spearman_rank_coefficient(
    rank_1: Union[list, np.ndarray], rank_2: Union[list, np.ndarray]
) -> float:
    '''
    Compute rank correlation between two lists of rankings
    More information on accuracy formulation: 
    Args:
        rank_1: (list or np.array) list of ranks (ints), shape = [N,]
        rank_2: (list or np.array) list of ranks (ints), shape = [N,]
    Return:
        rank_correlation: (float) spearman rank correlation coefficient (-1 to 1) between the two rank lists
    '''
    assert (len(rank_1) == len(rank_2))
    distances = [(r1 - r2)**2 for r1, r2 in zip(rank_1, rank_2)]
    n = len(rank_1)
    return 1 - ((6 * sum(distances)) / ((n * (n**2 - 1))))


def print_metrics(metrics: Dict[str, Union[int, float]]) -> None:
    '''
    Given a dictionary of metrics (string key: float or int values), print the keys and (rounded) values 
    Args:
        metrics: (dict) dictionary of metrics (string key: float or int values)
    Return:
        None: print the keys and (rounded) values from metrics
    '''
    for k, v in metrics.items():
        if isinstance(v, np.ndarray) and len(v.shape) > 1:
            print(f"{k}: \n{round_metric(v, 5)}")
            continue
        print(f"{k}: {round_metric(v, 5)}")


def round_metrics(
    metrics: Dict[str, Union[int, float]]
) -> Dict[str, Union[int, float]]:
    '''
    Given a dictionary of metrics (string key: float or int values), print the keys and (rounded) values 
    Args:
        metrics: (dict) dictionary of metrics (string key: float or int values)
    Return:
        new_metrics: (dict) new dictionary with the keys and (rounded) values from metrics
    '''
    new_metrics = {}
    for k, v in metrics.items():
        new_metrics[k] = round_metric(v, 5)
    return new_metrics


def round_metric(
    metric: Union[float, np.ndarray], num_places: Optional[int] = 5
) -> float:
    '''
    Rounds a float metric to a certain number of decimal places
    Args:
        metric: (float) a metric
        num_places: (int) how many decimal places to round number
    Return:
        new_metric: (float) rounded metric
    '''
    if isinstance(metric, np.ndarray):
        return metric.round(num_places)
    return round(metric, num_places)


def get_segmented_data(
    ground_truth: Union[Sequence[int], np.ndarray],
    predicted: Union[Sequence[int], np.ndarray],
    segments: Union[Sequence[int], np.ndarray], segment_id: int
) -> Tuple[Union[Sequence[int], np.ndarray], Union[Sequence[int], np.ndarray]]:
    '''
    Return ground_truth and predicted data corresponding to a given segment_id.
    Args:
        ground_truth: (list or np.array) list of ground truth labels, shape = [N,]
        predicted: (list or np.array) list of model predictions, shape = [N,]
        segments: (list or np.array) list of custom segment ids for each sampe, shape = [N,]
        segment_id: (int) index of a segment to choose to filter ground_truth and predicted data
    Return:
        ground_truth: (list or np.array) list of ground truth labels for samples with the given segment_id 
        predicted: (list or np.array) list of predictions for samples with the given segment_id 
    '''
    assert (len(ground_truth) == len(predicted) == len(segments))
    if segment_id is not None:
        ground_truth = [
            ground_truth[i]
            for i in range(len(ground_truth))
            if segments[i] == segment_id
        ]
        predicted = [
            predicted[i]
            for i in range(len(predicted))
            if segments[i] == segment_id
        ]
    return ground_truth, predicted


def segment_all_data(
    ground_truth: Union[list, np.ndarray], predicted: Union[list, np.ndarray],
    segments: Union[list, np.ndarray]
) -> Dict[Union[str, int], Sequence[int]]:
    '''
    Stratify all ground truth and predicted data by segment_ids.
    Args:
        ground_truth: (list or np.array) list of ground truth labels, shape = [N,]
        predicted: (list or np.array) list of model predictions, shape = [N,]
        segments: (list or np.array) list of custom segment ids for each sampe, shape = [N,]
    Return:
        segmented_data: (dict) map from segment_id to list of ground truth and predicted data for that segment_id
    '''
    assert (len(ground_truth) == len(predicted) == len(segments))
    segmented_data = {}

    for i in range(len(segments)):
        segment_id = segments[i]
        if segment_id not in segmented_data:
            segmented_data[segment_id] = [[ground_truth[i]], [predicted[i]]]
        else:
            segmented_data[segment_id][0].append(ground_truth[i])
            segmented_data[segment_id][1].append(predicted[i])

    segmented_data["total"] = [ground_truth, predicted]
    return segmented_data


def get_segment_metrics_dict(
    segmented_data: Dict[Union[int, str], Tuple[Sequence[int], Sequence[int]]],
    segment_id_to_name: Sequence[Any],
    metrics: Sequence[OutputMetrics],
    num_classes: int,
):
    '''
    Stratify all ground truth and predicted data by segment_ids.
    Args:
        segmented_data: (dict) map from segment_id to list of ground truth and predicted data for that segment_id
        segmentd_id_to_name: (list) each index is a segment_id and the value at that index is the segment_name
        metrics: (list) list of OutputMetric Enums, which are the metrics to be run on the segments
        num_classes: (int) number of classes in the output
    Return:
        segment_metrics_dict: (dict) map from segment_name to metrics for that given segment
    '''
    segment_metrics_dict = {}
    for segment_id in list(segmented_data.keys()):
        for metric in metrics:
            segment_ground_truth, segment_predicted = segmented_data[segment_id]

            metric_name, metric_function = metric.value

            if segment_id != "total":
                segment_name = segment_id_to_name[segment_id]
            else:
                segment_name = segment_id

            if segment_name not in segment_metrics_dict:
                segment_metrics_dict[segment_name] = {}

            segment_metrics_dict[segment_name][metric_name] = metric_function(
                segment_ground_truth, segment_predicted, num_classes
            )

    return segment_metrics_dict


def get_segment_disadvantage_rankings(
    segment_metrics: Dict[str, Any],
    num_segments_to_return: int,
) -> pd.DataFrame:
    '''
    Rank all segments by disadvantage using disparate impact.
    Args:
        segment_metrics: (dict) map from segment name to metrics for that segment
        num_segments_to_return: (int) number of disadvantaged segments to visualize
    Return:
        disadvantaged_segments: (pd.DataFrame) sorted dataframe with segment name and avg. disparate impact score

    '''
    segment_names = sorted(list(segment_metrics.keys()))
    segment_disparate_impact_scores = defaultdict(float)
    num_comparisons = len(segment_names) - 1

    for segment_1_id, segment_1_name in enumerate(segment_names):
        for segment_2_id, segment_2_name in enumerate(segment_names):
            if segment_1_id < segment_2_id:
                segment_disparity_metrics = disparity_wrapper(
                    OutputMetrics.CONFUSION_MATRIX_METRICS, segment_metrics,
                    segment_1_name, segment_2_name
                )
                segment_disparate_impact_scores[segment_1_name
                                               ] += segment_disparity_metrics[
                                                   'disparate_impact_ratio']
                segment_disparate_impact_scores[
                    segment_2_name
                ] += 1 / segment_disparity_metrics['disparate_impact_ratio']
    segment_disadvantge_rankings = sorted(
        [
            [segment_name, disparate_impact_score / num_comparisons]
            for segment_name, disparate_impact_score in
            segment_disparate_impact_scores.items()
        ],
        key=lambda x: x[1]
    )
    return pd.DataFrame(
        segment_disadvantge_rankings[:num_segments_to_return],
        columns=["Segment Name", "Avg. Disparate Impact Score"]
    )


def get_segment_per_text(
    text_list: Sequence[str], segments_dict: Dict[str, Any]
) -> Sequence[str]:
    '''
        Return list of segment names for a given list of text samples
        Args:
            text_list: (Sequence[str]) list of text samples, shape = [N]
        Return:
            segments: (Sequence[str]) corresponding segments for each text sample, shape = [N]
        '''
    segments = []

    for text in text_list:
        words = text.split()
        metadata = defaultdict(int)
        metadata_found = False
        for word in words:
            for segment in segments_dict:
                if word.lower() in segments_dict[segment]:
                    metadata[segment] += 1
                    metadata_found = True
        if metadata_found:
            segment = sorted(
                [(key, value) for key, value in metadata.items()],
                key=lambda x: (x[1], x[0])
            )[-1][0]
            segments.append(segment)
        else:
            segments.append('unclassified')
    return segments


def clean_word(word: str) -> str:
    '''
    Given a word, remove punctuation and make it lower case.
    Args:
        word: (str) input word to be cleaned
    Return:
        clean_word: (str) word cleaned of punctuation and casing
    '''
    punctuation = ["'", ".", "!", "?", ",", ";", ":"]
    word = word.lower()
    for punc in punctuation:
        word = word.replace(punc, "")
    return word


def tokenize_text(
    tokenizer: PreTrainedTokenizer, text_list: Sequence[str],
    sequence_length: int
) -> torch.Tensor:
    '''
    Tokenize a list of sentences.
    Args:
        tokenizer: (PreTrainedTokenizer) a huggingface tokenizer for a given transformer model
        text_list: (list(strs)) list of sentences to be tokenized
        sequence_length: (int) length to pad or truncate each sentence's token sequence to
    Return:
        tokenized_text: (torch.Tensor) all tokenized sentences, shape = (len(text_list), sequence_length)
    '''
    tokenized_text = torch.zeros((len(text_list), sequence_length)
                                ).to(dtype=torch.int)
    for i, text in enumerate(text_list):
        tokens = tokenizer(
            text.lower(),
            padding=True,
            max_length=sequence_length,
            truncation=True,
            return_tensors='pt'
        )['input_ids']
        tokens_seq = nn.functional.pad(
            tokens, (0, sequence_length - tokens.shape[-1])
        )
        tokenized_text[i] = tokens_seq.squeeze().to(dtype=torch.int)
    return tokenized_text


def get_model_inference(
    text: str, tokenizer: PreTrainedTokenizer, model: Any, sequence_length: int
) -> int:
    '''
    Predict label for a given sample text.
    Args:
        text: (str) input text
        tokenizer: (PreTrainedTokenizer) a huggingface tokenizer for a given transformer model
        model: (any transformer) corresponding transformer model
        sequence_length: (int) length to pad or truncate each sentence's token sequence to
    Return:
        prediction: (int) predicted label
    '''
    softmax = nn.Softmax()
    return model(tokenize_text(tokenizer, [text], sequence_length)
                )[0].argmax(-1).item() + 1


def visualize_labels_dist(labels: Union[Sequence[int], np.ndarray]) -> None:
    '''
    Visualize distribution of labels for given samples via a counter.
    Args:
        labels: (Union[list, np.ndarray]) list of sample labels for a given split of a dataset
    Return:
        None: labels distribution (dict) is printed
    '''
    labels_dist = defaultdict(int)
    for i in labels:
        labels_dist[i] += 1
    print(labels_dist)


def accuracy(output: torch.Tensor, target: torch.Tensor) -> float:
    '''
    Calculcate top-1 accuracy given predictions and target
    Args:
        accuracy: (torch.Tensor) predictions with shape()[-1] = N
        target: (torch.Tensor) ground truth labels with shape() = (N)
    Return:
        accuracy: (float) 0-1 measurement of accuracy
    '''
    acc = (output.argmax(-1) == target).float().cpu().numpy()
    return float(100 * acc.sum() / len(acc))


def visualize_confusion_matrix(confusion_matrix: Dict[str, np.ndarray]) -> None:
    '''
    Visualize the confusion matrices for two different segments
    Args:
        confusion_matrix: (dict) contains np.ndarrays for the confusion matrix corresponding to both segments
    Return:
        None: plot and show using plt
    '''
    # TODO: make this produce figures to dispay instead of displaying them whenever this is called

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Confusion Matrix Comparison')

    segment_1_matrix = metrics.ConfusionMatrixDisplay(
        confusion_matrix["segment_1_confusion_matrix"]
    )
    segment_1_matrix.plot(ax=ax1)
    segment_1_matrix.ax_.set_title("Segment 1")
    segment_1_matrix.im_.colorbar.remove()

    segment_2_matrix = metrics.ConfusionMatrixDisplay(
        confusion_matrix["segment_2_confusion_matrix"]
    )
    segment_2_matrix.plot(ax=ax2)
    segment_2_matrix.ax_.set_title("Segment 2")
    segment_2_matrix.im_.colorbar.remove()


def visualize_confusion_matrix_rates(
    confusion_matrix_metrics: Dict[str, Any]
) -> None:
    '''
    Visualize the confusion matrix rates for two different segments
    Args:
        confusion_matrix_metrics: (dict) contains floats and np.ndarrays for the rates corresponding to both segments
    Return:
        None: plot and show using plt
    '''
    comparitive_metrics = [
        "true_positive_rate", "false_positive_rate", "true_negative_rate",
        "false_negative_rate", "positive_predictive_value", "prob_positive"
    ]
    xtick_labels = ['TPR', 'FPR', 'TNR', 'FNR', 'PPV', "P(pred=1)"]
    operator = lambda x: x

    binary_classification = len(
        confusion_matrix_metrics["segment_1_true_positives"]
    ) == 2

    if not binary_classification:
        comparitive_metrics, xtick_labels = comparitive_metrics[:-1
                                                               ], xtick_labels[:
                                                                               -1
                                                                              ]
        operator = lambda x: x.mean()

    segment_1 = []
    segment_2 = []

    for i, comparitive_metric in enumerate(comparitive_metrics):
        segment_1.append(
            operator(
                confusion_matrix_metrics[f"segment_1_{comparitive_metric}"]
            )
        )
        segment_2.append(
            operator(
                confusion_matrix_metrics[f"segment_2_{comparitive_metric}"]
            )
        )

    plt.figure(figsize=(10, 5))

    # Plot 1
    plt.subplot(1, 2, 1)
    bar_positions = np.arange(len(comparitive_metrics))
    width = 0.2

    plt.bar(bar_positions, segment_1, width, label='Segment 1')
    plt.bar(bar_positions + width, segment_2, width, label='Segment 2')

    plt.xticks(bar_positions + width / 2, xtick_labels)

    plt.legend(loc='best')
    plt.title('Confusion Rates')

    if binary_classification:

        # Plot 2
        parity_metric_names = [
            "equality_of_odds_positive", "equality_of_odds_negative",
            "disparate_impact_ratio"
        ]
        parity_xtick_labels = ["EqOpp_POS", "EqOpp_NEG", "DI"]
        parity_metrics = [
            confusion_matrix_metrics[metric_name]
            for metric_name in parity_metric_names
        ]
        plt.subplot(1, 2, 2)
        bar_positions = np.arange(len(parity_metrics))

        plt.bar(bar_positions, parity_metrics, width)

        plt.xticks(bar_positions + width / 2, parity_xtick_labels)

        plt.legend(loc='best')
        plt.title('Statistical Parity Rates')

    plt.show()

    # plt.figure(figsize=(10, 5))
    # bar_positions = np.arange(len(comparitive_metrics))
    # width = 0.2

    # plt.bar(bar_positions, segment_1, width, label='Segment 1')
    # plt.bar(bar_positions + width, segment_2, width, label='Segment 2')

    # plt.xticks(bar_positions + width / 2, xtick_labels)

    # plt.legend(loc='best')
    # plt.title('Confusion Rates')
    # plt.show()


def visualize_confusion_parity(confusion_matrix_metrics):
    '''
    Visualize the confusion matrix parity for two different segments
    Args:
        confusion_matrix_metrics: (dict) contains floats and np.ndarrays for the rates corresponding to both segments
    Return:
        None: plot and show using plt
    '''
    if len(confusion_matrix_metrics["segment_1_true_positives"]) > 2:
        return

    parity_metrics = [
        "equality_of_odds_positive", "equality_of_odds_positive",
        "disparate_impact_ratio"
    ]
    actual, ideal = [], []

    for i, parity_metric in enumerate(parity_metrics):
        actual.append(confusion_matrix_metrics[parity_metric])
        ideal.append(1.0)

    plt.figure(figsize=(10, 5))
    bar_positions = np.arange(len(parity_metrics))
    width = 0.2

    plt.bar(bar_positions, actual, width, label='Actual')
    plt.bar(bar_positions + width, ideal, width, label='Ideal')

    plt.xticks(
        bar_positions + width / 2, ('Eq. Opp Pos', 'Eq. Opp Neg', 'DI Ratio')
    )

    plt.legend(loc='best')
    plt.title('Parity Metrics')
    plt.show()


def visualize_f1_score(f1_score_metrics: Dict[str, Any]) -> None:
    '''
    Visualize f1_score_metrics.
    Args:
        f1_score_metrics: (Dict[str, Any]) f1_score metrics dictionary
    Return:
        None: print dataframe
    '''
    columns = ["Precision", "Recall", "F1_Score"]
    rows = ["Segment_1", "Segment_2", "Disparity", "Total"]

    data = [[0 for _ in range(len(columns))] for _ in range(len(rows))]

    for i in range(len(rows)):
        for j in range(len(columns)):
            row_name = rows[i].lower()
            col_name = columns[j].lower()
            if row_name != "disparity":
                metric_name = f'{row_name}_{col_name}'
            else:
                metric_name = f'{col_name}_{row_name}'
            metric_value = f1_score_metrics[metric_name]
            if isinstance(metric_value, list):
                metric_value = ' '.join([round_metric(x) for x in metric_value])
            else:
                metric_value = round_metric(metric_value)
            data[i][j] = metric_value
    print(pd.DataFrame(data, columns=columns, index=rows))


def visualize_accuracy(accuracy_metrics: Dict[str, Any]) -> None:
    '''
    Visualize accuracy_metrics.
    Args:
        accuracy_metrics_metrics: (Dict[str, Any]) accuracy metrics dictionary
    Return:
        None: print dataframe
    '''
    columns = ["Accuracy"]
    rows = ["Segment_1", "Segment_2", "Disparity", "Total"]

    data = [[0 for _ in range(len(columns))] for _ in range(len(rows))]

    for i in range(len(rows)):
        row_name = rows[i].lower()
        col_name = columns[0].lower()
        if row_name != "disparity":
            metric_name = f'{row_name}_{col_name}'
        else:
            metric_name = f'{col_name}_{row_name}'
        metric_value = accuracy_metrics[metric_name]
        if isinstance(metric_value, list):
            metric_value = ' '.join([round_metric(x) for x in metric_value])
        else:
            metric_value = round_metric(metric_value)
        data[i][0] = metric_value
    print(pd.DataFrame(data, columns=columns, index=rows))
