import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error
from sklearn.externals import joblib
from sklearn.preprocessing import PolynomialFeatures
import os

def lrmodel_1(X_train, X_test, y_train, y_test):
     # poly_reg = PolynomialFeatures(degree = 2)
     # X_train = poly_reg.fit_transform(X_train)
     # X_test = poly_reg.fit_transform(X_test)
     regressor = LinearRegression()
     regressor.fit(X_train, y_train)
     y_pred = regressor.predict(X_test)
     MAEValue = mean_absolute_error(y_test, y_pred)
     MSEValue = mean_squared_error(y_test, y_pred)
     MdSEValue = median_absolute_error(y_test, y_pred)
     return regressor, MAEValue, MSEValue, MdSEValue
     
def lrmodel_2(X_train, X_test, y_train, y_test):
     SGDRegressionModel = SGDRegressor(alpha=0.1,random_state=33)
     SGDRegressionModel.fit(X_train, y_train)
     y_pred = SGDRegressionModel.predict(X_test)
     MAEValue = mean_absolute_error(y_test, y_pred, multioutput='uniform_average')
     MSEValue = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
     MdSEValue = median_absolute_error(y_test, y_pred)
     return SGDRegressionModel, MAEValue, MSEValue, MdSEValue

def lrmodel_3(X_train, X_test, y_train, y_test):
     RidgeRegressionModel = Ridge(alpha=0.1,random_state=33)
     RidgeRegressionModel.fit(X_train, y_train)
     #Calculating Prediction
     y_pred = RidgeRegressionModel.predict(X_test)
     MAEValue = mean_absolute_error(y_test, y_pred, multioutput='uniform_average')
     MSEValue = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
     MdSEValue = median_absolute_error(y_test, y_pred)
     return RidgeRegressionModel, MAEValue, MSEValue, MdSEValue

def model(filename):
     # Importing the dataset
     dataset = pd.read_csv(filename, sep='[:,|_] ')
     # dataset = DataPrepartion(dataset)
     # Splitting the dataset into the Training set and Test set
     print(dataset.shape)
     cols = dataset.shape[1]
     if cols == 1 :
          return "error"
     X = dataset.iloc[:,0:cols-1]
     y = dataset.iloc[:,cols - 1 : cols]
     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 30)
     regressor, MAEValue, MSEValue, MdSEValue = lrmodel_1(X_train, X_test, y_train, y_test)
     print(MAEValue, MSEValue, MdSEValue)
     regressor1, MAEValue1, MSEValue1, MdSEValue1 = lrmodel_2(X_train, X_test, y_train, y_test)
     print("second")
     print(MAEValue1, MSEValue1, MdSEValue1)
     regressor2, MAEValue2, MSEValue2, MdSEValue2 = lrmodel_2(X_train, X_test, y_train, y_test)
     print("third")
     print(MAEValue1, MSEValue1, MdSEValue1)
     # RidgeRegressionModel = Ridge(alpha=1.0,random_state=33)
     # RidgeRegressionModel.fit(X_train, y_train)
     # filename.strip('.csv')
     filename = os.path.splitext(filename)[0]
     model_name = filename + '.pkl'
     joblib.dump(regressor, model_name)
     return "model is ready"

def prediction(filename):
     dataset = pd.read_csv(filename, sep='[:,|_] ')
     if dataset.shape[1] == 1 :
          return "error"
     filename = os.path.splitext(filename)[0]
     model_name = filename + '.pkl'
     pr = joblib.load(model_name)
     cols = dataset.shape[1]
     X = dataset.iloc[:,0:cols-1]
     prediction = pr.predict(X)
     return prediction[0:40]