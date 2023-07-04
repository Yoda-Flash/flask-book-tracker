from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BookTracker(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date())
    complete = db.Column(db.Boolean)

@app.route("/")
def home():
    book_list = BookTracker.query.all()
    return render_template("index.html", book_list = book_list)

@app.route("/add", methods = ["Post"])
def add():
    book_name = request.form.get("book_name")
    start_date = datetime.date(datetime.strptime(request.form.get("start_date"), '%Y-%m-%d'))
    print(f"Start date: {start_date}")
    new_book = BookTracker(book_name = book_name, start_date = start_date, complete = False)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:book_id>")
def update(book_id):
    book = BookTracker.query.filter_by(id = book_id).first()
    book.end_date = request.form.get("end_date")
    book.complete = not book.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:book_id>")
def delete(book_id):
    book = BookTracker.query.filter_by(id = book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(debug=False)