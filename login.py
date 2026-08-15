from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="houda2004",
    database="MatriTrackBD"
)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        print(username)
        print(password)

        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM administrateur WHERE USERNAME = %s AND PASSWORD = %s",
            (username, password)
        )

        admin = cursor.fetchone()
        cursor.close()

        if admin:
            return redirect(url_for("dashboard"))

        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
    
