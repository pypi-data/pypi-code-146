import pytest
from review_recommender.inverted_files import *

QUERY2FREQS = {'item1':              {'token1': 10, 'token2': 5, 'token3': 7, 'token4': 15 },
               'itemSimilarto1' :    {'token1': 5, 'token2': 7, 'token3': 10, 'token4': 20, 'token5': 4 },
               'itemDifferentfrom1' : {'token1': 1, 'token6': 17, 'token7': 2, 'token8': 12 }}

def test_inverted_files():
    invertedFile = InvertedFile()
    invertedFile.add('item1', QUERY2FREQS['item1'])
    invertedFile.add('itemDifferentfrom1', QUERY2FREQS['itemDifferentfrom1'])

    items2Score = invertedFile.getSimilar(QUERY2FREQS['itemSimilarto1'])
    
    assert items2Score['item1'] > items2Score['itemDifferentfrom1']

def test_inverted_files_empty():
    invertedFile = InvertedFile()

    items2Score = invertedFile.getSimilar(QUERY2FREQS['itemSimilarto1'])
    
    assert not len(items2Score)