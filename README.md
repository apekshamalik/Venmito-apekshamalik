# Venmito Data Engineering Project

## Introduction

Hello and welcome to this data engineering project for Venmito. We're excited to see how you tackle this challenge and provide us with a solution that can bring together disparate data sources into an insightful and valuable resource.

Venmito is a payment company that allows users to transfer funds to other users and pay in participant stores. The company has several data files in various formats. Our goal is to organize all of this information to gain insights about our clients and transactions. We believe that there is an immense value hidden in these data files, and we are looking for a solution that can help us extract and utilize this value.

We have five files:

- `people.json`
- `people.yml`
- `transfers.csv`
- `transactions.xml`
- `promotions.csv`

Each of these files contains different pieces of information about our clients, their transactions, transfers and promotions.

Your task is to develop a solution that can read these files, match and conform the data, and provide a way to consume this data.

## Requirements

1. **Data Ingestion**: Your solution should be able to read and load data from all the provided files. Take into account that these files are in different formats (JSON, YAML, CSV, XML).

2. **Data Matching and Conforming**: Once the data is loaded, your solution should be capable of matching and conforming the data across these files. This includes identifying common entities, resolving inconsistencies, and organizing the data into a unified format. Furthermore, the consolidated data should not only be transient but also persistent. This persistence should be achieved using appropriate methods such as storing in a file, database, or other suitable data storage solutions, and not restricted to just a variable in memory. This way, the integrity and availability of the consolidated data are ensured for future use and analysis.

3. **Data Analysis**: Your solution should be able to process the conformed data to derive insights about our clients and transactions. This would involve implementing data aggregations, calculating relevant metrics, and identifying patterns. These insights will be invaluable in helping us understand our clientele and transaction trends better. Examples of things, but is not restricted to, we want to be able to see are:
    - Which clients have what type of promotion?
    - Give suggestions on how to turn "No" responses from clients in the promotions file.
    - Insights on stores, like:
        - What item is the best seller?
        - What store has had the most profit?
        - Etc.
    - How can we use the data we got from the transfer file?
  
    These are only suggestions. Please don't limit yourself to only these examples and explore in your analysis any other suggestions could be beneficial for Venmito.

4. **Data Output**: The final output of your solution should enable us to consume the reorganized and analyzed data in a meaningful way. This could be, but is not restricted to, a command line interface (CLI), a database with structured schemas, a GUI featuring interactive visualizations, a Jupyter Notebook, or a RESTful API. We invite you to leverage other innovative methods that you believe would be beneficial for a company like Venmito. Please provide at least 2 data consumption methods, 1 for the non-technical team and 1 for the technical team.

5. **Code**: The code for your solution should be well-structured and comprehensible, with comments included where necessary. Remember, the quality and readability of the code will be a significant factor in the evaluation of the final deliverable.

Note: The examples provided in these requirements (such as GUI, RESTful API etc.) are purely illustrative. You are free to employ any solution or technology you deem fit for fulfilling these requirements

## Deliverables

1. Source code.
2. A README file with your name, email, a description of your solution, your design decisions, and clear instructions on how to run your code.
3. A method to consume the reorganized and analyzed data.

## Instructions for Submission

1. Complete your project as described above in a branch within your fork.
2. Write a detailed README file with your name, email, a description explaining your approach, the technologies you used, and provides clear instructions on how to run your code.
3. Submit your project by uploading a zip file to the provided URL.

We look forward to seeing your solution!

Thank you,

Venmito

## DISCLAIMER:

This project and its contents are the exclusive property of Xtillion, LLC and are intended solely for the evaluation of the individual to whom it was provided. Any distribution, reproduction, or unauthorized use is strictly prohibited. By accessing and using this project, you agree to abide by these conditions. Failure to comply with these terms may result in legal action.

Please note that this project is provided "as is", without warranty of any kind, express or implied. Xtillion is not liable for any damages or claims that might arise from using or misusing this project.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Apeksha's Notes

This project is designed to **automate** data processing and offer a clear analytical approach** for understanding how Venmito’s financial ecosystem operates.  

Take a look at the interactive dashboard for plots and analysis of the provided data.
https://venmito-apekshamalik.streamlit.app/


---

##  Technologies & Tools Used**  

