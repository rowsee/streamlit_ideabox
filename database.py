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
                proposed_change TEXT,
                project_lead TEXT,
                region TEXT,
                bu_cl_site TEXT,
                problem_statements TEXT,
                benefits TEXT,
                is_implemented TEXT DEFAULT 'No',
                solution_implemented TEXT,
                date_implemented TEXT,
                effective_date TEXT,
                drivers TEXT,
                impact_group TEXT,
                hours_saved INTEGER,
                capacity_file TEXT,
                planned_use TEXT,
                email_approval TEXT,
                site_leader TEXT,
                teoa_leader TEXT,
                submitted_by INTEGER NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Pending',
                votes INTEGER DEFAULT 0,
                FOREIGN KEY (submitted_by) REFERENCES users (id)
            )
        """)

        # Migration: Add all potentially missing columns
        columns_to_add = [
            ("proposed_change", "TEXT"),
            ("project_lead", "TEXT"),
            ("region", "TEXT"),
            ("bu_cl_site", "TEXT"),
            ("problem_statements", "TEXT"),
            ("benefits", "TEXT"),
            ("is_implemented", "TEXT DEFAULT 'No'"),
            ("solution_implemented", "TEXT"),
            ("date_implemented", "TEXT"),
            ("effective_date", "TEXT"),
            ("drivers", "TEXT"),
            ("impact_group", "TEXT"),
            ("hours_saved", "INTEGER"),
            ("capacity_file", "TEXT"),
            ("planned_use", "TEXT"),
            ("email_approval", "TEXT"),
            ("site_leader", "TEXT"),
            ("teoa_leader", "TEXT"),
            ("status", "TEXT DEFAULT 'Pending'"),
            ("votes", "INTEGER DEFAULT 0"),
        ]

        for column_name, column_type in columns_to_add:
            try:
                cursor.execute(
                    f"ALTER TABLE ideas ADD COLUMN {column_name} {column_type}"
                )
            except sqlite3.OperationalError:
                pass  # Column already exists

        # Create audit log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS idea_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id INTEGER NOT NULL,
                field_name TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (idea_id) REFERENCES ideas (id)
            )
        """)

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
                (username, email, full_name),
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
    title,
    proposed_change,
    project_lead,
    region,
    bu_cl_site,
    problem_statements,
    benefits,
    is_implemented,
    effective_date,
    drivers,
    impact_group,
    hours_saved,
    capacity_file,
    planned_use,
    email_approval,
    submitted_by,
    site_leader="",
    teoa_leader="",
    solution_implemented=None,
    date_implemented=None,
):
    drivers_json = json.dumps(drivers) if drivers else None
    capacity_path = (
        save_uploaded_file(capacity_file, "capacity") if capacity_file else None
    )
    email_path = (
        save_uploaded_file(email_approval, "approval") if email_approval else None
    )

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO ideas (
                title, proposed_change, project_lead, region, bu_cl_site,
                problem_statements, benefits, is_implemented, effective_date,
                drivers, impact_group, hours_saved, capacity_file, planned_use,
                email_approval, submitted_by, site_leader, teoa_leader,
                solution_implemented, date_implemented
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                title,
                proposed_change,
                project_lead,
                region,
                bu_cl_site,
                problem_statements,
                benefits,
                is_implemented,
                effective_date,
                drivers_json,
                impact_group,
                hours_saved,
                capacity_path,
                planned_use,
                email_path,
                submitted_by,
                site_leader,
                teoa_leader,
                solution_implemented,
                date_implemented,
            ),
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
        cursor.execute(
            """
            SELECT i.*, u.username, u.full_name, u.email
            FROM ideas i
            JOIN users u ON i.submitted_by = u.id
            WHERE i.submitted_by = ?
            ORDER BY i.submitted_at DESC
        """,
            (user_id,),
        )
        return cursor.fetchall()


