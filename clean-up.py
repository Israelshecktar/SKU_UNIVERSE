from app import app, db
from models import Brand, Category, SKU

def clean_up_categories():
    valid_categories = {
        "DULUX": ["water-based", "solvent-based", "Industrials"],
        "SANDTEX": ["water-based", "solvent-based", "SANDTEX industrials"],
        "CAPLUX": ["water-based", "solvent-based", "CAPLUX specials"],
        "Hempel": [],
        "Project": ["water-based", "solvent-based", "Project Industrials"],
    }

    for brand_name, categories in valid_categories.items():
        brand = Brand.query.filter_by(name=brand_name).first()
        if brand:
            existing_categories = Category.query.filter_by(brand_id=brand.id).all()
            for category in existing_categories:
                if category.name not in categories:
                    if categories:  # Check if categories list is not empty
                        valid_category = Category.query.filter_by(name=categories[0], brand_id=brand.id).first()
                        SKUs_to_update = SKU.query.filter_by(category_id=category.id).all()
                        for sku in SKUs_to_update:
                            sku.category_id = valid_category.id
                        db.session.commit()
                    # Delete the category
                    db.session.delete(category)
            db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        clean_up_categories()
