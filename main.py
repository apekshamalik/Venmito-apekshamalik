import logging
import os
import pandas as pd
from data_loader import load_yaml, load_json, load_csv, parse_transactions_xml
from data_matching import merge_people_data, link_promotions, link_transactions, link_transfers

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define file paths
DATA_FILES = {
    "people_yaml": "data/people.yml",
    "people_json": "data/people.json",
    "transfers": "data/transfers.csv",
    "promotions": "data/promotions.csv",
    "transactions": "data/transactions.xml"
}

# Create output directory for CSV files
OUTPUT_DIR = "output_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_to_csv(df, filename):
    """Save DataFrame to CSV file."""
    if df is not None and not df.empty:
        file_path = os.path.join(OUTPUT_DIR, f"{filename}.csv")
        df.to_csv(file_path, index=False)  # Save DataFrame to CSV without index
        logging.info(f"✅ Saved {filename}.csv to {OUTPUT_DIR}/")
    else:
        logging.warning(f" {filename} DataFrame is empty. Skipping CSV save.")


def main():
    """Main function to load data, merge datasets, and save results."""
    logging.info("🚀 Starting Data Ingestion...\n")

    try:
        # Load datasets
        people_yml_df = load_yaml(DATA_FILES["people_yaml"])
        people_json_df = load_json(DATA_FILES["people_json"])
        transfers_df = load_csv(DATA_FILES["transfers"])
        promotions_df = load_csv(DATA_FILES["promotions"])
        transactions_df = parse_transactions_xml(DATA_FILES["transactions"])

        if transactions_df is None or transactions_df.empty:
            logging.warning("⚠ Transactions DataFrame is empty. Check XML parsing.")

        # Merge people data
        people_df = merge_people_data(people_json_df, people_yml_df)

        # Link datasets
        promotions_linked_df = link_promotions(people_df, promotions_df)
        transactions_linked_df = link_transactions(people_df, transactions_df)
        transfers_linked_df = link_transfers(people_df, transfers_df)

        # Rename id columns in transactions for clarity
        if 'id_x' in transactions_linked_df.columns and 'id_y' in transactions_linked_df.columns:
            transactions_linked_df.rename(columns={'id_x': 'transaction_id', 'id_y': 'person_id'}, inplace=True)

        # Store all DataFrames in a dictionary for easier iteration
        datasets = {
            "People (Merged)": people_df,
            "Promotions (Linked)": promotions_linked_df,
            "Transactions (Linked)": transactions_linked_df,
            "Transfers (Linked)": transfers_linked_df
        }

        # Display and save each dataset
        for name, df in datasets.items():
            if df is not None and not df.empty:
                logging.info(f"\n{name}:\n{df.head()}\n")
                save_to_csv(df, name.lower().replace(" ", "_"))  # Save as CSV
            else:
                logging.warning(f"\n{name}: DataFrame is empty or not loaded correctly.\n")

    except Exception as e:
        logging.error(f"🚨 Error during data processing: {e}", exc_info=True)


if __name__ == "__main__":
    main()
