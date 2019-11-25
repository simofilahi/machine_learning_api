# from sklearn.linear_model import Ridge
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
import os

def model(filename):
     dataset = pd.read_csv(filename, delim_whitespace=True)
     cols = dataset.shape[1]
     X = dataset.iloc[:,0:cols-1]
     y = dataset.iloc[:,cols - 1 : cols]
     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
     regressor = LinearRegression()
     regressor.fit(X_train, y_train)
     # RidgeRegressionModel = Ridge(alpha=1.0,random_state=33)
     # RidgeRegressionModel.fit(X_train, y_train)
     # filename.strip('.csv')
     filename = os.path.splitext(filename)[0]
     model_name = filename + '.pkl'
     joblib.dump(regressor, model_name)
     return "model is ready"

def prediction(filename):
     dataset = pd.read_csv(filename, delim_whitespace=True)
     X = dataset.iloc[:,:]
     filename = os.path.splitext(filename)[0]
     model_name = filename + '.pkl'
     pr = joblib.load(model_name)
     pr.predict(X)