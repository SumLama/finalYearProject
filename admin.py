# from flask import Flask
# from flask_pymongo import PyMongo
# from flask_admin import Admin
# from flask_admin.contrib.pymongo import ModelView

# app = Flask(__name__)


# app.config['MONGO_URI'] = "mongodb://localhost:27017/UserDb"
# mongo = PyMongo(app)


# admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')


# class User(mongo.db.Document): 

#     username = mongo.db.StringField(required=True)


#     def __repr__(self):
#         return self.username


# admin.add_view(ModelView(User))


# if __name__ == '__main__':
#     app.run()
