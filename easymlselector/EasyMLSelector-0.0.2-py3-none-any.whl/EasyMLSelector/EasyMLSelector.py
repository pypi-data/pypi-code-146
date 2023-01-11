import warnings 

from sklearn.utils import all_estimators
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, r2_score, completeness_score

warnings.filterwarnings('ignore')

class ModelSelector():
    def __init__(self, type_filter=None, verbose=False, Xy_tuple=None):
        self.results_book = []
        self.best_model = None
        self.verbose= verbose
        self.type_filter = type_filter

        SK_ALL = all_estimators(type_filter=type_filter)
        # ‘classifier’, ‘regressor’, ‘cluster’ and ‘transformer’
        self.model_names    = [sk[0] for sk in SK_ALL]
        self.models         = [sk[1] for sk in SK_ALL]

        if self.verbose:
            print(type_filter+"s",'initialized with',len(self.models),'models')
            if not Xy_tuple:
                print('Remember to train_test_split using this.split or this.fill')
        
        if Xy_tuple and len(Xy_tuple) == 4:
            self.fill(Xy_tuple[0], Xy_tuple[1], Xy_tuple[2], Xy_tuple[3])

        if Xy_tuple and len(Xy_tuple) == 2:
            self.split(Xy_tuple[0],Xy_tuple[1])
    
    def split(self, X, y):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.5, shuffle=False)
        if self.verbose:
            print('generated a 50/50 train-test-split')

    def fill(self, X_train,y_train,X_test,y_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def training_and_scoring(self, i, MN=None):
        name = self.model_names[i] if not MN else MN[1]

        if self.verbose:
            print('Training',name,'. . .')

        try:
            model = self.models[i]() if not MN else MN[0]()
            model.fit(X=self.X_train, y=self.y_train)
            scores = model.score(self.X_test, self.y_test)
            entry = {'name':name, 
                     'score':scores, 
                     'model':model}

            self.results_book.append(entry)
            if self.verbose:
                print(scores)
        except Exception as e:
            if self.verbose:
                print(name, 'FAIL', str(e)[:100])
            
        if self.verbose:
            print('-'*20)
    
    def model_loop(self,):
        print('Looping all models . . . ')
        for i in range(len(self.models)):
            self.training_and_scoring(i)
        
        self.results_book.sort(key=lambda x: x['score'], reverse=True)
        self.best_model = self.results_book[0]['model']
        if self.verbose:
            print(".best_model: ", self.results_book[0])
    
    def test_best(self,m=None):
        model = m if m else self.best_model

        if self.verbose:
            print('testing best model . . .')
            print(self.results_book[0]['name'])
        preds = model.predict(self.X_test)

        if self.type_filter == "classifier":
            print(classification_report(preds, self.y_test))
        elif self.type_filter == "regressor":
            print("R2 score:", r2_score(self.y_test, preds))
        elif self.type_filter == "cluster":
            print("Completeness:", completeness_score(self.y_test, preds))
        else:
            print("sklearn score:", model.score(self.X_test, self.y_test))
    
    def __getitem__(self, item):
        return self.results_book[item]
    
    def __len__(self):
        return len(self.results_book)
    
