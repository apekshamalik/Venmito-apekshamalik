#!/usr/bin/env python
# coding: utf-8

# # Data loader

# # Loading CSV, XML, YML, and JSON data

# In[4]:


import pandas as pd
import yaml
import json
import xml.etree.ElementTree as ET


# # YAML Loader

# In[5]:


def load_yaml(file_path):
    """Loads data from a YAML file into a Pandas DataFrame."""
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return pd.DataFrame(data)


# # Load and display YAML dataframe

# In[6]:


people_yml_df = load_yaml("data/people.yml")
print(people_yml_df.head())


# # JSON Loader

# In[7]:


def load_json(file_path):
    """Loads data from a JSON file into a Pandas DataFrame."""
    with open(file_path, "r") as file:
        data = json.load(file)
    return pd.DataFrame(data)


# # Load and display JSON dataframe

# In[8]:


people_json_df = load_json("data/people.json")
print(people_json_df.head())


# # CSV Loader

# In[9]:


def load_csv(file_path):
    """Loads data from a CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


# # Load and display CSV datafme

# In[10]:


transfers_df = load_csv("data/transfers.csv")
print(transfers_df.head())


# # XML Transactions Parser

# # Nested elements and structure of XML requires iteration to structure items in transaction into list

# In[11]:


def parse_transactions_xml(file_path):
    """Parses transaction data from an XML file into a Pandas DataFrame."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        transactions = []

        for transaction in root.findall("transaction"):
            transaction_data = {
                "id": transaction.attrib.get("id"),
                "phone": transaction.find("phone").text if transaction.find("phone") is not None else None,
                "store": transaction.find("store").text if transaction.find("store") is not None else None
            }
        # Extract items as a list
            items_list = []
            items_tag = transaction.find("items")
            if items_tag is not None:
                for item in items_tag.findall("item"):
                    item_name_tag = item.find("item")
                    item_name = item_name_tag.text if item_name_tag is not None else "Unknown"
                    quantity_tag = item.find("quantity")
                    quantity = quantity_tag.text if quantity_tag is not None else "1"
                    items_list.append(f"{item_name} (x{quantity})")

            transaction_data["items"] = items_list
            transactions.append(transaction_data)

        df = pd.DataFrame(transactions)
        df["items"] = df["items"].apply(lambda x: x if isinstance(x, list) else [])
        return df

    except Exception as e:
        print(f"❌ Error parsing transactions XML: {e}")
        return None


# # Load and display XML dataframe

# In[12]:


transactions_df = parse_transactions_xml("data/transactions.xml")
print(transactions_df.head())

