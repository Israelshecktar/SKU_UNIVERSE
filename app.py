from flask import Flask, jsonify, request
from models import db, add_initial_data, SKU, Brand, Category
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

@app.route("/api/skus/brand/<int:brand_id>", methods=["GET"])
def get_skus_by_brand(brand_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    skus = SKU.query.filter_by(brand_id=brand_id).paginate(page=page, per_page=per_page, error_out=False)
    skus_list = [
        {
            "material": sku.material,
            "material_description": sku.material_description,
            "uom": sku.uom,
            "brand_id": sku.brand_id,
            "category_id": sku.category_id,
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

@app.route("/api/skus/category/<int:category_id>", methods=["GET"])
def get_skus_by_category(category_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    skus = SKU.query.filter_by(category_id=category_id).paginate(page=page, per_page=per_page, error_out=False)
    skus_list = [
        {
            "material": sku.material,
            "material_description": sku.material_description,
            "uom": sku.uom,
            "brand_id": sku.brand_id,
            "category_id": sku.category_id,
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

@app.route("/api/skus/<int:sku_id>", methods=["GET"])
def get_sku(sku_id):
    sku = SKU.query.get_or_404(sku_id)
    sku_details = {
        "material": sku.material,
        "material_description": sku.material_description,
        "uom": sku.uom,
        "brand_id": sku.brand_id,
        "category_id": sku.category_id,
        "product_line": sku.product_line,
        "brand_name": sku.brand.name,
        "category_name": sku.category.name,
    }
    return jsonify(sku_details)

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
