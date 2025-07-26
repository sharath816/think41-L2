import pandas as pd
from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce_db"]

# File paths
DATA_PATH = "../data"

def load_csv_to_collection(file_name, collection_name):
    df = pd.read_csv(f"{DATA_PATH}/{file_name}")
    records = df.to_dict(orient="records")
    if records:
        db[collection_name].insert_many(records)
        print(f"✅ Inserted {len(records)} records into '{collection_name}'")

if __name__ == "__main__":
    load_csv_to_collection("products.csv", "products")
    load_csv_to_collection("orders.csv", "orders")
    load_csv_to_collection("users.csv", "users")
    load_csv_to_collection("order_items.csv", "order_items")
    load_csv_to_collection("inventory_items.csv", "inventory_items")
    load_csv_to_collection("distribution_centers.csv", "distribution_centers")
