import mindsdb
from flask import *
import json
import pandas as pd
from exportedmodels.export import export
import os
from threading import Thread
import time
import requests

currentDirectory = os.getcwd()
os.environ['MINDSDB_STORAGE_PATH'] = '{currentDirectory}\modelsinfo'.format(
    currentDirectory=currentDirectory)
app = Flask(__name__)

def threaded_task(df, model_uuid, targetname):
    mdb = mindsdb.Predictor(name=model_uuid)
    mdb.learn(from_data=df, to_predict=targetname)
    export(mdb, model_uuid)
    url = ' http://127.0.0.1:5000/api/v1/prediction/4deb0c2e-cd53-4d77-a612-a0d23893e423'
    data = {
        "modelname": "model",
        "selectedFeature": {
        "data": [
            { "test2": 2, "test3": 3, "A": 55, "B": 66 },
            { "test2": 10, "test3": 22, "A": 33, "B": 433 },
            { "test2": 33, "test3": 44, "A": 12, "B": 12 },
            { "test2": "14", "test3": "21", "A": "45", "B": "44" },
            { "test2": "12", "test3": "11", "A": "33", "B": "55" },
            { "test2": "55", "test3": "1", "A": 4, "B": 3 },
            { "test2": "43", "test3": "4", "A": 4, "B": 1 },
            { "test2": "33", "test3": "0", "A": 6, "B": 7 }
            ]
        },
        "selectedTarget": {"value": "I"}
    }
    headers = {"content-type" : "application/json"}
    req = requests.post(url, data=json.dumps(data), headers=headers)
    print(req.text)

@app.route('/api/v1/training/<uuid>', methods=['POST'])
def training(uuid):
    # try:
    # print("req ====> ", request.method)
    model_uuid = uuid
    req = request.get_json(force=True)
    if request.method == 'POST':
        # print("data ", req['modelname'])
        # data = req['body']
        dt = req.copy()
        # parse the data sented from front-end
        modelname = dt.get('modelname')
        selectedFeature = dt.get('selectedFeature')
        # print("SELECTED ==> ", selectedFeature)
        selectedFeature = json.dumps(selectedFeature['data'])
        selectedTarget = dt.get('selectedTarget')
        targetname = selectedTarget['value']
        df = pd.read_json(path_or_buf=selectedFeature, orient='records')
        thread = Thread(target=threaded_task, args=(df, model_uuid, targetname))
        thread.daemon = True
        thread.start()
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
        mdb = mindsdb.Predictor(name=model_uuid)
        result = mdb.predict(
            when_data=df
        )
        for x, y in result.data.items():
            if 'model_' + targetname == x:
                predictedValues = y
            elif targetname + '_model_confidence' == x:
                confidance = y
        data = {"values": predictedValues, "confidance": confidance}
        response = jsonify({"success": True, "data":  data})
        return response
    # except:
    #     return jsonify({"success": False})


@app.route('/api/v1/delete/<uuid>', methods=['GET'])
def delete(uuid):
    model_uuid = uuid
    try:
        if request.method == 'GET':
            predictor = mindsdb.Predictor(name=model_uuid)
            predictor.delete_model(model_name=model_uuid)
            return jsonify({"success": True})
    except:
        return jsonify({"success": False})


@app.route('/api/v1/download/<uuid>', methods=['GET'])
def download(uuid):
    model_uuid = uuid
    # try:
    if request.method == 'GET':
        mdb = mindsdb.Predictor(name=model_uuid)
        path = model_uuid + '.zip'
        res = mdb.load(model_archive_path=path)
        print("res ==> ", res)
    return jsonify("download")
    # except:
    #     return jsonify({"success": False})

if __name__ == '__main__':
    app.run(host='10.1.35.13', port=5000, debug=True)
