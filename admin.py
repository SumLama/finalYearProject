# # 

# from flask import Flask
# from flask_pymongo import PyMongo
# from flask_admin import Admin
# from flask_admin.contrib.pymongo import ModelView

# app = Flask(__name__)

# # Configure the Flask app with MongoDB URI
# app.config['MONGO_URI'] = "mongodb://localhost:27017/UserDb"
# mongo = PyMongo(app)

# class User(mongo.db.Document):
#     username = mongo.db.StringField()
#     email = mongo.db.StringField()

# # Create admin
# admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

# # Add view for User model
# admin.add_view(ModelView(User))

# if __name__ == '__main__':
#     # app.run(debug=True)