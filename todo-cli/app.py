import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import pyrebase







# Database setup
conn = sqlite3.connect("tasks.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    priority TEXT,
    deadline TEXT,
    completed INTEGER DEFAULT 0
)
""")
conn.commit()

# Function to get tasks
def get_tasks(priority_filter="All", sort_by_deadline=False):
    query = "SELECT * FROM tasks"
    params = []
    if priority_filter != "All":
        query += " WHERE priority = ?"
        params.append(priority_filter)
    if sort_by_deadline:
        query += " ORDER BY deadline ASC"
    c.execute(query, params)
    return c.fetchall()

# Function to add task
def add_task(task, priority, deadline):
    c.execute("INSERT INTO tasks (task, priority, deadline, completed) VALUES (?, ?, ?, 0)",
              (task, priority, deadline))
    conn.commit()
    
    # Clear input fields after adding a task
   # Clear all session state values to reset inputs safely
    st.session_state.clear()
    st.rerun()
   

# Function to mark task as complete
def complete_task(task_id):
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    st.rerun()

# Function to delete task
def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    st.rerun()

# Function to determine deadline status
def get_deadline_status(deadline):
    if not deadline:
        return "No Deadline", "gray"
    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        today = datetime.today()
        if deadline_date < today:
            return "Past Deadline", "red"
        elif deadline_date - today < timedelta(days=1):
            return "Deadline Soon", "orange"
        return "Sufficient Time", "green"
    except ValueError:
        return "Invalid Date", "gray"

# UI
st.set_page_config(layout="wide", page_title="To-Do List")
st.title("🌟 𝐓𝐚𝐬𝐤𝐓𝐨𝐃𝐨 – 𝒮𝒾𝓂𝓅𝓁𝑒 & 𝒞𝓁𝑒𝒶𝓇 𝒯𝒶𝓈𝓀 𝒯𝓇𝒶𝒸𝓀𝑒𝓇 ✅📅")

# Sidebar
st.sidebar.header("📋 Your Tasks")
priority_filter = st.sidebar.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
sort_by_deadline = st.sidebar.checkbox("Sort by Deadline")

## Show tasks in the sidebar
tasks = get_tasks(priority_filter, sort_by_deadline)
for task in tasks:
    task_id, task_text, priority, deadline, completed = task
    with st.sidebar.expander(f"📝 {task_text} ({priority})", expanded=True):

        # Determine deadline status (color-coded)
        status_text, status_color = get_deadline_status(deadline)

        # Task Status Label (Completed ✅ or Remaining ⏳)
        if completed:
            status_label = "✅ Completed"
            label_color = "green"
        else:
            status_label = "⏳ Remaining"
            label_color = "orange"

        # Display status & deadline info
        st.markdown(f"<p style='color:{label_color}; font-weight:bold;'>{status_label}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{status_color};'>{status_text}</p>", unsafe_allow_html=True)

        # Task Actions
        col1, col2 = st.columns([1, 1])
        with col1:
            if not completed and st.button("✔ Mark as Completed", key=f"complete-{task_id}"):
                complete_task(task_id)
        with col2:
            if st.button("🗑 Delete", key=f"delete-{task_id}"):
                delete_task(task_id)

# Task input
st.subheader("➕ Add New Task")

# Initialize session state for input fields
if "task_name" not in st.session_state:
    st.session_state["task_name"] = ""
if "deadline" not in st.session_state:
    st.session_state["deadline"] = ""
if "priority" not in st.session_state:
    st.session_state["priority"] = "Medium"

task_text = st.text_input("Task Name", value=st.session_state["task_name"], key="task_name")
priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(st.session_state["priority"]), key="priority")
deadline = st.date_input("Deadline (Optional)", value=None, key="deadline")

if st.button("Add Task"):
    formatted_deadline = deadline.strftime("%Y-%m-%d") if deadline else ""  # Convert date to string
    add_task(task_text, priority, formatted_deadline)

# if st.button("Add Task"):
#     if task_text.strip():
#         add_task(task_text, priority, deadline)
else:
        st.warning("Please enter a task name.")

## Show all tasks
st.subheader("📂 All Tasks")
for task in tasks:
    task_id, task_text, priority, deadline, completed = task
    status_text, status_color = get_deadline_status(deadline)

    # Task Status Label (Completed ✅ or Remaining ⏳)
    if completed:
        status_label = "✅ Completed"
        label_color = "green"
    else:
        status_label = "⏳ Remaining"
        label_color = "orange"

    with st.container():
        # Task Title
        st.markdown(f"### 📝 {task_text} ({priority})")

        # Status Labels & Deadline
        st.markdown(f"<p style='color:{label_color}; font-weight:bold;'>{status_label}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{status_color};'>{status_text}</p>", unsafe_allow_html=True)

        # Task Actions
        col1, col2 = st.columns([1, 1])
        with col1:
            if not completed:
                if st.button("✔ Mark as Completed", key=f"main-complete-{task_id}"):
                    complete_task(task_id)
        with col2:
            if st.button("🗑 Delete", key=f"main-delete-{task_id}"):
                delete_task(task_id)


# Firebase Configuration (Replace with your own details)
firebaseConfig = {
    "apiKey": "AIzaSyC6gY1pZ_ZXSyXrijT6g-VgOBC4dvz-0Zk",
    "authDomain": "todo-app-5c4da.firebaseapp.com",
    "databaseURL": "",  # Add your Firebase Realtime Database URL here if used
    "projectId": "todo-app-5c4da",
    "storageBucket": "todo-app-5c4da.appspot.com",  # Correct format
    "messagingSenderId": "638069257923",
    "appId": "1:638069257923:web:3466a22cc420e562025476"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Sidebar Login/Signup UI
st.sidebar.markdown("## 🔐 User Authentication")

if "user" not in st.session_state:
    with st.sidebar.expander("👤 Login / Sign Up", expanded=True):
        option = st.radio("Select:", ["Login", "Sign Up"], horizontal=True)

        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

        col1, col2 = st.columns(2)
        with col1:
            if option == "Login":
                if st.button("➡️ Login"):
                    try:
                        user = auth.sign_in_with_email_and_password(email, password)
                        st.session_state["user"] = user
                        st.success("✅ Login Successful!")
                        st.ererun()
                    except:
                        st.error("❌ Invalid Credentials!")

            else:  # Sign Up
                if st.button("🆕 Sign Up"):
                    try:
                        auth.create_user_with_email_and_password(email, password)
                        st.success("🎉 Account Created! Please log in.")
                    except Exception as e:
                        st.error(f"❌ Signup Failed! {str(e)}")

else:
    # User Logged In UI
    st.sidebar.success(f"👋 Welcome, **{st.session_state['user']['email']}**")
    if st.sidebar.button("🚪 Logout", key="logout"):
        del st.session_state["user"]
        st.rerun()

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")

if dark_mode:
    dark_theme = """
    <style>
        /* Full Page Dark Background */
        body, .stApp {
            background-color: #121212 !important;
            color: #EAEAEA !important;
        }

        /* Sidebar Dark Mode */
        .st-emotion-cache-1d391kg, .st-emotion-cache-1lcbmhc {
            background-color: #181818 !important;
            color: #EAEAEA !important;
        }

        /* Sidebar Title & Text */
        .st-emotion-cache-10trblm, .st-emotion-cache-16txtl3, .st-emotion-cache-13ln8v1 {
            color: #EAEAEA !important;
        }

        /* Inputs & Dropdowns */
        .stTextInput>div>div>input, 
        .stSelectbox>div>div {
            background-color: #333333 !important;
            color: #EAEAEA !important;
            border-radius: 5px !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #444 !important;
            color: white !important;
            border-radius: 5px !important;
            border: 1px solid white !important;
        }

        /* Expander (Task Lists in Sidebar) */
        .st-expander {
            background-color: #222 !important;
            color: #EAEAEA !important;
        }

        /* Headings Fix */
        h1, h2, h3, h4, h5, h6 {
            color: #FFD700 !important; /* Gold Color for Better Visibility */
        }

        /* Radio Buttons & Checkboxes */
        .stRadio>div>label, .stCheckbox>label {
            color: #EAEAEA !important;
        }
    </style>
    """
    st.markdown(dark_theme, unsafe_allow_html=True)
