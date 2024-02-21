import bcrypt
from flask_pymongo import PyMongo
from flask_login import login_required
from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import pandas as pd
from flask_mail import Mail, Message
from email_validator import validate_email, EmailNotValidError
from email.mime.multipart import MIMEMultipart
from functools import wraps
# from googleapiclient.errors import HttpError
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request

import pickle
import base64
import re
# for email

# from pymongo import MongoClient
# from email.mime.text import MIMEText

# for email validation

####imported new

from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
import sys
sys.path.append("E:\DemoPractice")
from randomforest.DecisionTree import DecisionTree
from randomforest.RandomForest import RandomForest
from sklearn.preprocessing import LabelEncoder


app = Flask(__name__, template_folder="template")

app.secret_key = "mysecretkey"

app.config['MONGO_DBNAME'] = "UserDb"
app.config['MONGO_URI'] = "mongodb://localhost:27017/UserDb"
mongo = PyMongo(app)
print("connected")
###################
model = pickle.load(open("./models/TrainedModel.pkl", "rb"))
# label_encoder = pickle.load(open("./models/Location.pkl","rb")) 
print("Model Loaded")

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")



def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function


@ app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
       
        user_name = session.get('username')
        user_email = session.get('email')
        print(user_email)

        # check if email and password are not empty
        if not email or not password:
            error_message = "Email and password are required."
            return f"<script>alert('{error_message}');window.location='/login'</script>"

        user = mongo.db.user

        login_user = user.find_one({'email': email})

        if login_user:
            user_email = login_user['email']
            session['email'] = user_email

            if bcrypt.checkpw(password.encode('utf-8'), login_user['password']):
                session['email'] = email
                session['username'] = login_user['username']
                return redirect('/')
            else:
                error_message = "Invalid email or password."
        else:
            error_message = "User not registered"

        # display the error message using JavaScript alert function
        return f"<script>alert('{error_message}');window.location='/login'</script>"    
    return render_template('signIn.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = mongo.db.user
        # existing_user = user.find_one({'username': request.form['username']})
        # existing_email = user.find_one({'email': request.form['email']})
        # if existing_email:
        #     email_error = "email have been already used."
        #     return f"<script>alert('{email_error}');window.location='/register'</script>"

        # if existing_user:
        #     name_error = "username is already taken."
        #     return f"<script>alert('{name_error}');window.location='/register'</script>"
        
        
        if request.form['password'] != request.form['confirm_password']:
            pass_error = "password do not matched"
            return f"<script>alert('{pass_error}');window.location='/register'</script>"

        if len(request.form["password"]) < 8:
            pass_error = "password must be of 8 character"
            return f"<script>alert('{pass_error}');window.location='/register'</script>"

        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

        if not re.fullmatch(password_pattern, request.form["password"]):
            pass_error = "uppercase letters: A-Z, lowercase letters: a-z, numbers: 0-9, any of the special characters: @#$%^&+="
            return f"<script>alert('{pass_error}');window.location='/register'</script>"

        hashpass = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        user.insert_one(
            {'username': request.form['username'], 'password': hashpass, 'email': request.form['email']})
        session['username'] = request.form['username']
        session['email'] = request.form['email']

        return render_template("signIn.html")

    return render_template("register.html")
    

@app.route("/predict", methods=['GET','POST'])
@ login_required
def predict():
    
    prediction_text = ""
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
        input_lst = [location, maxTemp,minTemp,humidity,rainfall,rainToday,year, month, day]
        final_list = np.array(input_lst)

         # Create a credentials object from the access token and refresh token
        # creds = Credentials(
        #     ACCESS_TOKEN,
        #     token_uri=TOKEN_URI,
        #     refresh_token=REFRESH_TOKEN,
        #     client_id=CLIENT_ID,
        #     client_secret=CLIENT_SECRET)
        # if creds and creds.expired and creds.refresh_token:
        #     creds.refresh(Request())

        # service = build('gmail', 'v1', credentials=creds)
       
        # Predicting
        pred = model.predict(final_list)
            
            # Rendering template based on prediction
        if pred[0] == 0:
                #  pass_error = "password must be of 8 character"
                # return f"<script>alert('{pass_error}');window.location='/register'</script>"
                # try:
                #     subject = 'Rainfall Notification'
                #     message = f'Hello there,there will be no rain in  on your desired date.Enjoy with your friends and family. Thankyou'
                #     msg = MIMEText(message)
                #     msg['to'] = user_email
                #     msg['subject'] = subject
                #     raw_message = base64.urlsafe_b64encode(
                #         msg.as_bytes()).decode('utf-8')
                #     send_message = {'raw': raw_message}
                #     send_message = (service.users().messages().send(
                #         userId="me", body=send_message).execute())
                #     print(
                #         F'The email was sent to {user_email} with email Id: {send_message["id"]}')
                # except HttpError as error:
                #     print(F'An error occurred: {error}')
                #     send_message = None
             prediction_text = " It is likely to be sunny"
                
        else:
                # try:
                #     subject = 'Rainfall Notification'
                #     message = f'hello there,there will be rain on your desired date, please take care while going outside. Thankyou'
                #     msg = MIMEText(message)
                #     msg['to'] = user_email
                #     msg['subject'] = subject
                #     raw_message = base64.urlsafe_b64encode(
                #         msg.as_bytes()).decode('utf-8')
                #     send_message = {'raw': raw_message}
                #     send_message = (service.users().messages().send(
                #         userId="me", body=send_message).execute())
                #     print(
                #         F'The email was sent to {user_email} with email Id: {send_message["id"]}')
                # except HttpError as error:
                #     print(F'An error occurred: {error}')
                #     send_message = None
                prediction_text = " It is likely to rain"
           

    
    
    return render_template("predictor.html", prediction_text=prediction_text)

# # for email message
# CLIENT_ID = '279094025508-q5l5k4l57i8lpjq09239bvoj2n0t4j76.apps.googleusercontent.com'
# CLIENT_SECRET = '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'
# ACCESS_TOKEN = 'ya29.a0AWY7CklY8IXfBClmOoDflHxQYtlb18h5khuk14RFqYv6ExHJyjTtgS1eCI3AO6uTQzgmXdrGH94x3PqUk2lRadUUcyUqCIBJSIJxPoOy-4XWdtFwvz8zjG5wYmPEoT61q0HOdn2bJoo5WKjWCa2oIWTxOFXyaCgYKAbASARESFQG1tDrp7tpCogLYQoGQ1XDZPsyTpw0163'
# REFRESH_TOKEN = '1//    04KTZsKHl30GxCgYIARAAGAQSNwF-L9Ir93qmnAzADRxj0K5RiQG_5f4pUkC2_dhUTUHPWZpaoI3T4E3kVHNf2whE799rgczlE6A'
# TOKEN_URI = 'https://oauth2.googleapis.com/token'

# @ app.route("/email", methods=['GET', 'POST'])
# def email():
#     if request.method == "POST":
#         try:
#             # Create a credentials object from the access token and refresh token
#             creds = Credentials(
#                 ACCESS_TOKEN,
#                 token_uri=TOKEN_URI,
#                 refresh_token=REFRESH_TOKEN,
#                 client_id=CLIENT_ID,
#                 client_secret=CLIENT_SECRET)
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())


# # Create a Gmail API service client
#             service = build('gmail', 'v1', credentials=creds)

#             to = request.form['receiver_email']

#             subject = 'Rainfall Notification'
#             message = request.form['message']
#             msg = MIMEText(message)
#             msg['to'] = to
#             msg['subject'] = subject
#             raw_message = base64.urlsafe_b64encode(
#                 msg.as_bytes()).decode('utf-8')

#             send_message = {'raw': raw_message}
#             send_message = (service.users().messages().send(
#                 userId="me", body=send_message).execute())
#             print(
#                 F'The email was sent to {to} with email Id: {send_message["id"]}')
#         except HttpError as error:
#             print(F'An error occurred: {error}')
#             send_message = None

#     return render_template('email.html')

@ app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


