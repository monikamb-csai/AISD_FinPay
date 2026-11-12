from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db
from repository import UserRepository, TransactionRepository
from services import PaymentService

app = Flask(__name__)
app.secret_key = "change-this-demo-secret-key"
init_db()

users = UserRepository()
transactions = TransactionRepository()
payments = PaymentService()

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = users.get_by_id(session["user_id"])
    history = transactions.for_user(session["user_id"])
    return render_template("dashboard.html", user=user, history=history)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Enter all details. Password must contain at least 8 characters.")
            return redirect(url_for("register"))
        if users.get_by_email(email):
            flash("An account with this email already exists.")
            return redirect(url_for("register"))
        user_id = users.create(name, email, generate_password_hash(password))
        session["user_id"] = user_id
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = users.get_by_email(email)
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session["user_id"] = user["id"]
            return redirect(url_for("home"))
        flash("Incorrect email or password.")
    return render_template("login.html")

@app.route("/transfer", methods=["POST"])
def transfer():
    if "user_id" not in session:
        return redirect(url_for("login"))
    recipient_email = request.form.get("recipient_email", "").strip().lower()
    try:
        amount = float(request.form.get("amount", "0"))
        message = payments.transfer(session["user_id"], recipient_email, amount)
        flash(message)
    except ValueError as error:
        flash(str(error))
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
