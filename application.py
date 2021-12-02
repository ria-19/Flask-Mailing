import os
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_mail import Mail, Message

DATABASE = "./birthdays.db"

# Configure application
app = Flask(__name__)

# Configure application for Mailing
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Connect to DATABASE using sqlite3
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        email = request.form.get("email")
        if not day or not month or not name or not email:
            return render_template("Invalid.html")
        if month in [4, 6, 9 , 11] and day == 31:
            return render_template("Invalid.html")
        if month == 2 and day >= 28:
            return render_template("Invalid.html")
        
        conn = get_db_connection() 
        cursor = conn.cursor()
        cursor.execute("INSERT INTO birthdays (name, month, day, email) VALUES (?, ?, ?, ?)", [name, month, day, email])
        conn.commit()
        conn.close()

        msg = f"Hey {name}! You are registered for Birthday Group!!"
        message = Message(msg, recipients=[email])
        mail.send(message)
        return redirect("/")

    else:
        conn = get_db_connection() 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM birthdays")
        birthdays = cursor.fetchall()
        conn.close()
        return render_template("index.html", birthdays=birthdays)

@app.route("/delete")
def delete():
    id = request.args.get("delete")
    conn = get_db_connection() 
    cursor = conn.cursor()
    cursor.execute("DELETE FROM birthdays WHERE id = (?)", [id])
    conn.commit()
    conn.close()
    return redirect("/")


