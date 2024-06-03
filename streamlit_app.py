import streamlit as st
import pandas as pd
import altair as alt

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

# Plot the weight data using Altair
if not st.session_state['data'].empty:
    st.write("### Weight Over Time")
    
    # Calculate y-axis limits
    min_weight = st.session_state['data']['Weight'].min() - 10
    max_weight = st.session_state['data']['Weight'].max() + 10

    # Create the Altair chart
    chart = alt.Chart(st.session_state['data']).mark_line(point=alt.OverlayMarkDef(color='black')).encode(
        x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%b %d')),
        y=alt.Y('Weight:Q', title='Weight (lbs)', scale=alt.Scale(domain=[min_weight, max_weight])),
        tooltip=['Date:T', 'Weight:Q']
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
