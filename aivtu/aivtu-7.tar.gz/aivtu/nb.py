from  sklearn import datasets
iris = datasets.load_iris()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size = 0.2)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test) 

from sklearn.metrics import accuracy_score 
print('Split {0} rows into train={1} and test={2} rows'.format(len(iris.data),len(X_train), len(X_test)))
print("Accuracy : ", accuracy_score(y_test,y_pred))
