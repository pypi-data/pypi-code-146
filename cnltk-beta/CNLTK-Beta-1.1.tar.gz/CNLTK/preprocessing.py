ceb_stopwords = [ "ako", "amua", "ato", "busa", "ikaw", "ila", "ilang", "imo", "imong", "iya", "iyang", "kaayo", "kana", "kaniya", "kaugalingon", 
                 "kay", "kini", "kinsa", "kita", "lamang", "mahimong", "mga", "mismo", "nahimo", "nga", "pareho", "pud", "sila", "siya", "unsa" ]


def remove_stopwords(text):
    return " ".join([word for word in text.split() if word.lower() not in ceb_stopwords])

def _POS(sentence):
    process_sents = []
    
    sentence = sentence.lower()
    
    sentence = remove_stopwords(sentence)
        
    process_sents.append(sentence.split())
    
    return process_sents



puncts = [ "!", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "]", "^",
    "_", "`", "{", "|", "}", "~" ]

def remove_puncts(text):
    return " ".join([word for word in text.split() if word not in puncts])

def _NER(sentence):
    process_sents = []
    
    sentence = remove_puncts(sentence)
    
    process_sents.append(sentence.split())
    
    return process_sents