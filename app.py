import mindsdb
from flask import *
import json
import pandas as pd
import os
currentDirectory = os.getcwd()
os.environ['MINDSDB_STORAGE_PATH'] = '{currentDirectory}\modelsinfo'.format(
    currentDirectory=currentDirectory)
app = Flask(__name__)


@app.route('/api/v1/training/<uuid>', methods=['POST'])
def training(uuid):
    # try:
    # print("req ====> ", request.method)
    model_uuid = uuid
    req = request.get_json(force=True)
    if request.method == 'POST':
        print("data ", req['modelname'])
        # data = req['body']
        dt = req.copy()
        # parse the data sented from front-end
        modelname = dt.get('modelname')
        selectedFeature = dt.get('selectedFeature')
        # print("SELECTED ==> ", selectedFeature)
        selectedFeature = json.dumps(selectedFeature['data'])
        selectedTarget = dt.get('selectedTarget')
        targetname = selectedTarget['value']
        # print("uuid ==> ", uuid)
        df = pd.read_json(path_or_buf=selectedFeature, orient='records')
        mdb = mindsdb.Predictor(name=model_uuid)
        mdb.learn(from_data=df, to_predict=targetname)
        response = jsonify({"succes": True})
        response.status_code = 200
        return response
    # except:
    #     return jsonify({"succes": False})


@app.route('/api/v1/prediction/<uuid>', methods=['POST'])
def prediction(uuid):
    # try:
    model_uuid = uuid
    req = request.get_json(force=True)
    if request.method == 'POST':
        dt = req.copy()
        selectedFeature = dt.get('selectedFeature')
        selectedFeature = json.dumps(selectedFeature['data'])
        selectedTarget = dt.get('selectedTarget')
        targetname = selectedTarget['value']
        df = pd.read_json(path_or_buf=selectedFeature, orient='records')
        print("here data frame ==> ", df)
        mdb = mindsdb.Predictor(name=model_uuid)
        result = mdb.predict(
            when_data=df
        )
        # res = mdb.get_model_data(model_name=model_uuid)

        res = json.dumps(result.data)
        for x, y in result.data.items():
            print(x, y)
            if 'model_' + targetname == x:
                predictedValues = y
            elif targetname + '_model_confidence' == x:
                confidance = y
        data = {"values": predictedValues, "confidance": confidance}
        print("")
        response = jsonify({"success": True, "data":  data})
        # print("res **** ===> ", res)
        # result = jsonify(result)
        # for i in range(0, 20):
        # result = json.dumps(result,
        #                     indent=2, sort_keys=True)
        # print("here result ==> ", result)
        # result = json.dumps(result.__dict__)
        # print("here result ==> ", result)
        # print("res ==> ", result['test1'])
        # print("type ==> ", result)
        return response
    # except:
    #     return jsonify({"success": False})


@app.route('/api/v1/delete/<uuid>', methods=['GET'])
def delete(uuid):
    model_uuid = uuid
    try:
        if req['method'] == 'GET':
            Predictor(name=model_uuid)
            predictor.delete_model(model_name=model_name)
            return jsonify({"success": True})
    except:
        return jsonify({"success": False})


@app.route('/api/v1/download/<uuid>', methods=['GET'])
def download(uuid):
    model_uuid = uuid
    try:
        if req['method'] == 'GET':
            predictor = Predictor(name=model_uuid)
            predictor.delete_model(model_name=model_name)
        return jsonify("download")
    except expression as identifier:
        return jsonify({"success": False})


if __name__ == '__main__':
    app.run(host='10.1.35.13', port=5000)
