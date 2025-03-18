#What clients received what promotions

import pandas as pd

# Load promotions data
file_path = "/Users/apeksha/Desktop/Xtillion_Venmito/Venmito-apekshamalik/output_data/promotions_(linked).csv"
promotions_df = pd.read_csv(file_path)

# Show clients and their promotions
client_promotions = promotions_df[['email', 'promotion', 'responded']]
print(client_promotions.head())

# Count Yes vs. No responses for each promotion
response_counts = promotions_df.groupby("promotion")["responded"].value_counts().unstack()

# Calculate conversion rate
response_counts["conversion_rate"] = response_counts["Yes"] / (response_counts["Yes"] + response_counts["No"]) * 100

print(response_counts)

# Insights:
# - Find promotions with low conversion rates.
# - Offer discounts for clients who previously said "No".
# - Use personalized promotions based on past transactions.