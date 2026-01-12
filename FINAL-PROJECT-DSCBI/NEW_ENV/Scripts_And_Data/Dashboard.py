import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta, datetime
import numpy as np
import io # Import the 'io' module for the StringIO buffer

# --- Configuration ---
PROCESSED_FILE_NAME = "processed_complaint_data.csv"
WASAC_WEBSITE_URL = "https://www.wasac.rw/" # <-- Added URL here

# --- Utility Function for Human-Readable Duration ---
def format_timedelta(td):
    """Formats a float representing hours into a human-readable string (e.g., 2d 5h 30m)."""
    if pd.isna(td):
        return "N/A"
    
    # Ensure td is treated as hours if it's a float, convert to seconds
    total_seconds = int(td * 3600)
    
    if total_seconds < 0: return "Invalid Time"

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    
    parts = []
    if days > 0: parts.append(f"{days}d")
    if hours > 0: parts.append(f"{hours}h")
    if minutes > 0 or not parts: parts.append(f"{minutes}m")
    
    return " ".join(parts)

# --- CSV Download Utility Function ---
def convert_df_to_csv(df):
    """Converts a pandas DataFrame to a CSV format string."""
    # Use to_csv with index=False to exclude the pandas index column
    return df.to_csv(index=False).encode('utf-8')

# --- Data Loading and Processing (Static) ---

@st.cache_data
def load_processed_data():
    """Loads and prepares the processed data from the local CSV."""
    try:
        df = pd.read_csv(PROCESSED_FILE_NAME)
        
        # Convert necessary columns back to datetime objects
        df['Time_Complaint_Received'] = pd.to_datetime(df['Time_Complaint_Received'], errors='coerce')
        
        # Calculate overall KPIs before filtering
        total_complaints = len(df)
        
        if not df['Time_Complaint_Received'].empty:
            start_date = df['Time_Complaint_Received'].min().normalize()
            end_date = df['Time_Complaint_Received'].max().normalize()
            total_days = (end_date - start_date).days + 1
            avg_daily_complaints = total_complaints / total_days if total_days > 0 else 0
        else:
            avg_daily_complaints = 0
            
        closed_complaints = df[df['Complaint_Status'] == 'Closed'].copy()
        avg_resolution_time_hours = closed_complaints['Resolution_Time_Hours'].mean()
        
        return df, avg_daily_complaints, avg_resolution_time_hours

    except FileNotFoundError:
        st.error(f"Error: Processed data file '{PROCESSED_FILE_NAME}' not found.")
        st.info("Please run the `data_processor.py` script first to generate the necessary file.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading or processing the data: {e}")
        st.stop()

# Load the initial data and global KPIs
df, global_avg_daily_complaints, global_avg_resolution_time = load_processed_data()

if df.empty:
    st.warning("No complaint data available to display.")
    st.stop()

# --- Dashboard Aesthetics Setup (Background Image and Header) ---

st.set_page_config(layout="wide", page_title="Customer Complaint Patterns And Operational Efficiency Dashboard", initial_sidebar_state="expanded")



# --- Sticky Header Implementation (Main Title & Subtitle) ---

header_container = st.container()

with header_container:
    st.markdown('<div class="fixed-header">', unsafe_allow_html=True)
    
    # Custom Header (Main Title)
    st.markdown(
        """
        <div class="header-container">
            <h1> Complaints Patterns & Efficiency Analysis</h1>
        """,
        unsafe_allow_html=True
    )
    

    # Subtitle
    st.markdown("Analyzing complaint patterns and measuring operational efficiency across branches and districts using static data.")
    # Separator line
    st.markdown("---")
    
    # Close the custom HTML class div
    st.markdown('</div>', unsafe_allow_html=True)


# --- Sidebar Filters ---
st.sidebar.header(" ")

# Logo
st.sidebar.image("logo1-White.png", use_container_width=True)

# Location Filter
district_options = sorted(df['Location_District'].unique())
selected_districts = st.sidebar.multiselect(
    "Select District(s):",
    options=district_options,
    default=district_options
)

# Branch Filter
branch_options = sorted(df['Branch_Name'].unique())
selected_branches = st.sidebar.multiselect(
    "Select WASAC Branch(es):",
    options=branch_options,
    default=branch_options
)

