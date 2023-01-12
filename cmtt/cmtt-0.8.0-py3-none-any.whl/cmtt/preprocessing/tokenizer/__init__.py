import unicodedata
import os
import re

def convert_to_unicode(text):
  """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
  if isinstance(text, str):
    return text
  elif isinstance(text, bytes):
    return text.decode("utf-8", "ignore")
  else:
    raise ValueError("Unsupported string type: %s" % (type(text)))

##################################################
# Whitespace Tokenizer
##################################################
class WhitespaceTokenizer(object):
  def tokenize(self, text):
    text = text.strip()
    if not text:
      return []
    tokens = text.split()
    return tokens

  def detokenize(self, tokens):
    if type(tokens) is list:
      return ' '.join(tokens)
    else:
      raise TypeError('Tokens needs to be of type list. Expected type list but got type ' + str(type(tokens)))

##################################################
# Word Tokenizer
##################################################
class WordTokenizer(object):
  """Runs basic tokenization (punctuation splitting, lower casing, etc.)."""

  def __init__(self, do_lower_case=True):
    """Constructs a BasicTokenizer.
    Args:
      do_lower_case: Whether to lower case the input.
    """
    self.do_lower_case = do_lower_case

  def tokenize(self, text):
    """Tokenizes a piece of text."""
    text = convert_to_unicode(text)
    text = self._clean_text(text)

    WhitespaceT = WhitespaceTokenizer()
    orig_tokens = WhitespaceT.tokenize(text)
    split_tokens = []
    for token in orig_tokens:
      if self.do_lower_case:
        token = token.lower()
        token = self._run_strip_accents(token)
      split_tokens.extend(self._run_split_on_punc(token))

    output_tokens = WhitespaceT.tokenize(" ".join(split_tokens))
    return output_tokens

  def detokenize(self, tokens):
    if type(tokens) is list:
      text = ""
      for i in tokens:
        if len(i) == 1:
          if self._is_punctuation(i):
            text += i
          else:
            text += " " + i
        else:
          text += " " + i
      return text.strip()    
    else:
      raise TypeError('Tokens needs to be of type list. Expected type list but got type ' + str(type(tokens)))

  def _run_strip_accents(self, text):
    """Strips accents from a piece of text."""
    text = unicodedata.normalize("NFD", text)
    output = []
    for char in text:
      cat = unicodedata.category(char)
      if cat == "Mn":
        continue
      output.append(char)
    return "".join(output)

  def _run_split_on_punc(self, text):
    """Splits punctuation on a piece of text."""
    chars = list(text)
    i = 0
    start_new_word = True
    output = []
    while i < len(chars):
      char = chars[i]
      if self._is_punctuation(char):
        output.append([char])
        start_new_word = True
      else:
        if start_new_word:
          output.append([])
        start_new_word = False
        output[-1].append(char)
      i += 1

    return ["".join(x) for x in output]

  def _clean_text(self, text):
    """Performs invalid character removal and whitespace cleanup on text."""
    output = []
    for char in text:
      cp = ord(char)
      if cp == 0 or cp == 0xfffd or self._is_control(char):
        continue
      if self._is_whitespace(char):
        output.append(" ")
      else:
        output.append(char)
    return "".join(output)

  def _is_whitespace(self, char):
    """Checks whether `chars` is a whitespace character."""
    # \t, \n, and \r are technically contorl characters but we treat them
    # as whitespace since they are generally considered as such.
    if char == " " or char == "\t" or char == "\n" or char == "\r":
      return True
    cat = unicodedata.category(char)
    if cat == "Zs":
      return True
    return False

  def _is_control(self, char):
    """Checks whether `chars` is a control character."""
    # These are technically control characters but we count them as whitespace
    # characters.
    if char == "\t" or char == "\n" or char == "\r":
      return False
    cat = unicodedata.category(char)
    if cat in ("Cc", "Cf"):
      return True
    return False

  def _is_punctuation(self, char):
    """Checks whether `chars` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
        (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
      return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
      return True
    return False

##################################################
# Wordpiece Tokenizer
##################################################
def load_vocab_list():
  """Loads a vocabulary file into a dictionary."""
  vocab = []
  path = os.path.dirname(os.path.realpath(__file__))
  f = open(os.path.join(path, "vocab_2.txt"), 'r')
 
  with f as reader:
    while True:
      token = convert_to_unicode(reader.readline())
      if not token:
        break
      token = token.strip()
      vocab.append(token)
  return vocab 

class Wordpiece_tokenizer(object):
  def __init__(self, vocab = load_vocab_list()):
    self.vocab = vocab

  def encode_word(self, word):
    tokens = []
    while len(word) > 0:
      i = len(word)
      while i > 0 and word[:i].lower() not in self.vocab:
        i -= 1
      if i == 0:
        return ["[UNK]"]
      tokens.append(word[:i])
      word = word[i:]
      if len(word) > 0:
        word = f"##{word}"
    return tokens

  def tokenize(self, text):
    """
      Tokenizes a piece of text into its word pieces.
      For example:
        input = "unaffable"
        output = ["un", "##aff", "##able"]
      Args:
        text: A single token or whitespace separated tokens. This should have already been passed through `BasicTokenizer.
      Returns:
        A list of wordpiece tokens.
    """
    text = text.strip()
    text = re.findall(r"[\w]+|[^\s\w]", text)
    encoded_words = [self.encode_word(word) for word in text]
    return sum(encoded_words, [])

  def detokenize(self, tokens):
    if type(tokens) is list:
      text = ""
      for i in tokens:
        if len(i) == 1:
          if self._is_punctuation(i):
            text += i
          else:
            text += " " + i
        elif "##" in i:
          text += i[2:]
        else:
          text += " " + i
      return text.strip()    
    else:
      raise TypeError('Tokens needs to be of type list. Expected type list but got type ' + str(type(tokens)))

  def _is_punctuation(self, char):
    """Checks whether `chars` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
        (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
      return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
      return True
    return False

##################################################
# Devanagari Tokenizer
##################################################
class DevanagariTokenizer(object):
  def word_tokenize(self, text):
    text = text.strip()
    processed_text = ""
    for i in text:
      if self._is_punctuation(i):
        processed_text += " " + i
      else:
        processed_text += i
    
    tokens = processed_text.split(" ")
    return tokens        

  def character_tokenize(self, text):
    text = text.strip()
    if not text:
      return []
    tokens = re.findall(r"[\w]+|[^\s\w]", text)
    return tokens

  def word_detokenize(self, tokens):
    if type(tokens) is list:
      text = ""
      for i in tokens:
        if len(i) == 1:
          if self._is_punctuation(i):
            text += i
          else:
            text += " " + i
        else:
          text += " " + i
      return text.strip()   
    else:
      raise TypeError('Tokens needs to be of type list. Expected type list but got type ' + str(type(tokens)))

  def _is_punctuation(self, char):
    """Checks whether `chars` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
        (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
      return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
      return True
    return False