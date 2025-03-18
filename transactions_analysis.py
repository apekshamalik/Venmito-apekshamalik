import pandas as pd

file_path = "/Users/apeksha/Desktop/Xtillion_Venmito/Venmito-apekshamalik/output_data/transactions_(linked).csv"
transactions_df = pd.read_csv(file_path)

# Explode items list into individual rows
transactions_df = transactions_df.explode("items")

# Count occurrences of each item
best_sellers = transactions_df["items"].value_counts()

print("🔹 Best-selling items:")
print(best_sellers.head(10))

# Extract item name and quantity
transactions_df["item_clean"] = transactions_df["items"].str.extract(r'(.+) \(x\d+\)')
transactions_df["quantity"] = transactions_df["items"].str.extract(r'x(\d+)').astype(float)

# Calculate total sales per store
store_sales = transactions_df.groupby("store")["quantity"].sum().sort_values(ascending=False)

print("🔹 Store with highest sales:")
print(store_sales.head(10))
