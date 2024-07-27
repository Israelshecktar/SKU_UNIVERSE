from flask import Flask, jsonify, request
from models import db, SKU, Brand, Category, Subcategory
from config import Config
from flask_migrate import Migrate
from initial_data import add_initial_data
#from seed import add_initial_data  

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def welcome():
    return "Welcome to SKU_UNIVERSE!"

@app.route("/api/skus", methods=["GET"])
def get_skus():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    skus = SKU.query.paginate(page=page, per_page=per_page, error_out=False)
    skus_list = [
        {
            "material": sku.material,
            "material_description": sku.material_description,
            "uom": sku.uom,
            "brand_id": sku.brand_id,
            "category_id": sku.category_id,
            "subcategory_id": sku.subcategory_id,
            "product_line": sku.product_line,
        }
        for sku in skus.items
    ]
    return jsonify({
        "total": skus.total,
        "pages": skus.pages,
        "current_page": skus.page,
        "skus": skus_list
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
        add_initial_data()  # Add initial data
    app.run(debug=True)
