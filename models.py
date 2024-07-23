from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
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
