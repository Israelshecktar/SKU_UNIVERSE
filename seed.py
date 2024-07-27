from initial_data import add_initial_data
from app import app

if __name__ == "__main__":
    with app.app_context():
        add_initial_data()
