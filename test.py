from flask import Flask
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="houda2004",
    database="MatriTrack"
)


@app.route("/")
def home():
    return render_template ('')


if __name__ == "__main__":
    app.run(debug=True) 
