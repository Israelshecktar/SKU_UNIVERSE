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
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    skus_query = SKU.query.paginate(page=page, per_page=per_page, error_out=False)
    skus_list = []
    for sku in skus_query.items:
        brand = Brand.query.get(sku.brand_id)
        category = Category.query.get(sku.category_id)
        subcategory = Subcategory.query.get(sku.subcategory_id)
        skus_list.append(
            {
                "material": sku.material,
                "material_description": sku.material_description,
                "uom": sku.uom,
                "brand": brand.name if brand else None,
                "category": category.name if category else None,
                "subcategory": subcategory.name if subcategory else None,
                "product_line": sku.product_line,
            }
        )
    return jsonify(
        {
            "total": skus_query.total,
            "pages": skus_query.pages,
            "current_page": skus_query.page,
            "per_page": skus_query.per_page,
            "skus": skus_list,
        }
    )


@app.route("/api/skus", methods=["POST"])
def create_sku():
    data = request.get_json()
    new_sku = SKU(
        material=data.get("material"),
        material_description=data.get("material_description"),
        uom=data.get("uom"),
        brand_id=data.get("brand_id"),
        category_id=data.get("category_id"),
        subcategory_id=data.get("subcategory_id"),
        product_line=data.get("product_line"),
    )
    db.session.add(new_sku)
    db.session.commit()
    return jsonify({"message": "SKU created successfully"}), 201


@app.route("/api/skus/<identifier>", methods=["PUT"])
def update_sku(identifier):
    data = request.get_json()
    sku = SKU.query.filter(
        (SKU.id == identifier) | (SKU.material_description == identifier)
    ).first_or_404()
    sku.material = data.get("material", sku.material)
    sku.material_description = data.get(
        "material_description", sku.material_description
    )
    sku.uom = data.get("uom", sku.uom)
    sku.brand_id = data.get("brand_id", sku.brand_id)
    sku.category_id = data.get("category_id", sku.category_id)
    sku.subcategory_id = data.get("subcategory_id", sku.subcategory_id)
    sku.product_line = data.get("product_line", sku.product_line)
    db.session.commit()
    return jsonify({"message": "SKU updated successfully"})


@app.route("/api/skus/<identifier>", methods=["DELETE"])
def delete_sku(identifier):
    try:
        # Try to convert identifier to an integer to check if it's an ID or material code
        identifier = int(identifier)
        sku = SKU.query.filter_by(material=identifier).first_or_404(
            description=f"SKU with material {identifier} not found"
        )
    except ValueError:
        # If conversion fails, treat identifier as material description
        sku = SKU.query.filter_by(material_description=identifier).first_or_404(
            description=f"SKU with material description '{identifier}' not found"
        )

    db.session.delete(sku)
    db.session.commit()
    return jsonify({"message": "SKU deleted successfully"})


@app.route("/api/skus/brand/<string:brand_name>", methods=["GET"])
def get_skus_by_brand(brand_name):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    brand = Brand.query.filter_by(name=brand_name).first_or_404(
        description=f"Brand {brand_name} not found"
    )
    skus_query = SKU.query.filter_by(brand_id=brand.id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    skus_list = []
    for sku in skus_query.items:
        category = Category.query.get(sku.category_id)
        subcategory = Subcategory.query.get(sku.subcategory_id)
        skus_list.append(
            {
                "material": sku.material,
                "material_description": sku.material_description,
                "uom": sku.uom,
                "brand": brand.name,
                "category": category.name if category else None,
                "subcategory": subcategory.name if subcategory else None,
                "product_line": sku.product_line,
            }
        )
    return jsonify(
        {
            "total": skus_query.total,
            "pages": skus_query.pages,
            "current_page": skus_query.page,
            "per_page": skus_query.per_page,
            "skus": skus_list,
        }
    )


@app.route(
    "/api/skus/brand/<string:brand_name>/subcategory/<string:subcategory_name>",
    methods=["GET"],
)
def get_skus_by_brand_and_subcategory(brand_name, subcategory_name):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    brand = Brand.query.filter_by(name=brand_name).first_or_404(
        description=f"Brand {brand_name} not found"
    )

    # Find the correct subcategory ID for the given brand and subcategory name
    subcategory = (
        Subcategory.query.join(Category)
        .filter(Subcategory.name == subcategory_name, Category.brand_id == brand.id)
        .first_or_404(
            description=f"Subcategory {subcategory_name} not found for brand {brand_name}"
        )
    )

    logging.debug(f"Brand ID: {brand.id}, Subcategory ID: {subcategory.id}")

    skus_query = SKU.query.filter_by(
        brand_id=brand.id, subcategory_id=subcategory.id
    ).paginate(page=page, per_page=per_page, error_out=False)

    logging.debug(f"SKUs found: {skus_query.total}")

    skus_list = []
    for sku in skus_query.items:
        category = Category.query.get(sku.category_id)
        skus_list.append(
            {
                "material": sku.material,
                "material_description": sku.material_description,
                "uom": sku.uom,
                "brand": brand.name,
                "category": category.name if category else None,
                "subcategory": subcategory.name,
                "product_line": sku.product_line,
            }
        )
    return jsonify(
        {
            "total": skus_query.total,
            "pages": skus_query.pages,
            "current_page": skus_query.page,
            "per_page": skus_query.per_page,
            "skus": skus_list,
        }
    )


@app.route("/api/skus/search", methods=["GET"])
def get_sku_by_material_or_description():
    material = request.args.get("material", type=int)
    material_description = request.args.get("material_description", type=str)

    if material:
        sku = SKU.query.filter_by(material=material).first_or_404(
            description=f"SKU with material {material} not found"
        )
    elif material_description:
        sku = SKU.query.filter_by(
            material_description=material_description
        ).first_or_404(
            description=f"SKU with material description '{material_description}' not found"
        )
    else:
        return (
            jsonify(
                {
                    "error": "Please provide either 'material' or 'material_description' as query parameters"
                }
            ),
            400,
        )

    brand = Brand.query.get(sku.brand_id)
    category = Category.query.get(sku.category_id)
    subcategory = Subcategory.query.get(sku.subcategory_id)

    return jsonify(
        {
            "material": sku.material,
            "material_description": sku.material_description,
            "uom": sku.uom,
            "brand": brand.name if brand else None,
            "category": category.name if category else None,
            "subcategory": subcategory.name if subcategory else None,
            "product_line": sku.product_line,
        }
    )


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
    app.run(debug=True, host="0.0.0.0")
