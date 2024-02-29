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
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

import pickle
import base64
import re
# for email

from pymongo import MongoClient
from email.mime.text import MIMEText

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
model = pickle.load(open("models\TrainedModel.pkl", "rb"))
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


# @ app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
       
      
#         user_email = session.get('email')
#         print(user_email)

#         # check if email and password are not empty
#         if not email or not password:
#             error_message = "Email and password are required."
#             return f"<script>alert('{error_message}');window.location='/login'</script>"

#         user = mongo.db.user

#         login_user = user.find_one({'email': email})

#         if login_user:
#             user_email = login_user['email']
#             session['email'] = user_email

#             if bcrypt.checkpw(password.encode('utf-8'), login_user['password']):
#                 session['email'] = email
#                 session['username'] = login_user['username']
#                 return redirect('/')
#             else:
#                 error_message = "Invalid email or password."
#         else:
#             error_message = "User not registered"

#         # display the error message using JavaScript alert function
#         return f"<script>alert('{error_message}');window.location='/login'</script>"    
   
#     return render_template('signIn.html')
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

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        print(request.form) 
        user = mongo.db.user
        existing_email = user.find_one({'email': request.form.get('email')})
        if existing_email:
            email_error = "email have been already used."
            return f"<script>alert('{email_error}');window.location='/login'</script>"

        if request.form.get('password') != request.form.get('confirm_password'):
            pass_error = "password do not matched"
            return f"<script>alert('{pass_error}');window.location='/register'</script>"

        if len(request.form.get('password')) < 8:
            pass_error = "password must be of 8 character"
            return f"<script>alert('{pass_error}');window.location='/register'</script>"

        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

        if not re.fullmatch(password_pattern, request.form.get('password')):
            pass_error = "uppercase letters: A-Z, lowercase letters: a-z, numbers: 0-9, any of the special characters: @#$%^&+="
            return f"<script>alert('{pass_error}');window.location='/register'</script>"

        hashpass = bcrypt.hashpw(
            request.form.get('password').encode('utf-8'), bcrypt.gensalt())
        user.insert_one(
            {'username': request.form.get('username'), 'password': hashpass, 'email': request.form.get('email')})
        session['email'] = request.form.get('email')

        return f"<script>alert('User registered successfully!');window.location='/login'</script>" 
       
    return render_template('register.html')

    

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


        # encoded_location = label_encoder.fit_transform(location)    
        # Creating input list for prediction
        # input_lst = [encoded_location, maxTemp,minTemp,humidity,rainfall,rainToday,year, month, day,]
        input_lst = [location, maxTemp,minTemp,humidity,rainfall,rainToday,year, month, day]
        final_list = np.array(input_lst)

         #Create a credentials object from the access token and refresh token
        creds = Credentials(
            ACCESS_TOKEN,
            token_uri=TOKEN_URI,
            refresh_token=REFRESH_TOKEN,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        service = build('gmail', 'v1', credentials=creds)
       
        # Predicting
        pred = model.predict(final_list)
            
            # Rendering template based on prediction
       
                #  pass_error = "password must be of 8 character"
                # return f"<script>alert('{pass_error}');window.location='/register'</script>"
        try:
            user_email = session.get('email')  # Assuming the user's email is stored in the session
            if pred[0] == 0:
                subject = 'Rainfall Notification'
                message = 'Hello there, there will be no rain on your desired date. Enjoy with your friends and family. Thank you'
            else:
                subject = 'Rainfall Notification'
                message = 'Hello there, there will be rain on your desired date. Please take care while going outside. Thank you'

            msg = MIMEText(message)
            msg['to'] = user_email
            msg['subject'] = subject
            raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
            send_message = {'raw': raw_message}
            send_message = service.users().messages().send(userId="me", body=send_message).execute()
            print(F'The email was sent to {user_email} with email Id: {send_message["id"]}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = None

        prediction_text = "It is likely to be sunny, you can enjoy the outing to your desired location with your family and friends." if pred[0] == 0 else "It is likely to rain,so you might want to consider bringing an umbrella or planning indoor activities."

    return render_template("predictor.html", prediction_text=prediction_text)

# # for email message
CLIENT_ID = '620539546907-f31a9podppn69tqgm43k9j835scni076.apps.googleusercontent.com'
CLIENT_SECRET = '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'
ACCESS_TOKEN = 'ya29.a0AfB_byBxsRQ-C0C_v_1XIwtbYlhyKoekYtzso5fQqwsBdwQ1qCKmyLVX-oCHrQSNlSgtLN5eitvQw8bb3TboGBPL80kdiLCiL03XSR7jVwduAVV0F-G1wfZ3AJ7ZIVdPMztLu80FoosfbUS4NuHzVw1Fn6_ZefNDhpViaCgYKAc0SARASFQHGX2MiT1PF_12HGh0Bur5Ayo6-Kg0171'
REFRESH_TOKEN = '1//0g-_vl0bPd-_HCgYIARAAGBASNwF-L9IrA9reVpSZOvRoG56oueQvaVFFpHqoILGAOI7kmULgqOdEisYNt6SnEwXmgnRYVZFGVyc'
TOKEN_URI = 'https://oauth2.googleapis.com/token'

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
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return render_template('home.html')
        if 'email' in session:
            if session['email'] != 'rainfallPredictor@gmail.com' :
                denied_error = "Authorization denied"

                return f"<script>alert('{denied_error}');window.location='/home'</script>"
        return func(*args, **kwargs)

    return decorated_function

@app.route('/admin')
@admin_required
def admin_panel():
    if 'email' in session:
        if session['email'] != 'rainfallPredictor@gmail.com':
            pass_error = "Not Authorized"
            return f"<script>alert('{pass_error}');window.location='/'</script>"

    user = mongo.db.user

    users = user.find({})
    return render_template('admin.html', users=users)


@app.route('/admin/delete', methods=['POST'])
@admin_required
def delete_user():

    uname = request.form['user_id']

    user = mongo.db.user

    users = user.delete_one({'username': uname})

    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)


