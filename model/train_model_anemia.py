import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, ConfusionMatrixDisplay

from process.preprocess import preprocessing

def model_train_for_anemia():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', 'data', 'anemia.csv')
    data = pd.read_csv(file_path)

    target = 'Diagnosis'
    X = data.drop(columns=[target])
    Y = data[target]

    data_clean, scaler = preprocessing(X, training=True)
    X_train, X_test, Y_train, Y_test = train_test_split(data_clean, Y, test_size=0.2, random_state=42)

    #tunning Decission Tree
    param_grid = {
        'max_depth' : [3, 5, 7, 10, 15, None],
        'min_samples_split' : [2, 5, 10],
        'min_samples_leaf' : [1,2,4],
        'criterion' : ['gini', 'entropy']
    }
    model_dt = DecisionTreeClassifier(random_state=42)
    grid_search = GridSearchCV(model_dt, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, Y_train)
    print(grid_search.best_params_)
    print(grid_search.best_score_)

    model_dt = DecisionTreeClassifier(random_state=42, criterion='entropy', max_depth=5, min_samples_leaf=1, min_samples_split=2)
    model_dt.fit(X_train, Y_train)
    Y_pred_dt = model_dt.predict(X_test)

    akurasi_dt = accuracy_score(Y_test, Y_pred_dt)
    f1_dt = f1_score(Y_test, Y_pred_dt, average='weighted')

    print(f"akurasi decission tree : {akurasi_dt:.2f}")
    print(f"f1 score decission tree: {f1_dt:.2f}")

    #tunning random forest
    param_grid = {
        'n_estimators' : [100, 200, 300],
        'max_depth' : [None, 10, 20, 30],
        'min_samples_split' : [2, 5, 10],
        'min_samples_leaf' : [1, 2, 4],
        'max_features' : ['sqrt', 'log2'],
        'bootstrap' : [True, False],
        'criterion' : ['gini', 'entropy']
    }
    model_rf = RandomForestClassifier(random_state=42)
    grid_search = RandomizedSearchCV(model_rf, param_grid, n_iter=30, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, Y_train)
    print(grid_search.best_params_)
    print(grid_search.best_score_)

    model_rf = RandomForestClassifier(random_state=42, n_estimators=300, min_samples_split=2, min_samples_leaf=1, max_features='sqrt',max_depth=None, criterion='entropy', bootstrap=False)
    model_rf.fit(X_train, Y_train)
    Y_pred_rf = model_rf.predict(X_test)

    akurasi_rf = accuracy_score(Y_test, Y_pred_rf)
    f1_rf = f1_score(Y_test, Y_pred_rf,average='weighted')

    '''print(f"akurasi random forest : {akurasi_rf:.2f}")
    print(f"f1 score random forest : {f1_rf:.2f}")

    # print(Y.value_counts(normalize=True))  Lihat distribusi kelas
    print("dt", classification_report(Y_test, Y_pred_dt))
    print("rf", classification_report(Y_test, Y_pred_rf))'''

    model_path = os.path.join(base_dir, '..', 'model', 'model_anemia.pkl')
    scaler_path = os.path.join(base_dir, '..', 'model', 'scaler_anemia.pkl')
    joblib.dump(scaler, scaler_path)
    if akurasi_dt > akurasi_rf:
        joblib.dump(model_dt, model_path)
    else:
        joblib.dump(model_rf, model_path)

if __name__ == '__main__':
    model_train_for_anemia()