import mindsdb
from flask import *
import json
import pandas as pd
import os
import stat
from flask_cors import CORS
from threading import Thread

currentDirectory = os.getcwd()
os.environ['MINDSDB_STORAGE_PATH'] = '{currentDirectory}\modelsinfo'.format(
    currentDirectory=currentDirectory)
app = Flask(__name__)
CORS(app)


def threaded_task(df, model_uuid, targetname):
    try:
        mdb = mindsdb.Predictor(name=model_uuid)
        mdb.learn(from_data=df, to_predict=targetname)
        mdb.export_model()
        # oldpath = os.getcwd() + '\\' + model_uuid + '.zip'
        # newpath = os.getcwd() + '\\' + 'exportedmodels'
        # if os.path.exists(oldpath) == True:
        #     os.replace(oldpath, newpath)
    except ValueError:
        print(ValueError)


@app.route('/api/v1/training/<uuid>', methods=['POST'])
def training(uuid):
    try:
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
            print("SELECTED ==> ", selectedFeature)
            selectedFeature = json.dumps(selectedFeature['data'])
            selectedTarget = dt.get('selectedTarget')
            targetname = selectedTarget['value']
            df = pd.read_json(path_or_buf=selectedFeature, orient='records')
            thread = Thread(target=threaded_task, args=(
                df, model_uuid, targetname))
            thread.daemon = True
            thread.start()
            response = make_response(jsonify({"success": True}), 200)
            response.headers["Content-Type"] = 'application/json'
            return response
    except:
        response = make_response(jsonify({"success": False}), 500)
        response.headers["Content-Type"] = 'application/json'
        return response


@app.route('/api/v1/prediction/<uuid>', methods=['POST'])
def prediction(uuid):
    try:
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
            response = make_response(
                jsonify({"success": True, "data":  data}), 200)
            response.headers["Content-Type"] = 'application/json'
            return response
        else:
            response = make_response(jsonify({"success": False}), 404)
            response.headers["Content-Type"] = 'application/json'
            return response
    except:
        response = make_response(jsonify({"success": False}), 500)
        response.headers["Content-Type"] = 'application/json'
        return response


@app.route('/api/v1/delete/<uuid>', methods=['GET'])
def delete(uuid):
    try:
        model_uuid = uuid
        if request.method == 'GET':
            predictor = mindsdb.Predictor(name=model_uuid)
            res = predictor.delete_model(model_name=model_uuid)
            path = os.getcwd() + '\modelsinfo\\' + model_uuid + '_lightwood_data'
            print("path ==> ", path)
            if os.path.exists(path):
                os.remove(path)
                response = make_response(jsonify({"success": True}), 200)
                response.headers["Content-Type"] = 'application/json'
                return response
            else:
                response = make_response(jsonify({"success": False}), 404)
                response.headers["Content-Type"] = 'application/json'
                return response
    except:
        response = make_response(jsonify({"success": False}), 500)
        response.headers["Content-Type"] = 'application/json'
        return response

# replace download with tmp
@app.route('/api/v1/tmp/<uuid>', methods=['GET'])
def download(uuid):
    try:
        model_uuid = uuid
        if request.method == 'GET':
            print("Hello ")
            path = os.getcwd() + '\\' + model_uuid + '.zip'
            if os.path.exists(path):
                return send_file(
                    filename_or_fp=path,
                    mimetype='application/zip',
                    as_attachment=True,
                    attachment_filename='data.zip'
                )
            else:
                response = make_response(jsonify({"success": False}), 404)
                response.headers["Content-Type"] = 'application/json'
                return response
    except:
        response = make_response(jsonify({"success": False}), 500)
        response.headers["Content-Type"] = 'application/json'
        return response


if __name__ == '__main__':
    app.run(debug=True)
