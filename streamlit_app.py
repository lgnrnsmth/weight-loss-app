import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize a session state for storing data
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date', 'Weight'])

st.title("Weight Tracker")

# Input fields for weight and date
weight = st.number_input("Enter your weight (in pounds):", min_value=0.0, format="%.2f")
date = st.date_input("Select the date:")

# Add button to store the input data
if st.button("Add Entry"):
    new_entry = {'Date': date, 'Weight': weight}
    st.session_state['data'] = st.session_state['data'].append(new_entry, ignore_index=True)
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

# Plot the weight data
if not st.session_state['data'].empty:
    fig, ax = plt.subplots()
    ax.plot(st.session_state['data']['Date'], st.session_state['data']['Weight'], marker='o', linestyle='-')
    ax.set_title("Weight over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (lbs)")
    ax.set_ylim(st.session_state['data']['Weight'].min() - 10, st.session_state['data']['Weight'].max() + 10)
    plt.xticks(rotation=45)
    st.pyplot(fig)

