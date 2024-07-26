from flask import Flask, jsonify
from models import db, add_initial_data, SKU
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def welcome():
    return "Welcome to SKU_UNIVERSE!"


@app.route("/api/skus", methods=["GET"])
def get_skus():
    skus = SKU.query.all()
    skus_list = []
    for sku in skus:
        skus_list.append(
            {
                "material": sku.material,
                "material_description": sku.material_description,
                "uom": sku.uom,
                "brand_id": sku.brand_id,
                "category_id": sku.category_id,
                "product_line": sku.product_line,
            }
        )
    return jsonify(skus_list)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
        add_initial_data()  # Add initial data
    app.run(debug=True)
