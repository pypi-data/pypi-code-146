import numpy as np
from metaflow import FlowSpec, step
from py2store import myconfigs
from graze import graze
import soundfile as sf
from dol import FilesOfZip, wrap_kvs, filt_iter
from io import BytesIO


DFLT_FEATURIZER = lambda chk: np.abs(np.fft.rfft(chk))


config_filename = 'phone_digits_block.json'
DFLT_LOCAL_SOURCE_DIR = myconfigs.get_config_value(config_filename, 'local_source_dir')


def mk_fvs(chk_tags, featurizer=DFLT_FEATURIZER):
    for chk, tag in chk_tags:
        yield featurizer(chk), tag


class ClassifierTrainFlow(FlowSpec):
    @step
    def start(self):  # A
        from odat.mdat.phone_digits_block import mk_dacc

        dacc = mk_dacc()
        self.chk_tag = dacc.chk_tag_gen()

        X, y = list(chk_tag)
        (
            self.train_data,
            self.test_data,
            self.train_labels,
            self.test_labels,
        ) = train_test_split(X, y, test_size=0.4, random_state=0)
        self.next(self.mk_fvs)

    @step
    def mk_fvs(self):  # B
        self.fvs = mk_fvs(self.chk_tag)

        fvs_train = np.array(list(map(DFLT_FEATURIZER, list_chks[:100])))
        # from sklearn.neighbors import KNeighborsClassifier

        # self.model = KNeighborsClassifier()
        # self.model.fit(self.train_data, self.train_labels)
        # self.next(self.choose_model)

    @step
    def train_test(self):
        pass

    @step
    def train_svm(self):  # B
        from sklearn import svm

        self.model = svm.SVC(kernel='poly')  # D
        self.model.fit(self.train_data, self.train_labels)
        self.next(self.choose_model)

    @step
    def choose_model(self, inputs):  # B
        def score(inp):
            return inp.model, inp.model.score(inp.test_data, inp.test_labels)

        self.results = sorted(map(score, inputs), key=lambda x: -x[1])
        self.model = self.results[0][0]
        self.next(self.end)

    @step
    def end(self):  # C
        print('Scores:')
        print('\n'.join('%s %f' % res for res in self.results))


if __name__ == '__main__':
    ClassifierTrainFlow()
