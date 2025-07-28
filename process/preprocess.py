import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocessing(df, scaler=None, training=True):

    data = df.copy()
    data.ffill(inplace=True)

    '''
    if data.duplicated().sum() > 0:
        data = data.drop_duplicates()'''

    data_numerik = [i for i in data.columns if data[i].dtype != 'O']
    data_kategorik = [i for i in data.columns if data[i].dtype == 'O']

    X = data

    if training:
        scaler = StandardScaler()
        data_scaler = scaler.fit_transform(X)
    else:
        data_scaler = scaler.transform(X)
    data_process = pd.DataFrame(data_scaler, columns=X.columns, index=X.index)

    if training:
        return data_process, scaler
    else:
        return data_process