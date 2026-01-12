## PROJECT TITLE: ANALYSING THE IMPACT OF CUSTOMER COMPLAINT PATTERNS ON OPERATIONAL EFFICIENCY

## OVERVIEW
This project analyzes customer complaint data at the Water and Sanitation Corporation (WASAC) to understand how complaint patterns relate to operational efficiency and service delivery. Using a structured data pipeline, summary statistics, and an interactive Streamlit dashboard, the project transforms raw complaint records into clear, actionable insights. The analysis focuses on complaint distribution, resolution performance, and geographic and organizational patterns, supporting evidence-based decision-making and improved monitoring of service quality across branches and districts.

# Description of the repository structure

The repository is organized to reflect the complete analytical workflow of the project, from data preparation to dashboard deployment.  All materials are in the main folder (FINAL-PROJECT-DSCBI) with NEW_ENV\Scripts_And_Data which contain the following Python Scripts: ```Data_P.py``` for data processor, ```Dashboard.py``` for streamlit app to display outputs on dashboard and Raw data ```(WASAC_COMPLAINT_DATA.CSV)``` and cleaned customer complaint dataset ```(Processed_complaint_data.csv) ```datasets used in the analysis, serving as the foundation for all subsequent steps.
It includes Python used for data exploration, cleaning, feature engineering, and computation of summary statistics and contains reusable Python scripts that handle data processing functions and KPI calculations to ensure consistency across the project as specified on the first line. The app hosts the Streamlit application code responsible for building the interactive dashboard and visualizations. The assets stores screenshots or figures used for documentation and demonstration purposes. Finally, the README.md file provides an overview of the project, explains how the repository is structured, and gives instructions on how to run the analysis and dashboard.

# How to Run the Project (Local Setup)

1. Clone the GitHub repository to your local machine using git clone <repository_link>.

2. Navigate to the project directory and install the requirements

3. Open the main folder (FINAL-PROJECT-DSCBI) and ensure the cleaned dataset is available in the data (```"Cd NEW_ENV", "cd Scripts_And_Data" to enter in working environment, and "Python Data_P.py"```to process the cleaned data) in terminal 

4. Run the Streamlit application by executing streamlit run app/app.py from the project root directory (```"Streamlit run Dashboard.py"```) in terminal to run the app.

5. Open the provided local URL in your web browser to interact with the dashboard and explore the complaint analytics.

# AUTHOR: IRADUKUNDA Elisa 
Data Analyst, WASAC Utility
          
