from flask import * 
from model_training import model, prediction

app = Flask(__name__) 
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/training', methods = ['POST'])  
def training():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename) 
        msg = model(f.filename)
        return render_template("predict.html") 

@app.route('/predict', methods = ['POST']) 
def predict(): 
    if request.method == 'POST': 
        f = request.files['file'] 
        pr = prediction(f.filename)
        # else:
        #     return "model not found"
        # jsonify({'prediction': list(prediction)})
        return render_template("success.html", model_name = pr)
if __name__ == '__main__': 
    app.run(debug = True)