from flask import Flask
from models import db, add_initial_data
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def welcome():
    return "Welcome to SKU_UNIVERSE!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
        add_initial_data()  # Add initial data
    app.run(debug=True)
