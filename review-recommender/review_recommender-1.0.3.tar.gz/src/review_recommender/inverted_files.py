from __future__ import annotations
import math
from dataclasses import dataclass


@dataclass
class ItemReference:
    item: object
    length_squared: float

    def __hash__(self) -> int:
        return self.item.__hash__()

@dataclass
class TokenOccurence:
    item_ref: ItemReference
    count: int


@dataclass
class TokenInfo:
    idf: float
    occ_list: list[TokenOccurence]


class InvertedFile:
    """
    A class that models a basic inverted file, to witch you can add
    key value pairs of tokens to their count associated with an item
    (could be a document or anything else, the only condition is that
    it is hashable). 
    Can be queried to get similar items based on cosine similarity.
    """

    def __init__(self):
        self.token2Items: dict[str, TokenInfo] = {}
        self.totalItems = 0

    def add(self, item, token_freq: dict[str, int]):
        """
        Add an item with its associated token frequencies:

        Args:
            token_freq(dict[str, int]): pairs of token and their count
        """
        for token, count in token_freq.items():
            if not token in self.token2Items:
                self.token2Items[token] = TokenInfo(idf=0, occ_list=[])
            itemRef = ItemReference(item, length_squared=0)
            self.token2Items[token].occ_list.append(TokenOccurence(itemRef, count))
            self.totalItems += 1

    def calculateIDF(self):
        for tokenInfo in self.token2Items.values():
            tokenInfo.idf = math.log2(self.totalItems/len(tokenInfo.occ_list))
        
        for tokenInfo in self.token2Items.values():
            idf = tokenInfo.idf
            for tokenOccurrence in tokenInfo.occ_list:
                count = tokenOccurrence.count
                tokenOccurrence.item_ref.length_squared += (idf * count)**2

    def getSimilar(self, tokenFreqs):
        """
        Returns a  list of items that are similar to a query, that is 
        a new dictionary of token with their count.

        Args:
            tokenFreqs(dict[str, int]): pairs of token and their count
        """
        self.calculateIDF()
        retrievedRef2score: dict[ItemReference, float] = {}
        token2weights = {}
        for token, count in tokenFreqs.items():
            if not token in self.token2Items: continue
            tokenInfo = self.token2Items[token]
            idf = tokenInfo.idf
            weight = count * idf
            token2weights[token] = weight
            occList = tokenInfo.occ_list
            for occurrence in occList:
                itemRef = occurrence.item_ref
                countInItem = occurrence.count
                if not itemRef in retrievedRef2score: retrievedRef2score[itemRef] = 0
                retrievedRef2score[itemRef] += weight * idf * countInItem

        queryLengthSquared = 0
        for token, weight in token2weights.items():
            queryLengthSquared += weight**2
        queryLength = math.sqrt(queryLengthSquared)

        retrievedItem2score = {}
        for retrieved, score in retrievedRef2score.items():
            length = math.sqrt(retrieved.length_squared)
            retrievedItem2score[retrieved.item] = score/(queryLength * length)
        
        return retrievedItem2score
    
    def dump(self):
        print(self.token2Items.keys())
