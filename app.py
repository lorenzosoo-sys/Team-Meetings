from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), "meetings.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submitter_name TEXT NOT NULL,
            meeting_name TEXT NOT NULL,
            meeting_date TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS meeting_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER NOT NULL,
            individual_name TEXT NOT NULL,
            capacity TEXT NOT NULL DEFAULT '',
            action_items TEXT NOT NULL DEFAULT '',
            blockers TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    meetings = conn.execute(
        "SELECT * FROM meetings ORDER BY created_at DESC"
    ).fetchall()

    entries_by_meeting = {}
    for meeting in meetings:
        entries = conn.execute(
            "SELECT * FROM meeting_entries WHERE meeting_id = ? ORDER BY id",
            (meeting["id"],),
        ).fetchall()
        entries_by_meeting[meeting["id"]] = entries

    conn.close()
    return render_template(
        "index.html", meetings=meetings, entries_by_meeting=entries_by_meeting
    )


@app.route("/submit", methods=["POST"])
def submit():
    submitter_name = request.form.get("submitter_name", "").strip()
    meeting_name = request.form.get("meeting_name", "").strip()
    meeting_date = request.form.get("meeting_date", "").strip()

    if not submitter_name or not meeting_name or not meeting_date:
        return redirect(url_for("index"))

    individual_names = request.form.getlist("individual_name[]")
    capacities = request.form.getlist("capacity[]")
    action_items_list = request.form.getlist("action_items[]")
    blockers_list = request.form.getlist("blockers[]")

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO meetings (submitter_name, meeting_name, meeting_date, created_at) VALUES (?, ?, ?, ?)",
        (submitter_name, meeting_name, meeting_date, datetime.now().isoformat()),
    )
    meeting_id = cursor.lastrowid

    for i in range(len(individual_names)):
        name = individual_names[i].strip()
        if not name:
            continue
        capacity = capacities[i].strip() if i < len(capacities) else ""
        action = action_items_list[i].strip() if i < len(action_items_list) else ""
        blocker = blockers_list[i].strip() if i < len(blockers_list) else ""

        conn.execute(
            "INSERT INTO meeting_entries (meeting_id, individual_name, capacity, action_items, blockers) VALUES (?, ?, ?, ?, ?)",
            (meeting_id, name, capacity, action, blocker),
        )

    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:meeting_id>", methods=["POST"])
def delete(meeting_id):
    conn = get_db()
    conn.execute("DELETE FROM meeting_entries WHERE meeting_id = ?", (meeting_id,))
    conn.execute("DELETE FROM meetings WHERE id = ?", (meeting_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
