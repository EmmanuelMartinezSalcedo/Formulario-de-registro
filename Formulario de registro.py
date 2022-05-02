from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/yourprofile", methods=["POST"])
def perfil():
    lastname = request.form.get("apellido")
    name = request.form.get("nombre")
    date = request.form.get("fecha")
    sex = request.form.get("sexo")
    return render_template("profile.html", apellido=lastname, nombre=name, fecha=date, sexo=sex)