import pandas as pd
from models import db, SKU, Brand, Category
from app import app


def load_data_from_excel(file_path):
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

                # Create SKU with 'Product Line' as per user request
                sku = SKU(
                    material=row["Material"],
                    material_description=row["Material Description"],
                    uom=row["UoM"],
                    brand_id=brand.id,
                    category_id=category.id,
                    product_line=product_line,  # Add product line to SKU
                )
                db.session.add(sku)
            else:
                print(f"Invalid brand value: {row['Brand']} at row {index + 2}")
        db.session.commit()


if __name__ == "__main__":
    load_data_from_excel("SKU Pricing.xlsx")
