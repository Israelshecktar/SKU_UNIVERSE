import pandas as pd
from models import db, SKU, Brand, Category, Subcategory
from app import app

# Predefined brand-category mapping
brands = {
    "DULUX": ["water-based", "solvent-based", "Industrials"],
    "SANDTEX": ["water-based", "solvent-based", "industrials", "Sandtex specials"],
    "CAPLUX": ["water-based", "solvent-based", "CAPLUX specials"],
    "Hempel": [],
    "Project": ["water-based", "solvent-based", "Project Industrials"],
}

def load_data_from_excel(file_path):
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)

        # Drop rows with NaN in 'Brand' and 'Product Line' columns
        df = df.dropna(subset=["Brand", "Product Line"])

        # Ensure 'Material' column is treated as an integer
        df["Material"] = df["Material"].astype(int)

        with app.app_context():
            for index, row in df.iterrows():
                # Check if 'Brand' value is a string to avoid 'nan' values
                if isinstance(row["Brand"], str):
                    brand = Brand.query.filter_by(name=row["Brand"]).first()
                    if not brand:
                        print(f"Brand {row['Brand']} not found in the database.")
                        continue

                    # Use 'Product Line' as category
                    product_line = row["Product Line"]
                    category = Category.query.filter_by(
                        name=product_line, brand_id=brand.id
                    ).first()
                    if not category:
                        category = Category(name=product_line, brand_id=brand.id)
                        db.session.add(category)
                        db.session.commit()

                    # Handle NaN values in 'Product Type'
                    if pd.isna(row["Product Type"]):
                        print(f"Skipping row {index + 2} due to NaN in 'Product Type'")
                        continue

                    # Determine subcategory based on 'Product Type'
                    subcategory_name = row["Product Type"]
                    subcategory = Subcategory.query.filter_by(
                        name=subcategory_name, category_id=category.id
                    ).first()
                    if not subcategory:
                        subcategory = Subcategory(name=subcategory_name, category_id=category.id)
                        db.session.add(subcategory)
                        db.session.commit()

                    # Handle NaN values in 'Material Description' and 'UoM'
                    material_description = row["Material Description"] if pd.notna(row["Material Description"]) else ""
                    uom = row["UoM"] if pd.notna(row["UoM"]) else ""

                    # Create SKU with 'Product Line' and 'Product Type' (subcategory)
                    sku = SKU(
                        material=row["Material"],
                        material_description=material_description,
                        uom=uom,
                        brand_id=brand.id,
                        category_id=category.id,
                        subcategory_id=subcategory.id,
                        product_line=product_line,  # Add product line to SKU
                    )
                    db.session.add(sku)
                else:
                    print(f"Invalid brand value: {row['Brand']} at row {index + 2}")
            db.session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    load_data_from_excel("SKU Pricing.xlsx")