def get_idea_by_id(idea_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT i.*, u.username, u.full_name, u.email
            FROM ideas i
            JOIN users u ON i.submitted_by = u.id
            WHERE i.id = ?
        """,
            (idea_id,),
        )
        return cursor.fetchone()


def update_idea(
    idea_id,
    title,
    proposed_change,
    project_lead,
    bu_cl_site,
    problem_statements,
    benefits,
    is_implemented,
    effective_date,
    drivers,
    impact_group,
    hours_saved,
    capacity_file,
    planned_use,
    email_approval,
):
    drivers_json = json.dumps(drivers) if drivers else None
    capacity_path = (
        save_uploaded_file(capacity_file, "capacity") if capacity_file else None
    )
    email_path = (
        save_uploaded_file(email_approval, "approval") if email_approval else None
    )

    with get_db_connection() as conn:
        cursor = conn.cursor()

        updates = [
            "title = ?",
            "proposed_change = ?",
            "project_lead = ?",
            "bu_cl_site = ?",
            "problem_statements = ?",
            "benefits = ?",
            "is_implemented = ?",
            "effective_date = ?",
            "drivers = ?",
            "impact_group = ?",
            "hours_saved = ?",
            "planned_use = ?",
        ]
        values = [
            title,
            proposed_change,
            project_lead,
            bu_cl_site,
            problem_statements,
            benefits,
            is_implemented,
            effective_date,
            drivers_json,
            impact_group,
            hours_saved,
            planned_use,
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

        cursor.execute(
            "SELECT capacity_file, email_approval FROM ideas WHERE id = ?", (idea_id,)
        )
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
            (idea_id, user_id),
        )
        if cursor.rowcount > 0:
            cursor.execute(
                "UPDATE ideas SET votes = votes + 1 WHERE id = ?", (idea_id,)
            )
        conn.commit()
        return cursor.rowcount > 0


def has_voted(idea_id, user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM votes WHERE idea_id = ? AND user_id = ?", (idea_id, user_id)
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
            (current_month,),
        )
        this_month = cursor.fetchone()[0]

        current_year = datetime.now().year
        cursor.execute(
            "SELECT COUNT(*) FROM ideas WHERE strftime('%Y', submitted_at) = ?",
            (str(current_year),),
        )
        this_year = cursor.fetchone()[0]

        current_week_start = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT COUNT(*) FROM ideas WHERE date(submitted_at) >= date('now', '-7 days')"
        )
        this_week = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ideas WHERE status = 'Pending'")
        pending = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ideas WHERE is_implemented = 'Yes'")
        implemented = cursor.fetchone()[0]

        return {
            "total": total_ideas,
            "this_month": this_month,
            "this_year": this_year,
            "this_week": this_week,
            "pending": pending,
            "implemented": implemented,
        }


def get_top_contributors_per_bu():
    """Get the top BU with the most ideas submitted this month"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute(
            """SELECT bu_cl_site, COUNT(*) as count 
               FROM ideas 
               WHERE strftime('%Y-%m', submitted_at) = ? 
               AND bu_cl_site IS NOT NULL 
               AND bu_cl_site != ''
               GROUP BY bu_cl_site 
               ORDER BY count DESC 
               LIMIT 1""",
            (current_month,),
        )
        result = cursor.fetchone()

        if result:
            return {"bu_cl_site": result[0], "count": result[1]}
        return None


def get_top_contributor():
    """Get the top contributor (user) with the most ideas submitted this month"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute(
            """SELECT u.full_name, u.username, COUNT(*) as idea_count
               FROM ideas i
               JOIN users u ON i.submitted_by = u.id
               WHERE strftime('%Y-%m', i.submitted_at) = ?
               GROUP BY i.submitted_by
               ORDER BY idea_count DESC
               LIMIT 1""",
            (current_month,),
        )
        result = cursor.fetchone()

        if result:
            full_name = result[0] if result[0] else result[1]
            return {"name": full_name, "count": result[2]}
        return None


def ideas_to_dataframe(ideas):
    import pandas as pd

    data = []
    for idea in ideas:
        if not idea or not isinstance(idea, dict):
            continue

        drivers_list = []
        drivers = idea.get("drivers")
        if drivers:
            try:
                drivers_list = json.loads(drivers)
            except:
                drivers_list = [drivers] if drivers else []

        data.append(
            {
                "ID": idea.get("id", ""),
                "Project Title": idea.get("title", ""),
                "Proposed Change": idea.get("proposed_change", "") or "",
                "Project Lead": idea.get("project_lead", "") or "",
                "Submitter": idea.get("full_name")
                or (idea.get("username") if idea.get("username") else "Unknown"),
                "Submitter Email": idea.get("email", "") or "",
                "Region": idea.get("region", "") or "",
                "BU/CL Site": idea.get("bu_cl_site", "") or "",
                "Problem Statements": idea.get("problem_statements", "") or "",
                "Expected Benefits": idea.get("benefits", "") or "",
                "Is Implemented": idea.get("is_implemented", "") or "",
                "Solution Implemented": idea.get("solution_implemented", "") or "",
                "Date Implemented": idea.get("date_implemented", "") or "",
                "Effective Date": idea.get("effective_date", "") or "",
                "Drivers": ", ".join(drivers_list) if drivers_list else "",
                "Impact Group": idea.get("impact_group", "") or "",
                "Hours Saved Annually": idea.get("hours_saved", "") or "",
                "Planned Use": idea.get("planned_use", "") or "",
                "Site Leader": idea.get("site_leader", "") or "",
                "TEOA Functional Leader": idea.get("teoa_leader", "") or "",
                "Likes": idea.get("votes", 0),
                "Submitted Date": idea.get("submitted_at", "") or "",
            }
        )

    return pd.DataFrame(data)


def add_audit_log(idea_id, field_name, old_value, new_value):
    """Add an audit log entry for a field change"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO idea_audit_log (idea_id, field_name, old_value, new_value) VALUES (?, ?, ?, ?)""",
            (idea_id, field_name, old_value, new_value),
        )
        conn.commit()


def get_audit_log(idea_id):
    """Get all audit log entries for an idea"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM idea_audit_log WHERE idea_id = ? ORDER BY changed_at DESC""",
            (idea_id,),
        )
        return cursor.fetchall()


def log_idea_changes(idea_id, old_idea, new_data):
    """Compare old and new idea data and log all changes"""
    tracked_fields = [
        "title",
        "proposed_change",
        "project_lead",
        "bu_cl_site",
        "problem_statements",
        "benefits",
        "is_implemented",
        "effective_date",
        "drivers",
        "impact_group",
        "hours_saved",
        "planned_use",
    ]

    for field in tracked_fields:
        old_value = old_idea[field] if field in old_idea else ""
        new_value = new_data.get(field, "")

        if old_value != new_value:
            old_str = str(old_value) if old_value else ""
            new_str = str(new_value) if new_value else ""
            add_audit_log(idea_id, field, old_str, new_str)
