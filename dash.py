import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            color: #4CAF50;
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }
        .header {
            color: #2c3e50;
            font-size: 36px;
            margin-top: 40px;
            font-weight: bold;
        }
        .metric-value {
            color: #2980b9;
            font-size: 36px;
            font-weight: bold;
        }
        .data-table {
            font-size: 16px;
            color: #34495e;
            border-collapse: collapse;
        }
        .data-table th, .data-table td {
            padding: 8px 16px;
            border: 1px solid #ecf0f1;
        }
        .data-table th {
            background-color: #f4f6f7;
            text-align: left;
        }
        body {
            background-color: #f7f7f7;
        }
    </style>
""", unsafe_allow_html=True)

# Generate sample data for waste collection
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="W")
data = {
    "Date": dates,
    "Total Waste Collected (kg)": np.random.randint(500, 1500, len(dates)),
    "Recyclable Waste (kg)": np.random.randint(200, 800, len(dates)),
    "Organic Waste (kg)": np.random.randint(100, 500, len(dates)),
    "Non-Recyclable Waste (kg)": np.random.randint(100, 400, len(dates)),
}
df = pd.DataFrame(data)

# Calculate additional metrics
df["Recycling Rate (%)"] = (df["Recyclable Waste (kg)"] / df["Total Waste Collected (kg)"]) * 100
total_collected = df["Total Waste Collected (kg)"].sum()
total_recyclable = df["Recyclable Waste (kg)"].sum()
average_recycling_rate = df["Recycling Rate (%)"].mean()

# Set up the dashboard title
st.markdown('<div class="title">Waste Management Dashboard</div>', unsafe_allow_html=True)
st.write("""
Welcome to the Waste Management Dashboard. 
Here, you can view key insights into waste collection, recycling efforts, and waste distribution.
""")

# Create a dropdown menu for navigation
option = st.selectbox(
    "Choose a Section:",
    ("Key Metrics", "Waste Collection Trends", "Waste Types Breakdown", "Recycling Rate Trends", "Raw Data Table")
)

# Display content based on dropdown selection
if option == "Key Metrics":
    col1, col2 = st.columns(2)
    with col1:
        st.header("Total Waste Collected")
        st.metric(label="Total Waste Collected (kg)", value=f"{total_collected:,}")
    
    with col2:
        st.header("Recycling Rate")
        st.metric(label="Average Recycling Rate (%)", value=f"{average_recycling_rate:.2f}%")

elif option == "Waste Collection Trends":
    st.header("Waste Collection Trends")
    line_chart = alt.Chart(df).mark_line(color="#3498db", size=4).encode(
        x="Date:T",
        y="Total Waste Collected (kg):Q",
        tooltip=["Date", "Total Waste Collected (kg)"]
    ).properties(
        title="Weekly Waste Collection Over Time"
    ).configure_title(
        fontSize=20, font="Arial", anchor="middle", color="#2c3e50"
    )

    st.altair_chart(line_chart, use_container_width=True)

elif option == "Waste Types Breakdown":
    st.header("Waste Types Breakdown")
    waste_breakdown = df[["Recyclable Waste (kg)", "Organic Waste (kg)", "Non-Recyclable Waste (kg)"]].sum()
    waste_breakdown_df = pd.DataFrame({
        "Waste Type": waste_breakdown.index,
        "Amount (kg)": waste_breakdown.values
    })
    pie_chart = alt.Chart(waste_breakdown_df).mark_arc().encode(
        theta=alt.Theta(field="Amount (kg)", type="quantitative"),
        color=alt.Color(field="Waste Type", type="nominal"),
        tooltip=["Waste Type", "Amount (kg)"]
    ).properties(title="Waste Types Distribution")

    st.altair_chart(pie_chart, use_container_width=True)

elif option == "Recycling Rate Trends":
    st.header("Recycling Rate Trends")
    recycling_rate_chart = alt.Chart(df).mark_line(color="green", size=4).encode(
        x="Date:T",
        y="Recycling Rate (%):Q",
        tooltip=["Date", "Recycling Rate (%)"]
    ).properties(title="Recycling Rate Over Time")

    st.altair_chart(recycling_rate_chart, use_container_width=True)

elif option == "Raw Data Table":
    st.header("Raw Data Table")
    styled_df = df.style.set_table_styles(
        [{'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white')]}, 
         {'selector': 'tbody td', 'props': [('padding', '8px'), ('border', '1px solid #ddd')]},
         {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', '#f9f9f9')]},
         {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#fff')]}]
    )
    st.dataframe(styled_df)

# Add a sidebar for filtering by date range
st.sidebar.header("Filters")
min_date, max_date = st.sidebar.date_input(
    "Select date range:",
    [df["Date"].min(), df["Date"].max()]
)
filtered_df = df[(df["Date"] >= pd.to_datetime(min_date)) & (df["Date"] <= pd.to_datetime(max_date))]

st.sidebar.write(f"Filtered Data (from {min_date} to {max_date}):")
st.sidebar.dataframe(filtered_df)

# Conclusion
st.sidebar.write("Thank you for exploring the Waste Management Dashboard!")