# Complaint Type Filter
type_options = sorted(df['Type_of_Complaint_Received'].unique())
selected_types = st.sidebar.multiselect(
    "Select Complaint Type(s):",
    options=type_options,
    default=type_options
)

# Date Range Filter
min_date_val = df['Time_Complaint_Received'].min()
max_date_val = df['Time_Complaint_Received'].max()
min_date = min_date_val.date() if pd.notna(min_date_val) else datetime(2023, 1, 1).date()
max_date = max_date_val.date() if pd.notna(max_date_val) else datetime.now().date()
    
try:
    # Ensure start_date and end_date are within the data range
    default_start = max(min_date, start_date) if 'start_date' in locals() else min_date
    default_end = min(max_date, end_date) if 'end_date' in locals() else max_date
    
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range:",
        value=[default_start, default_end],
        min_value=min_date,
        max_value=max_date
    )
except ValueError:
    st.sidebar.warning("Invalid date range in data, showing all dates.")
    start_date = min_date
    end_date = max_date


# Apply Filters
df_filtered = df[
    (df['Location_District'].isin(selected_districts)) &
    (df['Branch_Name'].isin(selected_branches)) &
    (df['Type_of_Complaint_Received'].isin(selected_types)) &
    (df['Time_Complaint_Received'].dt.date >= start_date) &
    (df['Time_Complaint_Received'].dt.date <= end_date)
]

# --- CSV Download Button ---
csv_data = convert_df_to_csv(df_filtered)

st.sidebar.markdown("---")
st.sidebar.subheader("Download Data")

if not df_filtered.empty:
    st.sidebar.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name='filtered_complaint_data.csv',
        mime='text/csv',
        help="Download the data currently displayed based on your filters."
    )
else:
    st.sidebar.info("No data to download with current filters.")

# **NEW: WASAC Website Link in Sidebar**
st.sidebar.markdown("---")
st.sidebar.subheader("Official Website")
st.sidebar.markdown(f"**[Visit WASAC Website ↗️]({WASAC_WEBSITE_URL})**", unsafe_allow_html=True)
# ------------------------------------

# Recalculate filtered KPIs
total_filtered_complaints = len(df_filtered)
filtered_closed = df_filtered[df_filtered['Complaint_Status'] == 'Closed'].copy()
filtered_avg_resolution_time = filtered_closed['Resolution_Time_Hours'].mean()
filtered_resolution_rate = (len(filtered_closed) / total_filtered_complaints) * 100 if total_filtered_complaints > 0 else 0

# Recalculate average daily for filtered data
if not df_filtered['Time_Complaint_Received'].empty:
    filtered_start_date = df_filtered['Time_Complaint_Received'].min().normalize()
    filtered_end_date = df_filtered['Time_Complaint_Received'].max().normalize()
    filtered_total_days = (filtered_end_date - filtered_start_date).days + 1
    filtered_avg_daily_complaints = total_filtered_complaints / filtered_total_days if filtered_total_days > 0 else 0
else:
    filtered_avg_daily_complaints = 0


# --- Key Performance Indicators (KPIs) ---
st.subheader("Operational Efficiency KPIs")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    label="Total Complaints", 
    value=f"{total_filtered_complaints:,}"
)

col2.metric(
    label="Avg. Daily Complaints",
    value=f"{filtered_avg_daily_complaints:.1f}",
    delta=f"Global Avg: {global_avg_daily_complaints:.1f}",
    delta_color="off"
)

col3.metric(
    label="Avg. Resolution Time",
    value=format_timedelta(filtered_avg_resolution_time),
    delta=f"Global Avg: {format_timedelta(global_avg_resolution_time)}",
    delta_color="off"
)

col4.metric(
    label="Resolution Rate", 
    value=f"{filtered_resolution_rate:.1f}%",
    delta=f"Closed: {len(filtered_closed):,}",
    delta_color="off"
)

col5.metric(
    label="Active/Open Complaints",
    value=len(df_filtered[df_filtered['Complaint_Status'].isin(['Pending', 'Open'])]),
    delta_color="inverse"
)

