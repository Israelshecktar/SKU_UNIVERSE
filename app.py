from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from models import db, Brand, Category, Subcategory, SKU

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

@app.route('/')
def welcome():
    return "Welcome to SKU_UNIVERSE!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
