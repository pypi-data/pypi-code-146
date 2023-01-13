from sklearn import metrics
from sklearn.model_selection import train_test_split

class trainer:

    def __init__(self, model_type):

        settings = {
            "regression" : ["LinearRegression","MLPRegressor", "KNeighborsRegressor", "SVR", "DecisionTreeRegressor", "RandomForestRegressor", "GradientBoostingRegressor"],
            "classification" :  ["LogisticRegression","MLPClassifier", "KNeighborsClassifier", "SVC", "DecisionTreeClassifier", "RandomForestClassifier", "GradientBoostingClassifier"]
        }

        self._model_list = setings[model_type]

    def models(self):
        return self._model_list

    def add_model(self, model):
        self._model_list.append(model)

    def remove_model(self, model):
        if model in self._model_list:
            self._model_list.pop(model)
        return



def select_best_model(data, type_model=''):

    """Train different models by selecting the type_model by clasifitation
    or regrresion model.
    splits the dataframe and generate a dictionary with the metrics of each model
    """
    results = {}
    X_train, X_test, y_train, y_test = train_test_split(data.drop(columns = ['target']), data.target, test_size=0.33, random_state=42)

    if type_model == 'clasification':
        from sklearn.linear_model import LogisticRegression
        from sklearn.neural_network import MLPClassifier
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.svm import SVC
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

        modelsname = ["LogisticRegression","MLPClassifier", "KNeighborsClassifier", "SVC",
                         "DecisionTreeClassifier", "RandomForestClassifier", "GradientBoostingClassifier"]
        models = [LogisticRegression(random_state=0, max_iter = 10000),KNeighborsClassifier(n_neighbors=5),SVC(gamma=2, C=1, probability=True),DecisionTreeClassifier(max_depth=5),RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),MLPClassifier(alpha=1, max_iter=1000),GradientBoostingClassifier()]

        i=0
        for model in models:
            model.fit(X_train, y_train)
            fpr, tpr, thresholds = metrics.roc_curve(y_test, model.predict_proba(X_test)[:,1])
            y_pred = model.predict(X_test)
            auc = metrics.auc(fpr, tpr)
            accuracy = metrics.accuracy_score(y_test, y_pred)
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)
            results[modelsname[i]] = {'train_score': train_score,
                                    'test_score': test_score,
                                    'AUC_ROC': auc,
                                    'accuracy': accuracy}
            print(f'training model: {modelsname[i]}')
            print(f'train_score: {train_score}')
            print(f'test_score: {test_score}')
            print(f'AUC_ROC: {auc}')
            print(f'accuracy: {accuracy}')
            i=i+1

    if type_model == 'regression':
        from sklearn.linear_model import LinearRegression
        from sklearn.neural_network import MLPRegressor
        from sklearn.neighbors import KNeighborsRegressor
        from sklearn.svm import SVR
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

        modelsname = ["LinearRegression","MLPRegressor", "KNeighborsRegressor", "SVR",
                         "DecisionTreeRegressor", "RandomForestRegressor", "GradientBoostingRegressor"]

        models = [LinearRegression(random_state=0, max_iter = 10000),MLPRegressor(n_neighbors=5),KNeighborsRegressor(gamma=2, C=1, probability=True),SVR(max_depth=5),DecisionTreeRegressor(max_depth=5, n_estimators=10, max_features=1),RandomForestRegressor(alpha=1, max_iter=1000),GradientBoostingRegressor(max_iter=1000)]
        i=0
        for model in models:
            model.fit(X_train, y_train)
            y_pred = model.predict(y_test)
            mse = metrics.mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = metrics.r2_score(y_test, y_pred)
            mae = metrics.absolute_mean_error(y_test, y_pred)
            results[modelsname[i]] = {'MSE': mse,
                                    'MAE':mae,
                                    'RMSE': rmse,
                                    'r2_score': r2}
            print(f'training model: {modelsname[i]}')
            print(f'MSE: {mse}')
            print(f'MAE: {mae}')
            print(f'RMSE: {rmse}')
            print(f'r2_score: {r2}')
            i=i+1
