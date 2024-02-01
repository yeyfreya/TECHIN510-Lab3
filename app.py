import sqlite3
import psycopg2
import os
import datetime

import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp

# Connect to our database
DB_CONFIG = os.getenv("DB_TYPE")
if DB_CONFIG == 'PG':
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")
    con = psycopg2.connect(f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/todoapp?connect_timeout=10&application_name=todoapp")
else:
    con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
cur = con.cursor()


# Create the table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        is_done BOOLEAN,
        state TEXT,
        created_at TIMESTAMP,
        created_by TEXT,
        category TEXT
    )
    """
)

# Function to check and update the schema
def check_and_update_schema():
    cur.execute("PRAGMA table_info(tasks)")
    columns = {info[1] for info in cur.fetchall()}  # Use a set for efficient lookup

    missing_columns = {
        "state": "TEXT",
        "created_at": "TIMESTAMP",
        "created_by": "TEXT",
        "category": "TEXT",
        # Add any other new columns here
    }

    for column, data_type in missing_columns.items():
        if column not in columns:
            cur.execute(f"ALTER TABLE tasks ADD COLUMN {column} {data_type}")


# Call the updated function right after defining it
check_and_update_schema()


# Define our Form
class Task(BaseModel):
    name: str
    description: str
    is_done: bool = False
    state: str  # 'planned', 'in-progress', 'done'
    created_at: datetime.datetime = datetime.datetime.now()
    created_by: str
    category: str  # 'school', 'work', 'personal'

# Insert a new task into the database
def insert_task(name, description, is_done, state, created_by, category):
    created_at = datetime.datetime.now()
    cur.execute(
        """
        INSERT INTO tasks (name, description, is_done, state, created_at, created_by, category) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (name, description, is_done, state, created_at, created_by, category),
    )

# This function will be called when the check mark is toggled, this is called a callback function
def toggle_is_done(is_done, row):
    cur.execute(
        """
        UPDATE tasks SET is_done = ? WHERE id = ?
        """,
        (is_done, row[0]),
    )

# Function to delete a task
def delete_task(task_id):
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))


def main():
    st.title("Todo List App")
    st.write("Welcome to the Todo List App! Here you can add, delete and update tasks.")
    st.write("You can also mark tasks as done by clicking the checkbox.")
    st.write("You can also update the state and category of the task by selecting the new state and category from the dropdown.")   
    st.write("Created by: Freya Yu, UW ID: 2372732, Email: yeyfreya@uw.edu]")

    # Input form for new task
    with st.form(key='task_form'):
        name = st.text_input("Task Name")
        description = st.text_area("Task Description")
        is_done = st.checkbox("Is Done?")
        state = st.selectbox("State", options=["planned", "in-progress", "done"], index=0)
        created_by = st.text_input("Created By")
        category = st.selectbox("Category", options=["school", "work", "personal"], index=0)
        submit_button = st.form_submit_button(label="Add Task")

        if submit_button:
            insert_task(name, description, is_done, state, created_by, category)

    # Search and filter options
    search_query = st.text_input("Search tasks", "")
    filter_state = st.selectbox("Filter by State", ["", "planned", "in-progress", "done"], index=0)
    filter_category = st.selectbox("Filter by Category", ["", "school", "work", "personal"], index=0)
    
    # Constructing the query dynamically based on filters
    conditions = ["(name LIKE ? OR description LIKE ?)"]
    params = [f"%{search_query}%", f"%{search_query}%"]
    
    if filter_state:
        conditions.append("state = ?")
        params.append(filter_state)
        
    if filter_category:
        conditions.append("category = ?")
        params.append(filter_category)
        
    query = "SELECT * FROM tasks WHERE " + " AND ".join(conditions)

    
    data = cur.execute("SELECT * FROM tasks").fetchall()

    # Display tasks
    cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1])  # Adjust column widths as needed
    cols[0].write("Done?")
    cols[1].write("Name")
    cols[2].write("Detail")
    cols[3].write("State")
    cols[4].write("Category")
    cols[5].write("Created At")
    cols[6].write("Created By")
    cols[7].write("Delete")


    for row in data:
        cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1])  # Adjust column widths as needed
        
        is_done_key = f'done_{row[0]}'
        delete_key = f'delete_{row[0]}'
        
        cols[0].checkbox('', row[3], label_visibility='hidden', key=is_done_key, on_change=toggle_is_done, args=(not row[3], row))
        cols[1].write(row[1])
        cols[2].write(row[2])
        cols[3].write(row[4])  # State
        cols[4].write(row[7])  # Category
        cols[5].write(row[5].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row[5], datetime.datetime) else row[5])  # Created At
        cols[6].write(row[6])  # Created By
        if cols[7].button("Delete", key=delete_key):
            delete_task(row[0])
            st.experimental_rerun()

main()