|---------------|------------|
| **Python** | Primary programming language |
| **Pandas** | Data ingestion & transformation |
| **NumPy** | Numeric computations |
| **Matplotlib & Seaborn** | Data visualization |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Web-based interactive dashboards |
| **Jupyter Notebook** | Data exploration & reporting |

This stack was chosen to allow for **scalable**, **efficient**, and **insightful** analysis of Venmito’s financial data.  
---

## **📥 Installation & Setup**  
This project is designed to be simple to set up and run. Follow these steps:  

### **Clone the Repository**
```bash
git clone https://github.com/apekshamalik/Venmito-apekshamalik.git
cd Venmito-apekshamalik
```

### **Create a Virtual Environment**  
To avoid dependency conflicts, create a Python virtual environment:  
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### **Install Required Dependencies**  
```bash
pip install -r requirements.txt
```

### ** Run the Analysis**  
Execute the main analysis pipeline:  
```bash
python main.py
```
This will:  
Load & clean the data  
Link related datasets  
Generate output files for further analysis  

For **interactive dashboards**, launch **Streamlit**:
```bash
streamlit run streamlit.py
```

To open **Jupyter Notebooks** for further exploration:
```bash
jupyter notebook
```
Then navigate to and open any `.ipynb` file.

---

## **Project Structure**
```
Venmito-apekshamalik
├── data              # Raw data files (JSON, CSV, XML, YAML)
├── output_data       # Processed & linked data (CSV)
├── notebooks         # Jupyter Notebooks for analysis
├── scripts
│   ├── data_loader.py   # Parses and loads data
│   ├── data_matching.py # Links datasets
│   ├── promotions_analysis.py
│   ├── transactions_analysis.py
│   ├── transfer_analysis.py
├── main.py              # Main execution script
├── streamlit.py         # Interactive dashboard
├── requirements.txt     # Dependencies
├── README.md            # Documentation
```

---

## ** How the Data is Linked**
One of the most critical aspects of this project is **merging different data sources** into a unified dataset.  

### **Merging People Data**
- Data is pulled from **YAML** and **JSON** sources.
- The unique identifier is **`id`**, ensuring records from both formats are properly combined.

### **Linking Promotions**
- Customers in the **Promotions dataset** are matched via **email**.
- Emails are **cleaned** (stripped & lowercased) to avoid mismatches.
- This allows us to track **who received what promotion** and their **response (`Yes`/`No`)**.

### **Connecting Transactions**
- Transactions are linked using **phone numbers** and `person_id` to **assign purchases to specific users**.
- This enables **trend analysis on store purchases**.

### **Mapping Transfers**
- Transfers are linked via **sender and recipient IDs**.
- City/country details are extracted, allowing for:
  - **Tracking of global financial flows**
  - **Heatmaps for high-transfer regions**
  - **Identifying frequent senders & recipients**

---

## *Insights & Analysis**
This project allows for **powerful analysis** across multiple dimensions.

### ** Promotions Analysis**
 **Understanding Customer Behavior**  
- Who responds to promotions?  
- What **types of promotions** get the most engagement?  
- Do users who **spend more money** engage more?  

 **Flipping "No" Responses to "Yes"**  
- Identify **common traits** of users who respond "Yes" (e.g., frequent shoppers).  
- Test **personalized offers** based on past behavior.  
- Adjust **timing and messaging** to maximize engagement.  

 **Visualization:**
- **Distribution of promotion types**  
- **Response rate analysis (`Yes` vs. `No`)**  

### **Transfer Analysis**
**Tracking Money Flow**  
- **Who sends the most money?**  
- **Which countries/cities receive the most?**  
- **How does transfer volume change over time?**  

 **Visualization:**
- **Heatmaps showing financial hotspots**  
- **Top sender/receiver rankings**  

### **Transaction Analysis**
 **Customer Purchase Behavior**  
- **What stores do people shop at most?**  
- **How frequently do they make purchases?**  
- **How do transaction volumes change daily/weekly/monthly?**  

 **Visualization:**
- **Time-series plots for transactions per day/week/month**  
- **Store-based analysis to determine top sellers**  

### ** Store Insights**
 **Finding the Best-Performing Stores**
- **What items sell the most?**  
- **Which stores generate the highest revenue?**  

 **Visualization:**
- **Top-selling items chart**  
- **Revenue comparison across stores**  


---
