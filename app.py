from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
from randomforest.DecisionTree import DecisionTree
from randomforest.RandomForest import RandomForest
from sklearn.preprocessing import LabelEncoder
import sys
sys.path.append("/home/sujaldangal/Documents/Rain-Prediction/randomforest")

app = Flask(__name__, template_folder="template")
model = pickle.load(open("./models/TrainedModel.pkl", "rb"))
# label_encoder = pickle.load(open("./models/Location.pkl","rb")) 
print("Model Loaded")

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/predict", methods=['GET','POST'])
def predict():
    if request.method == "POST":
        # Extracting data from the form
        # date = pd.to_datetime(request.form['Date'])
        year = float(request.form['Year'])
        day = float(request.form['Day'])
        month = float(request.form['Month'])
        # day = float(date.day)
        # month = float(date.month)
        minTemp = float(request.form['min_temp'])
        maxTemp = float(request.form['max_temp'])
        rainfall = float(request.form['Rainfall'])
        humidity = float(request.form['Humidity'])
        location = float(request.form['Location'])
        rainToday = float(request.form['RainToday'])


        # encoded_location = label_encoder.transform(location)    
        # Creating input list for prediction
        # input_lst = [encoded_location, maxTemp,minTemp,humidity,rainfall,rainToday,year, month, day,]
        input_lst = [location, maxTemp,minTemp,humidity,rainfall,rainToday,year, month, day,]
        final_list = np.array(input_lst)
        # Predicting
        pred = model.predict(final_list)
        
        # Rendering template based on prediction
        if pred[0] == 0:
            return render_template("after_sunny.html")
        else:
            return render_template("after_rainy.html")
    
    return render_template("predictor.html")

if __name__ == '__main__':
    app.run(debug=True)

