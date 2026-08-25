from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

app.secret_key = "matritrack-secret-key"


def get_db():
    return mysql.connector.connect(
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

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM administrateur WHERE USERNAME = %s AND PASSWORD = %s",
            (username, password)
        )

        admin = cursor.fetchone()

        cursor.close()
        db.close()

        if admin:
            session["id_admin"] = admin["id_admin"]
            return redirect(url_for("dashboard"))
        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM materiels
        ORDER BY id_materiel DESC
        LIMIT 10000
    """)
    derniers_materiels = cursor.fetchall()

    cursor.execute("""
        SELECT COALESCE(SUM(quantite), 0) AS total
        FROM materiels
    """)
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COALESCE(SUM(quantite), 0) AS disponible
        FROM materiels
        WHERE etat = 'Disponible'
    """)
    disponible = cursor.fetchone()["disponible"]

    cursor.execute("""
        SELECT COALESCE(SUM(quantite), 0) AS affecte
        FROM materiels
        WHERE etat = 'Affecté'
    """)
    affecte = cursor.fetchone()["affecte"]

    pourcentage_total = 100
    pourcentage_disponible = round((disponible / total) * 100) if total > 0 else 0
    pourcentage_affecte = round((affecte / total) * 100) if total > 0 else 0

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html",
        derniers_materiels=derniers_materiels,
        total=total,
        disponible=disponible,
        affecte=affecte,
        pourcentage_total=pourcentage_total,
        pourcentage_disponible=pourcentage_disponible,
        pourcentage_affecte=pourcentage_affecte
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if "id_admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        type_materiels = request.form.get("type_materiels")
        marque = request.form.get("marque")
        nom_personne = request.form.get("nom_personne")
        departement = request.form.get("departement")
        etat = request.form.get("etat")
        quantite = request.form.get("quantite")

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO materiels
            (Type_materiels, marque, nom_personne, Departement, etat, quantite, id_admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                type_materiels,
                marque,
                nom_personne,
                departement,
                etat,
                quantite,
                session["id_admin"]
            )
        )

        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for("add"))

    return render_template("Add.html")


@app.route("/search")
def search():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM materiels
        ORDER BY id_materiel DESC
    """)

    materiels = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "search.html",
        materiels=materiels
    )


@app.route("/profil")
def profile():
    id_admin = session.get("id_admin")

    if not id_admin:
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM administrateur WHERE id_admin = %s",
        (id_admin,)
    )

    admin = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "profil.html",
        admin=admin
    )


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        type_materiels = request.form.get("type_materiels")
        marque = request.form.get("marque")
        nom_personne = request.form.get("nom_personne")
        departement = request.form.get("departement")
        etat = request.form.get("etat")
        quantite = request.form.get("quantite")

        cursor.execute(
            """
            UPDATE materiels
            SET Type_materiels = %s,
                marque = %s,
                nom_personne = %s,
                Departement = %s,
                etat = %s,
                quantite = %s
            WHERE id_materiel = %s
            """,
            (
                type_materiels,
                marque,
                nom_personne,
                departement,
                etat,
                quantite,
                id
            )
        )

        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for("search"))

    cursor.execute(
        "SELECT * FROM materiels WHERE id_materiel = %s",
        (id,)
    )

    materiel = cursor.fetchone()

    cursor.close()
    db.close()

    if not materiel:
        return "Matériel introuvable", 404

    return render_template(
        "edit.html",
        materiel=materiel
    )


@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM materiels WHERE id_materiel = %s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("search"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

