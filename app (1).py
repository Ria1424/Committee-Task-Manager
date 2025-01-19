import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for task data
if "tasks" not in st.session_state:
    st.session_state["tasks"] = pd.DataFrame(columns=["Task ID", "Task Name", "Assigned To", "Deadline", "Status", "Submission Date", "Submitted File"])

# Helper function to add a new task
def add_task(task_name, assigned_to, deadline):
    task_id = len(st.session_state["tasks"]) + 1
    new_task = {
        "Task ID": task_id,
        "Task Name": task_name,
        "Assigned To": assigned_to,
        "Deadline": deadline,
        "Status": "Pending",
        "Submission Date": None,
        "Submitted File": None,
    }
    st.session_state["tasks"] = pd.concat([st.session_state["tasks"], pd.DataFrame([new_task])], ignore_index=True)

# Helper function to update task status and details
def update_task_status(task_id, status, submission_date=None, file_name=None):
    task_index = st.session_state["tasks"][st.session_state["tasks"]["Task ID"] == task_id].index
    if not task_index.empty:
        st.session_state["tasks"].loc[task_index[0], "Status"] = status
        if submission_date:
            st.session_state["tasks"].loc[task_index[0], "Submission Date"] = submission_date
        if file_name:
            st.session_state["tasks"].loc[task_index[0], "Submitted File"] = file_name

# Streamlit UI
st.title("Committee Task Management System")

# Sidebar menu
menu = st.sidebar.radio("Navigation", ["Assign Task", "View Tasks", "Submit Work"])

# Assign Task Page
if menu == "Assign Task":
    st.header("Assign a New Task")
    task_name = st.text_input("Task Name")
    assigned_to = st.text_input("Assign To (e.g., Member Name)")
    deadline = st.date_input("Deadline")
    if st.button("Assign Task"):
        if task_name and assigned_to:
            add_task(task_name, assigned_to, deadline)
            st.success(f"Task '{task_name}' assigned to {assigned_to}!")
        else:
            st.error("Please fill in all fields.")

# View Tasks Page
elif menu == "View Tasks":
    st.header("View and Manage Tasks")
    tasks = st.session_state["tasks"]
    if not tasks.empty:
        st.dataframe(tasks)
        task_id = st.number_input("Enter Task ID to Update Status:", min_value=1, max_value=len(tasks), step=1)
        new_status = st.selectbox("Update Status To:", ["Pending", "In Progress", "Completed"])
        if st.button("Update Status"):
            update_task_status(task_id, new_status)
            st.success("Task status updated successfully!")
    else:
        st.info("No tasks available.")

# Submit Work Page
elif menu == "Submit Work":
    st.header("Submit Task Work")
    tasks = st.session_state["tasks"]
    if not tasks.empty:
        assigned_to = st.text_input("Enter Your Name:")
        if assigned_to:
            user_tasks = tasks[(tasks["Assigned To"] == assigned_to) & (tasks["Status"] != "Completed")]
            if not user_tasks.empty:
                task_id = st.selectbox("Select Task to Submit:", user_tasks["Task ID"])
                uploaded_file = st.file_uploader("Upload Submission:")
                if st.button("Submit Task"):
                    submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    update_task_status(task_id, "Completed", submission_date, uploaded_file.name if uploaded_file else None)
                    st.success("Task submitted successfully!")
            else:
                st.info("No tasks assigned to you or no pending tasks.")
        else:
            st.info("Please enter your name to see tasks.")
    else:
        st.info("No tasks available.")

