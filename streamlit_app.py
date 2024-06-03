import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, timedelta

# Initialize a session state for storing data
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date', 'Weight'])
if 'goal_weight' not in st.session_state:
    st.session_state['goal_weight'] = None

st.title("Weight Tracker")

# Input fields for weight and date
weight = st.number_input("Enter your weight (in pounds):", min_value=0.0, format="%.2f")
date = st.date_input("Select the date:")

# Goal weight input
goal_weight = st.number_input("Set your goal weight (in pounds):", min_value=0.0, format="%.2f")

# Add button to store the input data
if st.button("Add Entry"):
    new_entry = pd.DataFrame({'Date': [date], 'Weight': [weight]})
    st.session_state['data'] = pd.concat([st.session_state['data'], new_entry], ignore_index=True)
    st.session_state['data'] = st.session_state['data'].sort_values(by='Date').reset_index(drop=True)
    st.session_state['goal_weight'] = goal_weight

# Function to calculate percentage change
def calculate_percentage_change(data):
    data['% Change'] = data['Weight'].pct_change() * 100
    data['% Change'] = data['% Change'].round(2)
    data['% Change'].fillna(0, inplace=True)
    return data

# Function to calculate estimated goal date
def calculate_estimated_goal_date(data, goal_weight):
    if len(data) < 2:
        return None

    # Convert dates to ordinal for linear regression
    data['DateOrdinal'] = pd.to_datetime(data['Date']).map(datetime.toordinal)
    
    # Perform linear regression manually
    x = data['DateOrdinal'].values
    y = data['Weight'].values
    slope, intercept = np.polyfit(x, y, 1)

    if slope >= 0:
        return None  # Weight is not decreasing, cannot estimate goal date

    # Calculate the date when the weight will reach the goal
    goal_date_ordinal = (goal_weight - intercept) / slope
    goal_date = datetime.fromordinal(int(goal_date_ordinal))
    return goal_date, slope, intercept

# Apply percentage change calculation
if not st.session_state['data'].empty:
    st.session_state['data'] = calculate_percentage_change(st.session_state['data'])

# Display the weight data in a table
st.write("### Weight Data")
st.dataframe(st.session_state['data'])

# Display estimated goal date and prepare data for the extended line
estimated_goal_date = None
if st.session_state['goal_weight'] and not st.session_state['data'].empty:
    result = calculate_estimated_goal_date(st.session_state['data'], st.session_state['goal_weight'])
    if result:
        estimated_goal_date, slope, intercept = result
        st.write(f"### Estimated Goal Date: {estimated_goal_date.strftime('%b %d, %Y')}")
    else:
        st.write("### Estimated Goal Date: Not enough data to estimate or weight is not decreasing")

# Plot the weight data using Altair
if not st.session_state['data'].empty:
    st.write("### Weight Over Time")
    
    # Calculate y-axis limits
    min_weight = st.session_state['data']['Weight'].min() - 10
    max_weight = st.session_state['data']['Weight'].max() + 10

    # Original data chart
    base_chart = alt.Chart(st.session_state['data']).mark_line(point=alt.OverlayMarkDef(color='black')).encode(
        x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%b %d')),
        y=alt.Y('Weight:Q', title='Weight (lbs)', scale=alt.Scale(domain=[min_weight, max_weight])),
        tooltip=['Date:T', 'Weight:Q']
    )
    
    # Extended line chart to the goal weight
    if estimated_goal_date:
        extended_data = pd.DataFrame({
            'Date': [st.session_state['data']['Date'].iloc[-1], estimated_goal_date],
            'Weight': [st.session_state['data']['Weight'].iloc[-1], st.session_state['goal_weight']]
        })
        
        extended_chart = alt.Chart(extended_data).mark_line(strokeDash=[5, 5], color='black').encode(
            x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%b %d')),
            y=alt.Y('Weight:Q', title='Weight (lbs)', scale=alt.Scale(domain=[min_weight, max_weight]))
        )
        
        chart = base_chart + extended_chart
    else:
        chart = base_chart

    st.altair_chart(chart, use_container_width=True)
