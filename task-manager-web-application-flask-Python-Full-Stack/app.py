from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

@app.route("/")
def home():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    connection.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form["description"]

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
        (title, description, "Pending")
    )
    connection.commit()
    connection.close()

    return redirect("/")

@app.route("/complete/<int:id>")
def complete_task(id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", ("Completed", id))
    connection.commit()
    connection.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_task(id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    connection.commit()
    connection.close()

    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)