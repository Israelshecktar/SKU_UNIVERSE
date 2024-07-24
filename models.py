from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    categories = db.relationship('Category', backref='brand', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True)

class Subcategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

class SKU(db.Model):
    __tablename__ = 'skus'
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(255), nullable=False)
    material_description = db.Column(db.String(255))
    amount = db.Column(db.Numeric(10, 2))
    unit = db.Column(db.String(10))
    per_unit = db.Column(db.String(10))
    uom = db.Column(db.String(10))
    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'))

def add_initial_data():
    brands = {
        'DULUX': [
            'water-based', 'solvent-based', 'Industrials'
        ],
        'SANDTEX': [
            'water-based', 'solvent-based'
        ],
        'CAPLUX': [
            'water-based', 'solvent-based', 'CAPLUX specials'
        ],
        'Hempel': [],
        'Project': [
            'water-based', 'solvent-based', 'Industrials'
        ]
    }

    for brand_name, categories in brands.items():
        brand = Brand.query.filter_by(name=brand_name).first()
        if not brand:
            brand = Brand(name=brand_name)
            db.session.add(brand)
            db.session.commit()

        for category_name in categories:
            category = Category.query.filter_by(name=category_name, brand_id=brand.id).first()
            if not category:
                category = Category(name=category_name, brand_id=brand.id)
                db.session.add(category)
                db.session.commit()

if __name__ == '__main__':
    db.create_all()
    add_initial_data()
