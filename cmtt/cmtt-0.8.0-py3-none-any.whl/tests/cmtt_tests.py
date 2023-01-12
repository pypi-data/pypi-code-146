import unittest
from cmtt.data import *
from cmtt.preprocessing import *

class CMTTTestCase(unittest.TestCase):
  def setUp(self):
    self.load_url = load_url
    self.list_dataset_keys = list_dataset_keys
    self.WordT = WordTokenizer()
    self.WordpieceT = Wordpiece_tokenizer()
    self.WhitespaceT = WhitespaceTokenizer()

  def test_data_load_url_1(self):
    """Test data load_url function 1"""
    result = self.load_url('https://world.openfoodfacts.org/api/v0/product/5060292302201.json')
    self.assertEqual(result['code'], "5060292302201")

  def test_data_load_url_2(self):
    """Test data load_url function 2"""
    result = self.load_url('https://gist.githubusercontent.com/rnirmal/e01acfdaf54a6f9b24e91ba4cae63518/raw/6b589a5c5a851711e20c5eb28f9d54742d1fe2dc/datasets.csv')
    self.assertEqual(result['about'][20], "Tate Collection metadata")
    self.assertEqual(len(result['about']), 61)

  def test_list_dataset_keys(self):
    """Test list_dataset_keys function"""
    keys = self.list_dataset_keys()
    self.assertEqual(keys, ['url', 'id', 'name', 'format', 'language', 'task', 'credits', 'source', 'last_modified'])

  def test_whitespace_tokenize(self):
    """Test whitespace tokenize function"""
    text = "Hello world! This a python code. Let's activate"
    result = self.WhitespaceT.tokenize(text)
    self.assertEqual(len(result), 8)
  
  def test_word_tokenize(self):
    """Test word tokenize function"""
    text = "This Python interpreter is in a conda environment, but the environment has not been activated.  Libraries may fail to load.  To activate this environment"
    result = self.WordT.tokenize(text)
    self.assertEqual(len(result), 27)

  def test_wordpiece_tokenize(self):
    """Test wordpiece tokenize function"""
    text = "This Python interpreter is in a conda environment, but the environment has not been activated.  Libraries may fail to load.  To activate this environment"
    result = self.WordpieceT.tokenize(text)
    self.assertEqual(len(result), 32)

  def test_search(self):
    """Test wordpiece tokenize function"""
    text = "This Python interpreter is in a conda environment, but the environment has not been activated.  Libraries may fail to load.  To activate this environment"
    instances, list_instances = search_word(text, 'this', tokenize = True, width = 3)
    self.assertEqual(instances, 2)
  
if __name__ == '__main__':
  unittest.main()