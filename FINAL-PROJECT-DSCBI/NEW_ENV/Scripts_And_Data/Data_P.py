import pandas as pd
import uuid
from datetime import datetime, timedelta

# --- Data Loading and Processing ---
FILE_NAME = "WASAC_Complaint_Data.csv"
PROCESSED_FILE_NAME = "processed_complaint_data.csv"
# The third row (index 2) contains the header row in the WASAC file
HEADER_ROW = 2 

def clean_and_process_data():
    """Reads CSV data, cleans it, calculates metrics, and saves it locally."""
    print(f"--- Step 1: Data Cleaning and Preprocessing ---")
    try:
        # Load data, skipping initial summary rows 
        df = pd.read_csv(FILE_NAME, header=HEADER_ROW)
        print(f"Data read successfully from {FILE_NAME}. Total rows: {len(df)}")
    except FileNotFoundError:
        print(f"ERROR: The file '{FILE_NAME}' not found.")
        return

    # 1. Standardize Column Names and Select Required Columns
    df = df.rename(columns={
        'Complaint-ID': 'Complaint_ID',
        'Type_of_Complaint': 'Type_of_Complaint_Received',
        'Time_Received': 'Time_Complaint_Received',
        'Time_Resolved': 'Time_Complaint_Resolved',
        'Assigned_To': 'Assigned_Staff',
        'District': 'Location_District',
        'Branch': 'Branch_Name',
        # Keep other relevant columns for potential future use or context
        'Sector': 'Location_Sector',
        'Province': 'Location_Province',
    })
    
    # Select all required columns based on the project scope
    df = df[[
        'Complaint_ID', 'Type_of_Complaint_Received', 'Time_Complaint_Received', 
        'Time_Complaint_Resolved', 'Assigned_Staff', 'Complaint_Status',
        'Location_District', 'Branch_Name'
    ]].copy()

    # 2. Convert Time columns to datetime objects
    date_cols = ['Time_Complaint_Received', 'Time_Complaint_Resolved']
    for col in date_cols:
        # Use errors='coerce' to turn bad dates into NaT
        df[col] = pd.to_datetime(df[col], format='mixed', errors='coerce', dayfirst=False)

    # 3. Calculate Operational Efficiency Metric: Resolution Time
    df['Resolution_Time'] = df['Time_Complaint_Resolved'] - df['Time_Complaint_Received']
    
    # Calculate difference only if Time_Resolved is after Time_Received
    df.loc[df['Resolution_Time'] < timedelta(0), 'Resolution_Time'] = pd.NaT
    
    # Convert Resolution Time to hours (float)
    df['Resolution_Time_Hours'] = df['Resolution_Time'].dt.total_seconds() / 3600

    # 4. Clean string columns (trim whitespace, handle NaNs)
    string_cols = [
        'Type_of_Complaint_Received', 'Location_District', 'Assigned_Staff', 
        'Complaint_Status', 'Branch_Name'
    ]
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip().replace('nan', 'Unknown')
        
    print(f"Data cleaning and metric calculation complete. Total records processed: {len(df)}")
    
    # 5. Save the processed data
    # Convert datetime objects to string before saving to avoid issues with different pandas versions
    for col in date_cols:
        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('')
        
    df.to_csv(PROCESSED_FILE_NAME, index=False)
    print(f"\n--- Processing Complete ---")
    print(f"Processed data saved to: {PROCESSED_FILE_NAME}. Please run 'dashboard_app.py' next.")

if __name__ == '__main__':
    clean_and_process_data()
    
# To run this utility, save it as data_processor.py and run: python data_processor.py
# (Requires: pip install pandas)