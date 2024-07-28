from models import db, Brand, Category


def add_initial_data():
    brands = {
        "DULUX": ["water-based", "solvent-based", "Industrials"],
        "SANDTEX": ["water-based", "solvent-based", "industrials", "Sandtex specials"],
        "CAPLUX": ["water-based", "solvent-based", "CAPLUX specials"],
        "Hempel": [],
        "Project": ["water-based", "solvent-based", "Project Industrials"],
    }

    for brand_name, categories in brands.items():
        brand = Brand.query.filter_by(name=brand_name).first()
        if not brand:
            brand = Brand(name=brand_name)
            db.session.add(brand)
            db.session.commit()

        for category_name in categories:
            category = Category.query.filter_by(
                name=category_name, brand_id=brand.id
            ).first()
            if not category:
                category = Category(name=category_name, brand_id=brand.id)
                db.session.add(category)
                db.session.commit()
