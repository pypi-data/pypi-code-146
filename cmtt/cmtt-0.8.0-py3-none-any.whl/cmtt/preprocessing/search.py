from cmtt.preprocessing.tokenizer import WordTokenizer

def search_word(corpus, word, tokenize = False, width = 10):
  """
    Returns number of instances and list of all instances of the target word in corpus,
    :param corpus: the corpus in which the target words is to be searched
    :type corpus: list or str
    :param word: the target word
    :type text: str
    :param tokenize: option to tokenize the corpus or not
    :type tokenize: bool
    :param width: number of words/characters in the line
    :type width: int
    :return: number of instances and list of all instances of the target word in corpus
    :rtype: int, list
  """

  if(tokenize):
    WordT = WordTokenizer()
    if(type(corpus) == list):
      corpus = ' '.join(corpus)
      corpus = WordT.tokenize(corpus)
    else:
      corpus = WordT.tokenize(corpus)

  instances = 0
  list_instances = []
  lwidth = width//2
  rwidth = width - width//2
  for i in range(0, len(corpus)):
    if(word.lower() == corpus[i].lower()):
      instances += 1
      list_instances.append(corpus[(i - lwidth) if (i - lwidth) >= 0 else 0 : (i + rwidth) if (i + rwidth) <= len(corpus) else len(corpus)])

  print("Found the following " + str(instances) + " instances of " + word + " in corpus:")
  for i in list_instances:
    print(' '.join(i))

  return instances, list_instances