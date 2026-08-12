from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/login", methods=["GET","POST"])

def login():
    if request.method=="POST":
        uSername=request.form.get("username")
        password=request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            return redirect (url_for("welcome"))
        else:
            return render_template("login.html",error="Invalid username or password")
    return render_template ("login.html")  

    if __name__=="__main__":
        app.run(debug=True)        
    