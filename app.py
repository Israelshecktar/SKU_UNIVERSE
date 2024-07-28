from flask import Flask, jsonify, request
from models import db, SKU, Brand, Category, Subcategory
from config import Config
from flask_migrate import Migrate
from initial_data import add_initial_data
import logging

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def welcome():
    return "Welcome to SKU_UNIVERSE!"

@app.route("/api/skus", methods=["GET"])
def get_skus():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    skus_query = SKU.query.paginate(page=page, per_page=per_page, error_out=False)
    skus_list = []
    for sku in skus_query.items:
        brand = Brand.query.get(sku.brand_id)
        category = Category.query.get(sku.category_id)
        subcategory = Subcategory.query.get(sku.subcategory_id)
        skus_list.append({
            "material": sku.material,
            "material_description": sku.material_description,
            "uom": sku.uom,
            "brand": brand.name if brand else None,
            "category": category.name if category else None,
            "subcategory": subcategory.name if subcategory else None,
            "product_line": sku.product_line,
        })
    return jsonify({
        "total": skus_query.total,
        "pages": skus_query.pages,
        "current_page": skus_query.page,
        "per_page": skus_query.per_page,
        "skus": skus_list
    })

@app.route("/api/skus/brand/<string:brand_name>", methods=["GET"])
def get_skus_by_brand(brand_name):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    brand = Brand.query.filter_by(name=brand_name).first_or_404(description=f"Brand {brand_name} not found")
    skus_query = SKU.query.filter_by(brand_id=brand.id).paginate(page=page, per_page=per_page, error_out=False)
    skus_list = []
    for sku in skus_query.items:
        category = Category.query.get(sku.category_id)
        subcategory = Subcategory.query.get(sku.subcategory_id)
        skus_list.append({
            "material": sku.material,
            "material_description": sku.material_description,
            "uom": sku.uom,
            "brand": brand.name,
            "category": category.name if category else None,
            "subcategory": subcategory.name if subcategory else None,
            "product_line": sku.product_line,
        })
    return jsonify({
        "total": skus_query.total,
        "pages": skus_query.pages,
        "current_page": skus_query.page,
        "per_page": skus_query.per_page,
        "skus": skus_list
    })

@app.route("/api/skus/brand/<string:brand_name>/subcategory/<string:subcategory_name>", methods=["GET"])
def get_skus_by_brand_and_subcategory(brand_name, subcategory_name):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    brand = Brand.query.filter_by(name=brand_name).first_or_404(description=f"Brand {brand_name} not found")
    
    # Find the correct subcategory ID for the given brand and subcategory name
    subcategory = Subcategory.query.join(Category).filter(
        Subcategory.name == subcategory_name,
        Category.brand_id == brand.id
    ).first_or_404(description=f"Subcategory {subcategory_name} not found for brand {brand_name}")
    
    logging.debug(f"Brand ID: {brand.id}, Subcategory ID: {subcategory.id}")
    
    skus_query = SKU.query.filter_by(brand_id=brand.id, subcategory_id=subcategory.id).paginate(page=page, per_page=per_page, error_out=False)
    
    logging.debug(f"SKUs found: {skus_query.total}")
    
    skus_list = []
    for sku in skus_query.items:
        category = Category.query.get(sku.category_id)
        skus_list.append({
            "material": sku.material,
            "material_description": sku.material_description,
            "uom": sku.uom,
            "brand": brand.name,
            "category": category.name if category else None,
            "subcategory": subcategory.name,
            "product_line": sku.product_line,
        })
    return jsonify({
        "total": skus_query.total,
        "pages": skus_query.pages,
        "current_page": skus_query.page,
        "per_page": skus_query.per_page,
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
        db.create_all()  # Create tables if they don't exist
        add_initial_data()  # Add initial data
    app.run(debug=True)
