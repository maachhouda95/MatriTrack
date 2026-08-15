from flask import Flask, render_template, request, redirect, url_for,session
import mysql.connector

app = Flask(__name__)
app.secret_key="matritrack-secret-key"

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
            session["id_admin"]=admin["id_admin"]
            return redirect(url_for("dashboard"))

        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM materiels
        ORDER BY id_materiel DESC
        LIMIT 5
    """)

    derniers_materiels = cursor.fetchall()
    cursor.close()

    return render_template(
        "dashboard.html",
        derniers_materiels=derniers_materiels
    )


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        type_materiels = request.form.get("type_materiels")
        marque = request.form.get("marque")
        nom_personne = request.form.get("nom_personne")
        departement = request.form.get("departement")

        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO materiels
            (Type_materiels, marque, nom_personne, Departement, id_admin)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                type_materiels,
                marque,
                nom_personne,
                departement,
                session["id_admin"]
            )
        )

        db.commit()
        cursor.close()

        return redirect(url_for("add"))

    return render_template("Add.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/profil")
def profile():
    id_admin = session.get("id_admin")

    if not id_admin:
        return redirect(url_for("login"))

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM administrateur WHERE id_admin = %s",
        (id_admin,)
    )

    admin = cursor.fetchone()
    cursor.close()

    return render_template("profil.html", admin=admin)

if __name__ == "__main__":
    app.run(debug=True)
    
