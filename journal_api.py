from flask import Flask
from models import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    db.create_all()

# importing all user routes
from user_routes import *

# importing all entry routes
from entry_routes import *

   
if __name__ == "__main__":
    app.run(debug=True)

