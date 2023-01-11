from typing import Union

import torch

from truera.nlp.fairness.utils import cosine_similarity
from truera.nlp.fairness.utils import get_class
from truera.nlp.fairness.utils import get_embedding
from truera.nlp.fairness.utils import spearman_rank_coefficient


def direct_bias(
    class_1: str, class_2: str, query: str,
    embedder: Union["gensim.models.KeyedVectors", list]
) -> float:
    '''
    Compute direct bias by comparing a query word to two class vectors using cosine similarity.
    Original formulation of this metric (DB) found in this paper: https://proceedings.neurips.cc/paper/2016/file/a486cd07e4ac3d270571622f4f316ec5-Paper.pdf

    Args:
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "male")
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "female")
        query: (str) a word that will be compared to class_1 and class_2 words
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]    
    Return:
        db_score: (float) the direct bias measurement from comparing query to class1
    '''
    embedding_1 = get_embedding(class_1, embedder)
    embedding_2 = get_embedding(class_2, embedder)
    query = get_embedding(query, embedder)
    return cosine_similarity(embedding_1, query).item(
    ) - cosine_similarity(embedding_2, query).item()


def word_embedding_analogy(
    class_1: str, class_2: str, queries_1: list, queries_2: list,
    embedder: Union["gensim.models.KeyedVectors", list]
) -> float:
    '''
    Compute difference in average cosine similarity of words in class_1 query_1 and query_2 words compared to class_2.
    Original formulation of this metric (WEAT) found in this paper: https://www.science.org/doi/10.1126/science.aal4230
    Args:
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "male")
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "female")
        queries_1: (list) list of strings word that will be compared to class_1 and class_2 words
        queries_2: (list) list of strings word that will be compared to class_1 and class_2 words
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]    
    Return:
        weat_score: (float) difference in word analogies between classes and queries
    '''

    def word_embedding_analogy_helper(
        class_word: str, queries_1: list, queries_2: list
    ) -> torch.Tensor:
        class_embedding = get_embedding(class_word, embedder)
        cos_sim_results_1 = torch.zeros(len(queries_1))
        cos_sim_results_2 = torch.zeros(len(queries_2))
        for i, q1 in enumerate(queries_1):
            embedding_1 = get_embedding(q1, embedder)
            cos_sim_results_1[i] = cosine_similarity(
                class_embedding, embedding_1
            )
        for i, q2 in enumerate(queries_2):
            embedding_2 = get_embedding(q2, embedder)
            cos_sim_results_2[i] = cosine_similarity(
                class_embedding, embedding_2
            )
        return torch.mean(cos_sim_results_1) - torch.mean(cos_sim_results_2)

    analogy_score_1 = 0
    analogy_score_2 = 0
    for i, class_1_word in enumerate(class_1):
        analogy_score_1 += word_embedding_analogy_helper(
            class_1_word, queries_1, queries_2
        ).item()
    for i, class_2_word in enumerate(class_2):
        analogy_score_2 += word_embedding_analogy_helper(
            class_2_word, queries_1, queries_2
        ).item()
    return analogy_score_1 - analogy_score_2


def embedding_coherence_test(
    class_1: str, class_2: str, queries: list,
    embedder: Union["gensim.models.KeyedVectors", list]
) -> list:
    '''
    Compute correlation of ranks of words in queries to class_1 and class_2
    Original formulation of this metric (ECT) found in this paper: http://proceedings.mlr.press/v89/dev19a/dev19a.pdf   
    Args:
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "male")
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "female")
        queries: (list) list of strings (words) that will be compared to class_1 and class_2 words
        embedder: (gensim.model OR list) either a gensim model, or HuggingFace [Tokenizer, Model]    
    Return:
        ect_score: (float) correlation (-1 to 1) of ranks for class_1 and class_2 to words in queries
    '''

    def rank_helper(class_name: str, queries: list) -> list:
        cos_sim_results = []
        class_embedding = get_embedding(class_name, embedder)

        for i, q in enumerate(queries):
            query_embedding = get_embedding(q, embedder)
            cos_sim_results.append(
                (cosine_similarity(class_embedding, query_embedding), i)
            )
        cos_sim_results.sort(key=lambda x: -x[0])
        return [rank for cos_sim, rank in cos_sim_results]

    rank_1 = rank_helper(class_1, queries)
    rank_2 = rank_helper(class_2, queries)

    return spearman_rank_coefficient(rank_1, rank_2)


def relational_inner_product_association(
    class_1: str, class_2: str, query: str,
    embedder: Union["gensim.models.KeyedVectors", list]
) -> float:
    '''
    Compute cosine similarity of a given query with the difference vector between two classes
    Original formulation of this metric (RIPA) found in this paper: https://arxiv.org/pdf/1903.03862.pdf
    Args:
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "male")
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "female")
        query: (str) a word or the class_name for a words belonging to a class (e.g. "occupations")
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]    
    Return:
        ripa_score: (float) difference in word analogies between classes and queries
        
    For formula information
    '''
    embedding_1 = get_embedding(class_1, embedder)
    embedding_2 = get_embedding(class_2, embedder)
    query_embedding = get_embedding(query, embedder)

    difference_vector = (embedding_1 -
                         embedding_2) / torch.norm(embedding_1 - embedding_2)
    query_embedding = query_embedding / torch.norm(query_embedding)
    return torch.dot(query_embedding.squeeze(),
                     difference_vector.squeeze()).item()


def neighborhood_bias_metric(
    class_1: str, class_2, query: str, k,
    embedder: Union["gensim.models.KeyedVectors", list]
) -> float:
    '''
    Compare how many of nearest words for query are part of class_1 vs. class_2
    Original formulation of this metric (NBM) found in this paper: https://arxiv.org/pdf/1903.03862.pdf
    Args:
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "male")
        class_1: (str) a word or the class_name for a words belonging to a class (e.g. "female")
        query: (str) a word or the class_name for a words belonging to a class (e.g. "occupations")
        k: (int) number of nearest neighbor words to fetch for querry
        embedder: (KeyedVectors OR list) either a gensim model, or HuggingFace [Tokenizer, Model]    
    Return:
        nbm_score: (float) difference in word analogies between classes and queries
        
    For formula information
    '''
    class_1_words = get_class(class_1)
    class_2_words = get_class(class_2)

    query = get_embedding(query, embedder)
    neighbors = [
        (word, cosine_similarity(query, get_embedding(word, embedder)))
        for word in class_1_words + class_2_words
    ]
    topk = sorted(neighbors, key=lambda x: -x[1])[:k]

    class_1_count, class_2_count = 0, 0
    for word, sim in topk:
        if word in class_1_words:
            class_1_count += 1
        elif word in class_2_words:
            class_2_count += 1
    return abs(class_1_count - class_2_count) / (class_1_count + class_2_count)
