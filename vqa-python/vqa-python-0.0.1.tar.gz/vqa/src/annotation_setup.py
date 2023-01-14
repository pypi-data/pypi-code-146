import json
import unidecode
import numpy as np
from vqa.src import root_dir

class AnnotationSetup():
    def __init__(self) -> None:
        self.ROOT_dir = root_dir.find_ROOT_dir()
        self.dictionary = json.load(open(f"{self.ROOT_dir}/storage/dictionary.json", "r"))
        self.restore_dictionary = {y: x for x, y in self.dictionary.items()}

    def language_check(self, question):
        question = question.replace("\u3000", "")
        vocal = 'aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
        for t in question:
            if t not in vocal:
                return "ja"
        if unidecode.unidecode(question) != question and "résumé" not in question and "café" not in question:
            return "vi"
        else:
            return "en"
    
    def text_preprocessing(self, text):
        rep = '!#$%&\()*+,./:;=?@[\\]^_{|}~'
        for r in rep:
            text = text.replace(r, "")
        return text.lower()
    
    def answer_embedding(self, answer):
        source = np.zeros((60))
        split_answer = answer.split(" ")
        i = 0
        for ans in split_answer:
            if self.language_check(ans) == "ja":
                for cha in ans:
                    if cha in self.dictionary:
                        source[i] = self.dictionary[cha]
                        i+=1
                    else:
                        source[i] = 3
                        i+=1
            else:
            # charac = answer.split(" ")
            # for i, cha in enumerate(charac):
                if ans in self.dictionary:
                    source[i] = self.dictionary[ans]
                    i+=1
                else:
                    source[i] = 3
                    i+=1
        return source
