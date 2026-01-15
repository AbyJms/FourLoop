from flask import Flask, request, jsonify, session, render_template, redirect
from db import mysql, init_db

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "trash-secret-key"

init_db(app)

# --------------------
# PAGES
# --------------------

@app.get("/")
def auth_page():
    return render_template("auth.html")

@app.get("/dashboard")
def dashboard_page():
    if "uid" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.get("/mission")
def mission_page():
    if "uid" not in session:
        return redirect("/")
    return render_template("mission.html")

@app.get("/profile")
def profile_page():
    if "uid" not in session:
        return redirect("/")
    return render_template("profile.html")

@app.get("/store")
def store_page():
    if "uid" not in session:
        return redirect("/")
    return render_template("store.html")

@app.post("/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})

# --------------------
# AUTH
# --------------------

@app.post("/register")
def register():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
        (data["username"], data["email"], data["password"]),
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({"ok": True})

@app.post("/login")
def login():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (data["username"], data["password"]),
    )
    row = cur.fetchone()
    cur.close()

    if not row:
        return jsonify({"error": "Invalid credentials"}), 401

    session["uid"] = row[0]
    return jsonify({"ok": True})

# --------------------
# DATA API
# --------------------

@app.get("/api/dashboard")
def dashboard_data():
    if "uid" not in session:
        return jsonify({"error": "Not logged in"}), 401

    cur = mysql.connection.cursor()

    # User info + title
    cur.execute("""
        SELECT u.username, u.points, u.credits, u.total_points, t.name
        FROM users u
        LEFT JOIN titles t ON u.title_id = t.id
        WHERE u.id = %s
    """, (session["uid"],))
    u = cur.fetchone()

    # Leaderboard (top 10)
    cur.execute("""
        SELECT username, total_points
        FROM users
        ORDER BY total_points DESC
        LIMIT 10
    """)
    leaderboard = cur.fetchall()

    # Rank
    cur.execute("""
        SELECT COUNT(*) + 1
        FROM users
        WHERE total_points > %s
    """, (u[3],))
    rank = cur.fetchone()[0]

    cur.close()

    return jsonify({
        "user": {
            "username": u[0],
            "points": u[1],
            "credits": u[2],
            "total_points": u[3],
            "title": u[4],
            "rank": rank
        },
        "leaderboard": [
            {"username": r[0], "points": r[1]} for r in leaderboard
        ],
        "currentZone": "Crimson Wastefront",
        "boss": {"name": "Demo-garbage", "hp": 42}
    })

@app.get("/api/profile")
def profile_data():
    if "uid" not in session:
        return jsonify({"error": "Not logged in"}), 401

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT u.username, u.points, u.credits, u.total_points, t.name
        FROM users u
        LEFT JOIN titles t ON u.title_id = t.id
        WHERE u.id = %s
    """, (session["uid"],))
    u = cur.fetchone()

    cur.execute("""
        SELECT COUNT(*) + 1
        FROM users
        WHERE total_points > %s
    """, (u[3],))
    rank = cur.fetchone()[0]

    cur.close()

    return jsonify({
        "username": u[0],
        "points": u[1],
        "credits": u[2],
        "total_points": u[3],
        "title": u[4],
        "rank": rank
    })

if __name__ == "__main__":
    app.run(debug=True)
