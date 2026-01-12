## PROJECT TITLE: ANALYSING THE IMPACT OF CUSTOMER COMPLAINT PATTERNS ON OPERATIONAL EFFICIENCY

## OVERVIEW
This project analyzes customer complaint data at the Water and Sanitation Corporation (WASAC) to understand how complaint patterns relate to operational efficiency and service delivery. Using a structured data pipeline, summary statistics, and an interactive Streamlit dashboard, the project transforms raw complaint records into clear, actionable insights. The analysis focuses on complaint distribution, resolution performance, and geographic and organizational patterns, supporting evidence-based decision-making and improved monitoring of service quality across branches and districts.

# Description of the repository structure
The repository is organized to reflect the complete analytical workflow of the project, from data preparation to dashboard deployment. The data/ folder contains the raw and cleaned customer complaint datasets used in the analysis, serving as the foundation for all subsequent steps. The notebooks/ folder includes Python notebooks used for data exploration, cleaning, feature engineering, and computation of summary statistics. The src/ folder contains reusable Python scripts that handle data processing functions and KPI calculations to ensure consistency across the project. The app/ folder hosts the Streamlit application code responsible for building the interactive dashboard and visualizations. The assets/ folder stores screenshots or figures used for documentation and demonstration purposes. Finally, the README.md file provides an overview of the project, explains how the repository is structured, and gives instructions on how to run the analysis and dashboard.

The data processing scripts are located in the notebooks/ folder for exploratory analysis and in the src/ folder for reusable cleaning, transformation, and KPI calculation functions. Since this project focuses on descriptive analytics rather than predictive modeling, there is no separate model code; all analytical logic is embedded within the data processing scripts. The application code for the interactive dashboard is located in the app/ folder, which contains the Streamlit files responsible for layout, filtering, and visualization. Configuration files, such as environment settings or dependency lists, are located at the root level of the repository (e.g., requirements.txt). Supporting materials such as screenshots and figures used for reporting or demonstration are stored in the assets/ folder.

# How to Run the Project (Local Setup)

1. Clone the GitHub repository to your local machine using git clone <repository_link>.

2. Navigate to the project directory and install the required dependencies using pip install -r requirements.txt.

3. Ensure the cleaned dataset is available in the data/ folder.

4. Run the Streamlit application by executing streamlit run app/app.py from the project root directory.

5. Open the provided local URL in your web browser to interact with the dashboard and explore the complaint analytics.

# AUTHOR: IRADUKUNDA Elisa
          Data Analyst, WASAC Utility
          
