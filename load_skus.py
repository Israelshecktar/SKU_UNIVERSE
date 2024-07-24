import pandas as pd
from sqlalchemy import create_engine
from models import db, SKU
from config import Config

# Load the Excel file into a pandas DataFrame
df = pd.read_excel('SKU Pricing.xlsx')

# Rename the columns to match the SKU table in the database
df.rename(columns={
    'Column1': 'sku_id',
    'Column2': 'material',
    'Column3': 'Material Description',
    'Column4': 'unit',
    'Column5': 'Brand',
    'Column6': 'product line',
    'Column7': 'category'
}, inplace=True)

# Drop the 'amount' column as it's not needed
df.drop('amount', axis=1, inplace=True)

# Create a SQLAlchemy engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Connect to the database
with engine.connect() as connection:
    # Begin a transaction
    with connection.begin() as transaction:
        try:
            # Insert the data into the SKU table
            df.to_sql('skus', con=connection, if_exists='append', index=False)
            
            # Commit the transaction
            transaction.commit()
            print("Data loaded successfully into the SKU table.")
        except Exception as e:
            # Rollback the transaction in case of error
            transaction.rollback()
            print(f"An error occurred: {e}")
