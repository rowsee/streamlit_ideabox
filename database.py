import sqlite3
import os
import json
import io
from datetime import datetime
from contextlib import contextmanager

DATABASE = "ideabox.db"
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                project_lead TEXT,
                region TEXT,
                bu_cl_site TEXT,
                project_type TEXT,
                problem_statements TEXT,
                benefits TEXT,
                is_implemented TEXT DEFAULT 'No',
                effective_date TEXT,
                drivers TEXT,
                impact_group TEXT,
                hours_saved INTEGER,
                capacity_file TEXT,
                planned_use TEXT,
                email_approval TEXT,
                submitted_by INTEGER NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Pending',
                votes INTEGER DEFAULT 0,
                FOREIGN KEY (submitted_by) REFERENCES users (id)
            )
        """)
        
        # Migration: Add project_lead column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE ideas ADD COLUMN project_lead TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (idea_id) REFERENCES ideas (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(idea_id, user_id)
            )
        """)
        conn.commit()

def create_user(username, email, full_name=""):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, full_name) VALUES (?, ?, ?)",
                (username, email, full_name)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            return cursor.fetchone()[0]

def get_user_by_email(email):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()

def save_uploaded_file(uploaded_file, prefix="file"):
    if uploaded_file is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}_{uploaded_file.name}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filepath
    return None

def add_idea(
    title, description, project_lead, region, bu_cl_site, project_type,
    problem_statements, benefits, is_implemented, effective_date,
    drivers, impact_group, hours_saved, capacity_file, planned_use,
    email_approval, submitted_by
):
    drivers_json = json.dumps(drivers) if drivers else None
    capacity_path = save_uploaded_file(capacity_file, "capacity") if capacity_file else None
    email_path = save_uploaded_file(email_approval, "approval") if email_approval else None
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO ideas (
                title, description, project_lead, region, bu_cl_site, project_type,
                problem_statements, benefits, is_implemented, effective_date,
                drivers, impact_group, hours_saved, capacity_file, planned_use,
                email_approval, submitted_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                title, description, project_lead, region, bu_cl_site, project_type,
                problem_statements, benefits, is_implemented, effective_date,
                drivers_json, impact_group, hours_saved, capacity_path, planned_use,
                email_path, submitted_by
            )
        )
        conn.commit()
        return cursor.lastrowid

def get_all_ideas():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.*, u.username, u.full_name, u.email
            FROM ideas i
            JOIN users u ON i.submitted_by = u.id
            ORDER BY i.submitted_at DESC
        """)
        return cursor.fetchall()

def get_user_ideas(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM ideas
            WHERE submitted_by = ?
            ORDER BY submitted_at DESC
        """, (user_id,))
        return cursor.fetchall()

def get_idea_by_id(idea_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.*, u.username, u.full_name, u.email
            FROM ideas i
            JOIN users u ON i.submitted_by = u.id
            WHERE i.id = ?
        """, (idea_id,))
        return cursor.fetchone()

def update_idea(
    idea_id, title, description, project_lead, bu_cl_site, project_type,
    problem_statements, benefits, is_implemented, effective_date,
    drivers, impact_group, hours_saved, capacity_file, planned_use,
    email_approval
):
    drivers_json = json.dumps(drivers) if drivers else None
    capacity_path = save_uploaded_file(capacity_file, "capacity") if capacity_file else None
    email_path = save_uploaded_file(email_approval, "approval") if email_approval else None
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        updates = [
            "title = ?", "description = ?", "project_lead = ?", "bu_cl_site = ?",
            "project_type = ?", "problem_statements = ?", "benefits = ?",
            "is_implemented = ?", "effective_date = ?", "drivers = ?",
            "impact_group = ?", "hours_saved = ?", "planned_use = ?"
        ]
        values = [
            title, description, project_lead, bu_cl_site, project_type,
            problem_statements, benefits, is_implemented, effective_date,
            drivers_json, impact_group, hours_saved, planned_use
        ]
        
        if capacity_path:
            updates.append("capacity_file = ?")
            values.append(capacity_path)
        if email_path:
            updates.append("email_approval = ?")
            values.append(email_path)
        
        values.append(idea_id)
        
        query = f"UPDATE ideas SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()

def delete_idea(idea_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT capacity_file, email_approval FROM ideas WHERE id = ?", (idea_id,))
        files = cursor.fetchone()
        if files:
            for filepath in [files["capacity_file"], files["email_approval"]]:
                if filepath and os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except:
                        pass
        
        cursor.execute("DELETE FROM votes WHERE idea_id = ?", (idea_id,))
        cursor.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
        conn.commit()

def vote_idea(idea_id, user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO votes (idea_id, user_id) VALUES (?, ?)",
            (idea_id, user_id)
        )
        if cursor.rowcount > 0:
            cursor.execute("UPDATE ideas SET votes = votes + 1 WHERE id = ?", (idea_id,))
        conn.commit()
        return cursor.rowcount > 0

def has_voted(idea_id, user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM votes WHERE idea_id = ? AND user_id = ?",
            (idea_id, user_id)
        )
        return cursor.fetchone() is not None

def get_stats():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM ideas")
        total_ideas = cursor.fetchone()[0]
        
        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute(
            "SELECT COUNT(*) FROM ideas WHERE strftime('%Y-%m', submitted_at) = ?",
            (current_month,)
        )
        this_month = cursor.fetchone()[0]
        
        return {"total": total_ideas, "this_month": this_month}

def get_category_counts():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT project_type, COUNT(*) as count FROM ideas GROUP BY project_type")
        return dict(cursor.fetchall())

def ideas_to_dataframe(ideas):
    import pandas as pd
    
    data = []
    for idea in ideas:
        drivers_list = []
        if idea["drivers"]:
            try:
                drivers_list = json.loads(idea["drivers"])
            except:
                drivers_list = [idea["drivers"]] if idea["drivers"] else []
        
        data.append({
            "ID": idea["id"],
            "Project Title": idea["title"],
            "Project Description": idea["description"],
            "Project Lead": idea["project_lead"],
            "Submitter": idea["full_name"] or idea["username"],
            "Region": idea["region"],
            "BU/CL Site": idea["bu_cl_site"],
            "Project Type": idea["project_type"],
            "Problem Statements": idea["problem_statements"],
            "Expected Benefits": idea["benefits"],
            "Is Implemented": idea["is_implemented"],
            "Effective Date": idea["effective_date"],
            "Drivers": ", ".join(drivers_list) if drivers_list else "",
            "Impact Group": idea["impact_group"],
            "Hours Saved Annually": idea["hours_saved"],
            "Planned Use": idea["planned_use"],
            "Status": idea["status"],
            "Votes": idea["votes"],
            "Submitted Date": idea["submitted_at"]
        })
    
    return pd.DataFrame(data)
