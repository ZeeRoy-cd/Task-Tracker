import streamlit as st
import pandas as pd
import os

# File to store tasks
FILE_PATH = "tasks.csv"

# Function to load the task data from a CSV file
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Date", "Task", "Status"])

# Function to save the task data to a CSV file
def save_data(data):
    data.to_csv(FILE_PATH, index=False)

# Initialize session state for data
if "data" not in st.session_state:
    st.session_state.data = load_data()

st.title("FutureZA Task Tracker")

# Input form for new tasks
with st.form(key='task_form'):
    date = st.date_input("Date")
    task = st.text_area("Task")
    status = st.selectbox("Status", ["Pending", "In-progress", "Done", "Other"])
    submit_button = st.form_submit_button(label='Add Task')

if submit_button:
    # Add new entry to the session state data
    new_row = {"Date": date, "Task": task, "Status": status}
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
    save_data(st.session_state.data)  # Save the updated data to the file
    st.success("Task added successfully!")

# Display the data
st.subheader("Current Tasks")
task_filter = st.selectbox("Filter tasks by status", ["All", "Pending", "In-progress", "Done", "Other"])

# Filter data based on the selected status
if task_filter != "All":
    filtered_data = st.session_state.data[st.session_state.data["Status"] == task_filter]
else:
    filtered_data = st.session_state.data

st.dataframe(filtered_data)

# Edit or delete tasks
if not filtered_data.empty:
    st.subheader("Manage Tasks")
    task_to_edit = st.selectbox("Select a task to edit", filtered_data.index)
    if st.button("Delete Task"):
        st.session_state.data.drop(index=task_to_edit, inplace=True)
        save_data(st.session_state.data)  # Save changes after deleting the task
        st.success("Task deleted successfully!")
    else:
        with st.form(key='edit_form'):
            new_date = st.date_input("Edit Date", value=filtered_data.loc[task_to_edit, "Date"])
            new_task = st.text_area("Edit Task", value=filtered_data.loc[task_to_edit, "Task"])
            new_status = st.selectbox("Edit Status", ["Pending", "In-progress", "Done", "Other"], 
                                      index=["Pending", "In-progress", "Done", "Other"].index(filtered_data.loc[task_to_edit, "Status"]))
            update_button = st.form_submit_button(label="Update Task")
        
        if update_button:
            st.session_state.data.at[task_to_edit, "Date"] = new_date
            st.session_state.data.at[task_to_edit, "Task"] = new_task
            st.session_state.data.at[task_to_edit, "Status"] = new_status
            save_data(st.session_state.data)  # Save the updated data
            st.success("Task updated successfully!")

# Task status visualization
st.subheader("Task Status Summary")
status_counts = st.session_state.data["Status"].value_counts()
st.bar_chart(status_counts)
