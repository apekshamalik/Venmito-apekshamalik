import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Page Title
st.title("Promotions Analysis")

# Load dataset (Ensure file path is correct)
@st.cache_data
def load_data():
    return pd.read_csv("output_data/promotions_(linked).csv")

promotions_df = load_data()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Page Title
st.title("Promotion Analysis Dashboard")

# Load dataset (Ensure correct file path)
@st.cache_data
def load_data():
    return pd.read_csv("/Users/alipuccio/Desktop/apex/Venmito-apekshamalik/output_data/promotions_(linked).csv")

promotions_df = load_data()

### **🔹 1. Distribution of Promotions**
st.subheader("Distribution of Promotion Types")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(y=promotions_df["promotion"], palette="Blues_r", order=promotions_df["promotion"].value_counts().index, ax=ax)

ax.set_xlabel("Count")
ax.set_ylabel("Promotion Type")
ax.set_title("Distribution of Promotion Types")
plt.grid(axis="x", linestyle="--", alpha=0.7)

st.pyplot(fig)

### **🔹 2. Responses to Promotions (Stacked Bar Chart)**
st.subheader("Responses to Promotions (Sorted by Yes Responses)")

# Group responses by promotion type
response_summary = promotions_df.groupby(['promotion', 'responded']).size().unstack()

# Sort promotions by the number of "Yes" responses
response_summary = response_summary.sort_values(by="Yes", ascending=True)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 5))
response_summary.plot(kind='bar', stacked=True, colormap='viridis', ax=ax)

ax.set_title("Responses to Promotions (Sorted by Yes Responses)")
ax.set_ylabel("Number of Responses")
ax.set_xlabel("Promotion Type")
plt.xticks(rotation=45)
ax.legend(title="Response", labels=["No", "Yes"])

st.pyplot(fig)

### **🔹 3. Rejection Rates by Country (Dropdown for Promotion Selection)**
st.subheader("Rejection Rates by Country for Selected Promotion")

# Dropdown for selecting a promotion
selected_promotion = st.selectbox("Select a Promotion", promotions_df['promotion'].unique())

# Filter data for selected promotion
filtered_data = promotions_df[promotions_df['promotion'] == selected_promotion]

# Calculate rejection rates by country for the selected promotion
country_rejection_rates = (
    filtered_data[filtered_data['responded'] == "No"]
    .groupby('country')
    .size()
    .reset_index(name='rejection_count')
)

# Calculate total responses per country to get percentages
total_responses_per_country = filtered_data.groupby('country').size().reset_index(name='total_count')

# Merge data to compute rejection rate percentage
country_rejection_rates = country_rejection_rates.merge(total_responses_per_country, on='country', how='right')
country_rejection_rates['rejection_count'] = country_rejection_rates['rejection_count'].fillna(0)
country_rejection_rates['rejection_rate'] = (country_rejection_rates['rejection_count'] / country_rejection_rates['total_count']) * 100

# Plot rejection rates by country
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=country_rejection_rates, x='country', y='rejection_rate', palette='Reds', ax=ax)

ax.set_xlabel("Country")
ax.set_ylabel("Rejection Rate (%)")
ax.set_title(f"Rejection Rates by Country for {selected_promotion}")
plt.xticks(rotation=30, ha="right")
plt.grid(axis='y', linestyle='--', alpha=0.7)

st.pyplot(fig)

promotions_df['response_numeric'] = promotions_df['responded'].map({'Yes': 1, 'No': 0})

# Aggregate acceptance rate per country and promotion
promotion_acceptance = promotions_df.groupby(['country', 'promotion'])['response_numeric'].mean().reset_index()

# **Dropdown for selecting a country**
selected_country = st.selectbox("Select a Country", promotions_df['country'].unique())

# Filter data for selected country
filtered_data = promotion_acceptance[promotion_acceptance['country'] == selected_country]

# **Plot Acceptance Rate**
st.subheader(f"Promotion Acceptance Rate in {selected_country}")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='promotion', y='response_numeric', data=filtered_data, palette='Set2', ax=ax)

ax.set_xlabel("Promotion Type")
ax.set_ylabel("Acceptance Rate (%)")
ax.set_title(f"Promotion Acceptance Rate in {selected_country}", pad=20)
plt.xticks(rotation=45)
plt.ylim(0, 1)

# Add percentage labels
for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2, p.get_height() + 0.03, f"{p.get_height()*100:.1f}%", 
            ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()  # Prevent overlapping
st.pyplot(fig)  # Display plot in Streamlit