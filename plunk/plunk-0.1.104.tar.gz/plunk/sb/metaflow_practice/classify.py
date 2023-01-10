from metaflow import FlowSpec, step
from sklearn.datasets import make_classification


def mk_Xy():
    X, y = make_classification(
        n_features=2,
        n_redundant=0,
        n_informative=2,
        random_state=1,
        n_clusters_per_class=1,
    )
    return X, y


class ClassifierTrainFlow(FlowSpec):
    @step
    def start(self):  # A
        from sklearn.model_selection import train_test_split

        X, y = mk_Xy()
        (self.X_train, self.X_test, self.y_train, self.y_test,) = train_test_split(
            X, y, test_size=0.4, random_state=0
        )
        self.next(self.train_knn, self.train_svm)

    @step
    def train_knn(self):  # B
        from sklearn.neighbors import KNeighborsClassifier

        self.model = KNeighborsClassifier()
        self.model.fit(self.X_train, self.y_train)
        self.next(self.choose_model)

    @step
    def train_svm(self):  # B
        from sklearn import svm

        self.model = svm.SVC(kernel='poly')  # D
        self.model.fit(self.X_train, self.y_train)
        self.next(self.choose_model)

    @step
    def choose_model(self, inputs):  # B
        def score(inp):
            return inp.model, inp.model.score(inp.X_test, inp.y_test)

        self.results = sorted(map(score, inputs), key=lambda x: -x[1])
        self.model = self.results[0][0]
        self.next(self.end)

    @step
    def end(self):  # C
        print('Scores:')
        print('\n'.join('%s %f' % res for res in self.results))


if __name__ == '__main__':
    ClassifierTrainFlow()
