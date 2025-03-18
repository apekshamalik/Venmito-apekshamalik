#!/usr/bin/env python
# coding: utf-8

# # Data Matching & Linking 

# In[4]:


import pandas as pd


# # Merge people data from JSON and YAML sources

# In[5]:


def merge_people_data(people_json_df, people_yml_df):
    """Merges people data from JSON and YAML sources into a single DataFrame."""
    people_yml_df.rename(columns={"phone": "telephone", "email": "email"}, inplace=True)
    people_yml_df[['city', 'country']] = people_yml_df['city'].str.split(', ', expand=True)
    people_yml_df[['first_name', 'last_name']] = people_yml_df['name'].str.split(n=1, expand=True)
    people_yml_df['last_name'] = people_yml_df['last_name'].fillna('')
    people_yml_df['id'] = people_yml_df['id'].astype(str).str.zfill(4)

    merged_df = pd.merge(
        people_json_df, 
        people_yml_df, 
        on=['id', 'email', 'telephone'], 
        how='outer', 
        suffixes=('_json', '_yml')
    )

    merged_df['first_name'] = merged_df['first_name_json'].fillna(merged_df['first_name_yml'])
    merged_df['last_name'] = merged_df['last_name_json'].fillna(merged_df['last_name_yml'])
    merged_df.drop(columns=['first_name_json', 'first_name_yml', 'last_name_json', 'last_name_yml'], inplace=True)
    merged_df['country'] = merged_df['country'].fillna('Unknown')

    print("\npeople_df Columns After Cleanup:", merged_df.columns.tolist())

    return merged_df


# # Link promotions data with people data

# In[1]:


import pandas as pd

def link_promotions(people_df, promotions_df):
    """Links promotions data with people data using email as the key and includes additional details."""

    # Standardize email formatting (strip spaces, lowercase)
    promotions_df['client_email'] = promotions_df['client_email'].str.strip().str.lower()
    people_df['email'] = people_df['email'].str.strip().str.lower()

    # Rename for merging
    promotions_df = promotions_df.rename(columns={"client_email": "email"})

    # Merge promotions with people
    promotions_linked_df = pd.merge(
        promotions_df, 
        people_df[['id', 'email', 'telephone', 'first_name', 'last_name', 'city', 'country']], 
        on=['email'], 
        how="left"
    )

    # Ensure correct 'id' column is used
    if 'id_y' in promotions_linked_df.columns:
        promotions_linked_df['id'] = promotions_linked_df['id_y']
        promotions_linked_df.drop(columns=['id_x', 'id_y'], inplace=True, errors='ignore')

    # Drop rows where no match was found (i.e., unknown people)
    promotions_linked_df = promotions_linked_df.dropna(subset=['id'])

    return promotions_linked_df


# # Link transactions data with people data

# In[7]:


def link_transactions(people_df, transactions_df):
    """Links transactions data with people data using phone numbers as the key."""
    if transactions_df is None:
        print("\nERROR: transactions_df is None! Check XML parsing function.")
        return None

    if 'items' in transactions_df.columns:
        transactions_df['items'] = transactions_df['items'].apply(lambda x: x if isinstance(x, list) else [])
    else:
        transactions_df['items'] = [[]] * len(transactions_df)

    print("\nSample transactions_df (after fixing items column):")
    print(transactions_df.head())

    transactions_linked_df = transactions_df.merge(
        people_df[['id', 'telephone']], 
        left_on="phone", 
        right_on="telephone", 
        how="left"
    ).drop(columns=["telephone"])

    return transactions_linked_df


# # Function to link transfers data with people data

# In[8]:


def link_transfers(people_df, transfers_df):
    """Links transfers data with people data using sender and recipient IDs, and adds country information."""

    # Ensure ID columns are strings with 4-digit format
    transfers_df['sender_id'] = transfers_df['sender_id'].astype(str).str.zfill(4)
    transfers_df['recipient_id'] = transfers_df['recipient_id'].astype(str).str.zfill(4)
    people_df['id'] = people_df['id'].astype(str).str.zfill(4)

    # Extract country from location dictionary
    people_df["country"] = people_df["location"].apply(lambda x: x.get("Country", "Unknown") if isinstance(x, dict) else "Unknown")

    # Merge Sender Details (Name + Country)
    transfers_df = transfers_df.merge(
        people_df[['id', 'first_name', 'last_name', 'country']], 
        left_on="sender_id", 
        right_on="id", 
        how="left"
    ).rename(columns={
        "first_name": "sender_first_name",
        "last_name": "sender_last_name",
        "country": "sender_country"
    })

    # Merge Recipient Details (Name + Country)
    transfers_df = transfers_df.merge(
        people_df[['id', 'first_name', 'last_name', 'country']], 
        left_on="recipient_id", 
        right_on="id", 
        how="left"
    ).rename(columns={
        "first_name": "recipient_first_name",
        "last_name": "recipient_last_name",
        "country": "recipient_country"
    })

    # Drop duplicate ID columns after merging
    transfers_df.drop(columns=["id_x", "id_y"], inplace=True, errors="ignore")

    return transfers_df



