from flask import *
import json
import pandas as pd
from flask_cors import CORS
# from flask_jwt_extended import JWTManager
from sklearn.impute import SimpleImputer
from srcs.model import model, prediction
import numpy as np
from srcs.DBconnect import DBconnect, closeConnection
from flask_mysqldb import MySQL
import mindsdb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'waste_to_resources'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# jwt = JWTManager(app)
#


def summarizeOfData(df):
    print(df.describe().round(decimals=2))
    df = df.describe().round(decimals=2).to_json(orient='split')
    return df


def missingValueHandler(df):
    rows = df.shape[0]
    newdf = df.loc[0:rows].applymap(lambda x: np.nan if x in (
        'NA', 'n/a', 'na', '--', '-', 'NAN') else x)
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
    # change the type of values from str to int
    for col in df.columns:
        df[col] = df[col].astype(int)
    # drop columns that include a string value
    for col in df.columns:
        if stringValue(df, col):
            df.drop([col], axis=1, inplace=True)
    # fill missing value by mean methode
    df = missingValueHandler(df)
    # handle Outliers
    return df


def createModel(df, modelName):
    mdb = mindsdb.Predictor(name=modelName)
    # We tell the Predictor what column or key we want to learn and from what data
    mdb.learn(
        # the path to the file where we can learn from, (note: can be url)
        from_data="https://s3.eu-west-2.amazonaws.com/mindsdb-example-data/home_rentals.csv",
        # the column we want to learn to predict given all the data in the file
        to_predict='rental_price',
        use_gpu=True

    )
    print("type of mdb ==> ", type(mdb))


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


CORS(app)
@app.route('/training', methods=['POST', 'GET'])
def training():
    req = request.get_json(force=True)
    print("req", req)
    if req['method'] == 'POST':
        data = req['body']
        dt = data.copy()
        # parse the data sented from front-end
        modelname = dt.get('modelname')
        selectedFeature = dt.get('selectedFeature')
        selectedFeature = json.dumps(selectedFeature['data'])
        selectedTarget = dt.get('selectedTarget')
        uuid = dt.get('uuid')
        print("modelname ==> ", modelname)
        print("selectedFeature ==> ", selectedFeature)
        print("selectedTarget ==> ", selectedTarget)
        print("uuid ==> ", uuid)
        df = pd.read_json(path_or_buf=selectedFeature, orient='records')
        print(df)
        # connect to mysql
        # cur = mysql.connection.cursor()
        # # get feature name from mysql
        # features = ''
        # for i in range(len(selectedFeature)):
        #     # print("selectedFeature ==> ", selectedFeature[i])
        #     temp = selectedFeature[i]
        #     Query = 'SELECT v.name_in_db FROM variable \
        #         v JOIN part p on v.part_id = p.id JOIN data_set d ON \
        #         p.data_set_id = d.id WHERE d.uuid LIKE "{uuid}" AND v.name Like "{temp}"'.format(
        #         uuid=uuid, temp=temp)
        #     print("Query ==> ", Query)
        #     cur.execute(Query)
        #     data = cur.fetchall()
        #     if (i == (len(selectedFeature) - 1)):
        #         features = features + data[0]['name_in_db']
        #     else:
        #         features = features + data[0]['name_in_db'] + ', '
        #     # print("features ==> ", features)
        # # get target name from mysql
        # Query = 'SELECT v.name_in_db FROM variable \
        #         v JOIN part p on v.part_id = p.id JOIN data_set d ON \
        #         p.data_set_id = d.id WHERE d.uuid LIKE "{uuid}" AND v.name Like "{selectedTarget}"'.format(
        #         uuid=uuid, selectedTarget=selectedTarget)
        # cur.execute(Query)
        # data = cur.fetchall()
        # target = data[0]['name_in_db']
        # # print("target ==> ", target)
        # mysql.connection.commit()
        # cur.close()
        # # loading of data
        # conn, df = DBconnect(uuid, modelname, features, target)
        # closeConnection(conn)
        # data preparation
        # print("before ==> ", df)
        # newdf = datapreparation(df)
        # print("newdf ==> ", newdf)
        # summarize data
        # createModel(df, target)
        # df = summarizeOfData(newdf)
        # create model
    return jsonify("succes")
    # return jsonify(df)

# @app.route('/predict', methods = ['POST'])

# def predict():
#     if request.method == 'POST':
#         # loading of data
#         conn, df = DBconnect()
#         # pr = prediction()
#         jsonify({'prediction': list(pr)})
#     return render_template("success.html", model_name = pr)


if __name__ == '__main__':
    app.run(debug=True)

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
