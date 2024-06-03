import streamlit as st
import pandas as pd

# Initialize a session state for storing data
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date', 'Weight'])

st.title("Weight Tracker")

# Input fields for weight and date
weight = st.number_input("Enter your weight (in pounds):", min_value=0.0, format="%.2f")
date = st.date_input("Select the date:")

# Add button to store the input data
if st.button("Add Entry"):
    new_entry = pd.DataFrame({'Date': [date], 'Weight': [weight]})
    st.session_state['data'] = pd.concat([st.session_state['data'], new_entry], ignore_index=True)
    st.session_state['data'] = st.session_state['data'].sort_values(by='Date').reset_index(drop=True)

# Function to calculate percentage change
def calculate_percentage_change(data):
    data['% Change'] = data['Weight'].pct_change() * 100
    data['% Change'] = data['% Change'].round(2)
    data['% Change'].fillna(0, inplace=True)
    return data

# Apply percentage change calculation
if not st.session_state['data'].empty:
    st.session_state['data'] = calculate_percentage_change(st.session_state['data'])

# Display the weight data in a table
st.write("### Weight Data")
st.dataframe(st.session_state['data'])

# Plot the weight data using Streamlit's line_chart
if not st.session_state['data'].empty:
    st.write("### Weight Over Time")
    st.line_chart(st.session_state['data'].set_index('Date')['Weight'])
