import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title
st.title("Funds Transfer Analysis")

# Load dataset (Make sure file path is correct)
@st.cache_data
def load_data():
    return pd.read_csv("output_data/transfers_(linked).csv")  # Ensure you're using the right file

transfers_df = load_data()

st.subheader("Amount Sent by Region")

# Dropdown for selecting a sender country (using Streamlit)
sender_country = st.selectbox("Select Sender Country", transfers_df['sender_country'].unique())

# Filter data based on selection
filtered_df = transfers_df[transfers_df['sender_country'] == sender_country]
summary = filtered_df.groupby('recipient_country')['amount'].sum().sort_values(ascending=False)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 5))
summary.plot(kind='bar', color='blue', alpha=0.7, ax=ax)
ax.set_title(f"Total Amount Sent from {sender_country}")
ax.set_ylabel("Amount Transferred")
ax.set_xlabel("Recipient Country")
plt.xticks(rotation=45)

# Display plot in Streamlit
st.pyplot(fig)


st.subheader("Monthly Trends in Fund Transfers")

transfers_df['date'] = pd.to_datetime(transfers_df['date'])

# Extract month and weekday for seasonal trend analysis
transfers_df['month'] = transfers_df['date'].dt.month_name()
transfers_df['weekday'] = transfers_df['date'].dt.day_name()

# Aggregate transaction counts per month
monthly_trends = transfers_df.groupby('month').size().reset_index(name='transaction_count')

# Aggregate transaction counts per weekday
weekday_trends = transfers_df.groupby('weekday').size().reset_index(name='transaction_count')

# Order months and weekdays properly
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

monthly_trends['month'] = pd.Categorical(monthly_trends['month'], categories=month_order, ordered=True)
weekday_trends['weekday'] = pd.Categorical(weekday_trends['weekday'], categories=weekday_order, ordered=True)

# Sort values for plotting
monthly_trends = monthly_trends.sort_values('month')
weekday_trends = weekday_trends.sort_values('weekday')

### **Plot Monthly Trends**
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_trends, x='month', y='transaction_count', marker='o', linestyle='-', ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Number of Transactions")
ax.set_title("Seasonal Trends: Transactions Per Month")
plt.xticks(rotation=45, ha="right")
plt.grid(True)
st.pyplot(fig)  # Show plot in Streamlit

### **Plot Weekday Trends**
st.subheader("Weekly Trends in Fund Transfers")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=weekday_trends, x='weekday', y='transaction_count', palette='Set2', ax=ax)
ax.set_xlabel("Day of the Week")
ax.set_ylabel("Number of Transactions")
ax.set_title("Weekly Trends: Transactions Per Day")
plt.xticks(rotation=30, ha="right")
plt.grid(True)
st.pyplot(fig)


