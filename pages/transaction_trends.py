import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Streamlit Page Title
st.title("Store Transactions & Item Sales Analysis")

# Load dataset (Ensure file path is correct)
@st.cache_data
def load_data():
    return pd.read_csv("/Users/alipuccio/Desktop/apex/Venmito-apekshamalik/output_data/transactions_(linked).csv")

transactions_df = load_data()

# Function to extract item name and quantity
def extract_item_and_quantity(item_str):
    match = re.match(r"(.*) \(x(\d+)\)", item_str)
    if match:
        item_name, quantity = match.groups()
        return item_name.strip(), int(quantity)
    return item_str.strip(), 1  # Default to 1 if no quantity is specified

# Ensure items are processed correctly
def process_items_column(items):
    if isinstance(items, list):  # If already a list, return as is
        return items
    if isinstance(items, str):  # If a string, clean and split
        return items.strip("[]").replace("'", "").split(", ")
    return []  # If NaN or invalid, return an empty list

# Apply function to fix the items column
transactions_df['items'] = transactions_df['items'].apply(process_items_column)

# Explode items into separate rows
transactions_exploded = transactions_df.explode('items')

# Extract clean item names and their quantities
transactions_exploded[['item_name', 'quantity']] = transactions_exploded['items'].apply(lambda x: pd.Series(extract_item_and_quantity(x)))

# Aggregate transactions correctly by summing up the quantities
store_item_counts = transactions_exploded.groupby(['store', 'item_name'])['quantity'].sum().reset_index()

### **🔹 Total Transactions Per Store**
store_counts = transactions_exploded['store'].value_counts().reset_index()
store_counts.columns = ['Store', 'Transaction Count']

st.subheader("Total Transactions Per Store")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=store_counts, x='Store', y='Transaction Count', palette='Set2', ax=ax)
ax.set_xlabel("Store", fontsize=12)
ax.set_ylabel("Total Transactions", fontsize=12)
ax.set_title("Total Transactions Per Store", fontsize=14)
plt.xticks(rotation=30, ha="right")
plt.grid(True)
st.pyplot(fig)  # Display in Streamlit

### **🔹 Top 3 Highest Selling Items Per Store**
top_items_per_store = (
    store_item_counts.groupby("store")
    .apply(lambda x: x.nlargest(3, "quantity"))
    .reset_index(drop=True)
)

st.subheader("Top 3 Highest Selling Items Per Store")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_items_per_store, x='store', y='quantity', hue='item_name', palette='Set2', ax=ax)
ax.set_xlabel("Store", fontsize=12)
ax.set_ylabel("Number of Transactions", fontsize=12)
ax.set_title("Top 3 Highest Selling Items Per Store", fontsize=14)
plt.xticks(rotation=30, ha="right")
plt.legend(title="Item", bbox_to_anchor=(1, 1))
plt.grid(True)
st.pyplot(fig)  # Display in Streamlit

### **🔹 Top 3 Lowest Selling Items Per Store**
lowest_items_per_store = (
    store_item_counts.groupby("store")
    .apply(lambda x: x.nsmallest(3, "quantity"))
    .reset_index(drop=True)
)

st.subheader("3 Lowest Selling Items Per Store")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=lowest_items_per_store, x='store', y='quantity', hue='item_name', palette='Set3', ax=ax)
ax.set_xlabel("Store", fontsize=12)
ax.set_ylabel("Number of Transactions", fontsize=12)
ax.set_title("3 Lowest Selling Items Per Store", fontsize=14)
plt.xticks(rotation=30, ha="right")
plt.legend(title="Item", bbox_to_anchor=(1, 1))
plt.grid(True)
st.pyplot(fig)  # Display in Streamlit
