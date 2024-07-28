import pandas as pd
from models import db, SKU, Brand, Category, Subcategory
from app import app

def load_data_from_excel(file_path):
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)

        # Drop rows with NaN in 'Brand' and 'Product Line' columns
        df = df.dropna(subset=["Brand", "Product Line"])

        # Ensure 'Material' column is treated as an integer
        df["Material"] = df["Material"].astype(int)

        # Fill NaN values in 'Product Type' with a default value
        df["Product Type"] = df["Product Type"].fillna("Unknown")

        with app.app_context():
            # Empty the SKU table before loading new data
            db.session.query(SKU).delete()
            db.session.commit()

            # Load data into the SKU table
            for index, row in df.iterrows():
                # Get the brand ID
                brand = Brand.query.filter_by(name=row["Brand"]).first()
                if not brand:
                    print(f"Brand {row['Brand']} not found in the database.")
                    continue

                # Get the category ID
                category = Category.query.filter_by(name=row["Product Line"], brand_id=brand.id).first()
                if not category:
                    category = Category(name=row["Product Line"], brand_id=brand.id)
                    db.session.add(category)
                    db.session.commit()

                # Get the subcategory ID
                subcategory = Subcategory.query.filter_by(name=row["Product Type"], category_id=category.id).first()
                if not subcategory:
                    subcategory = Subcategory(name=row["Product Type"], category_id=category.id)
                    db.session.add(subcategory)
                    db.session.commit()

                # Check if SKU already exists to avoid duplicates
                existing_sku = SKU.query.filter_by(
                    material=row["Material"],
                    material_description=row["Material Description"] if pd.notna(row["Material Description"]) else "",
                    uom=row["UoM"] if pd.notna(row["UoM"]) else "",
                    brand_id=brand.id,
                    category_id=category.id,
                    subcategory_id=subcategory.id,
                    product_line=row["Product Line"]
                ).first()
                if existing_sku:
                    print(f"SKU with material {row['Material']} already exists. Skipping duplicate.")
                    continue

                # Create SKU with 'Product Line' and 'Product Type' (subcategory)
                sku = SKU(
                    material=row["Material"],
                    material_description=row["Material Description"] if pd.notna(row["Material Description"]) else "",
                    uom=row["UoM"] if pd.notna(row["UoM"]) else "",
                    brand_id=brand.id,
                    category_id=category.id,
                    subcategory_id=subcategory.id,
                    product_line=row["Product Line"]
                )
                db.session.add(sku)
            db.session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    load_data_from_excel("SKU Pricing.xlsx")

print("SKU table has been reloaded successfully.")
