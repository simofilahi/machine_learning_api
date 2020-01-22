from flask import * 
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sklearn.impute import SimpleImputer
from srcs.model import model, prediction
import numpy as np
from srcs.DBconnect import DBconnect, closeConnection

app = Flask(__name__)
# jwt = JWTManager(app)
#
def summarizeOfData(df):
    print(df.describe().round(decimals=2))
    df = df.describe().round(decimals=2).to_json(orient='split')
    return df

def missingValueHandler(df):
    rows = df.shape[0]
    newdf = df.loc[0:rows].applymap\
    (lambda x: np.nan if x in ('NA', 'n/a', 'na', '--', '-', 'NAN') else x)
    # still not complete
    if newdf.isnull().values.any() == True:
        # print('Before fill missing values \n', newdf.head(15))
        for key in newdf.columns:
            median = newdf[key].median()
            newdf[key].fillna(median, inplace=True)
        # print('after fill missing values \n', newdf.head(10))
        return newdf
    else:
        # print('still some missing values not NAN')
        return newdf

def stringValue(df, col):
    for value in df[col]:
        if type(value) != str:
            return False
    return True

def datapreparation(df):
    # drop columns that include a string value
    for col in df.columns:
        if stringValue(df, col):
            df.drop([col], axis=1, inplace=True)
    # fill missing value by mean methode
    df = missingValueHandler(df)
    # handle Outliers
    return df

@app.route('/')
def upload():
    return render_template("file_upload_form.html")

CORS(app)
@app.route('/training', methods = ['POST', 'GET'])
def training():
    if request.method == 'GET':
        # loading of data
        conn, df = DBconnect()
        # data preparation
        newdf = datapreparation(df)
        # summarize data
        df = summarizeOfData(newdf)
        closeConnection(conn)
    return df

@app.route('/predict', methods = ['POST'])

def predict():
    if request.method == 'POST':
        # loading of data
        conn, df = DBconnect()
        # pr = prediction()
        jsonify({'prediction': list(pr)})
    return render_template("success.html", model_name = pr)

if __name__ == '__main__': 
    app.run(debug = True)

# f = request.files['file']
# f.save(f.filename)
# msg = model(f.filename)
# step 1 => 
# conn, df = DBconnect()
# f = request.files['file']
# step 2 => summarize data
# SummarizeData(df)
# else:
#     return "model not found"