st.markdown("---")

# --- Charts for Pattern and Efficiency Analysis ---

# Row 1: Complaint Distribution and Branch Rate
st.subheader("Complaint Distribution and Branch Performance")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("##### 1. Complaint Distribution by Type")
    if not df_filtered.empty:
        # Complaint Distribution by Type 
        df_type_status = df_filtered.groupby('Type_of_Complaint_Received').size().reset_index(name='Count')
        fig_type = px.pie(
            df_type_status, 
            names='Type_of_Complaint_Received', 
            values='Count', 
            title='Percentage Distribution of Complaint Types',
            template='plotly_white',
            hole=.3,
        ).update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_type, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")


with chart_col2:
    st.markdown("##### 2. Complaint Rate by Branch (Volume)")
    if not df_filtered.empty:
        # Complaint Rate by Branch 
        df_branch_rate = df_filtered.groupby('Branch_Name').size().reset_index(name='Count')
        fig_branch = px.bar(
            df_branch_rate.sort_values('Count', ascending=False), 
            x='Branch_Name', 
            y='Count', 
            color='Count',
            color_continuous_scale=px.colors.sequential.Teal,
            title='Complaint Volume by Branch',
            template='plotly_white',
            labels={'Branch_Name': 'WASAC Branch', 'Count': 'Number of Complaints'}
        ).update_xaxes(categoryorder='total descending')
        st.plotly_chart(fig_branch, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

st.markdown("---")

# Row 2: District Rate (Top 5) and Staff Efficiency
st.subheader("Geographical Patterns and Efficiency")
efficiency_col1, efficiency_col2 = st.columns(2)

with efficiency_col1:
    st.markdown("##### 3. Top 5 Districts by Recurring Complaint Volume")
    if not df_filtered.empty:
        # Complaint Rate by District (Top 5 highlighted)
        df_district_rate = df_filtered.groupby('Location_District').size().reset_index(name='Count')
        df_district_top5 = df_district_rate.sort_values('Count', ascending=False).head(5)
        
        # Determine color for highlighting
        df_district_rate['Highlight'] = df_district_rate['Location_District'].apply(lambda x: 'Top 5' if x in df_district_top5['Location_District'].tolist() else 'Others')

        fig_district_rate = px.bar(
            df_district_rate.sort_values('Count', ascending=False),
            x='Location_District',
            y='Count',
            color='Highlight',
            color_discrete_map={'Top 5': '#DC3545', 'Others': "#36618D"}, # Red for Top 5, Gray for others
            title='Complaint Rate by District (Top 5 in Red)',
            template='plotly_white',
            labels={'Location_District': 'District', 'Count': 'Complaint Volume', 'Highlight': 'Ranking'},
        ).update_xaxes(categoryorder='total descending')
        st.plotly_chart(fig_district_rate, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with efficiency_col2:
    st.markdown("##### 4. Average Resolution Time by Staff")
    if not filtered_closed.empty:
        # Average Resolution Time by Staff (Efficiency Metric)
        df_staff_eff = filtered_closed.groupby('Assigned_Staff')['Resolution_Time_Hours'].mean().reset_index(name='Avg_Resolution_Time_Hours')
        df_staff_eff['Avg_Resolution_Time'] = df_staff_eff['Avg_Resolution_Time_Hours'].apply(format_timedelta)

        fig_staff_eff = px.bar(
            df_staff_eff.sort_values('Avg_Resolution_Time_Hours', ascending=False),
            x='Assigned_Staff',
            y='Avg_Resolution_Time_Hours',
            color='Avg_Resolution_Time_Hours',
            color_continuous_scale=px.colors.sequential.Viridis_r,
            title='Staff Efficiency Comparison (Lower is Better)',
            hover_data={'Avg_Resolution_Time_Hours': False, 'Avg_Resolution_Time': True},
            template='plotly_white',
            labels={'Avg_Resolution_Time_Hours': 'Avg. Resolution Time (Hours)', 'Assigned_Staff': 'Staff Member'}
        )
        st.plotly_chart(fig_staff_eff, use_container_width=True)
    else:
        st.info("No closed complaint data available for resolution time analysis.")