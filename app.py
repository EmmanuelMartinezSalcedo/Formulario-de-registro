from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    DateField,
    SelectField
)
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_BINDS"] = {"images": "sqlite:///images.db"}
app.config["SECRET_KEY"] = "secretkey"
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class images(db.Model):
    __bind_key__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(200))
    name = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return "\nNombre: {}. Precio: {}. Descripción: {}. Imagen: {}.\n".format(
            self.name, self.price, self.description, self.img
        )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "img": self.img,
        }


class RegisterForm(FlaskForm):
    name = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Nombre"},
    )
    lastname = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Apellido"},
    )
    birthday = DateField(
        "birthday",
        format="%Y-%m-%d",
        validators=[InputRequired()],
        render_kw={"placeholder": "Fecha de nacimiento"},
    )
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Correo"},
    )

    sex = SelectField("sex", choices=[("H", "Hombre"), ("F", "Mujer")])

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Contraseña"},
    )

    submit = SubmitField("Registrar")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "Ese correo ya existe, elija otro"
            )


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Correo"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Contraseña"},
    )

    submit = SubmitField("Iniciar sesión")


@app.route("/")
def home():
    return redirect("/register")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("tienda"))
    return render_template("login.html", form=form)

@app.route("/usersapi")
@login_required
def api2():
    try:
        users = User.query.all()
        toReturn2 = [user.serialize() for user in users]
        return jsonify(toReturn2), 200

    except Exception:
        print("[SERVER]: Error")
        return jsonify({"msg": "Ha ocurrido un error"}),

@app.route("/tienda/api")
@login_required
def api():
    try:
        productos = images.query.all()
        toReturn = [producto.serialize() for producto in productos]
        return jsonify(toReturn), 200

    except Exception:
        print("[SERVER]: Error")
        return jsonify({"msg": "Ha ocurrido un error"}), 500


@app.route("/tienda", methods=["GET", "POST"])
@login_required
def tienda():
    hists = os.listdir('static/productos')
    hists = ['productos/' + file for file in hists]
    return render_template("tienda.html", hists = hists, products = toReturn)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/product", methods=["GET", "POST"])
def product():
    if request.method == "POST":
        file = request.files["imagen"]
        filename = secure_filename(file.filename)

        file.save(os.path.join("./static/productos", filename))
        path = "static/productos/" + filename

        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        nombre = request.form.get("nombre")
        imagen_ = images(name=nombre, price=precio, description=descripcion, img=path)
        db.session.add(imagen_)
        db.session.commit()
        return redirect(url_for("tienda"))
    return render_template("product.html")
