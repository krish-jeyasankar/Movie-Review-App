from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)
app.secret_key = "change_this_secret_key"


# ---------------------------
# DATABASE CONNECTION
# ---------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def home():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM movies")
    movies = c.fetchall()
    return render_template("index.html", movies=movies)

# ---------------------------
# MOVIE PAGE (SHOW DESCRIPTION) 
# ---------------------------
@app.route("/movie/<int:movie_id>") 
def movie_page(movie_id): 
    conn = get_db() 
    c = conn.cursor() 
    
    c.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)) 
    movie = c.fetchone() 
    
    if not movie: return "Movie not found" 

    
    # Load reviews for this movie 
    c.execute(""" SELECT reviews.*, users.name 
              FROM reviews 
              JOIN users ON reviews.user_id = users.id 
              WHERE movie_id = ? 
              ORDER BY reviews.id DESC 
              """, (movie_id,)) 
    reviews = c.fetchall() 
    return render_template("movie_page.html", movie=movie, reviews=reviews)


# ---------------------------
# ADD MOVIE PAGE
# ---------------------------
@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        description = request.form["description"]

        conn = get_db()
        c = conn.cursor()

        c.execute("""
            INSERT INTO movies (title, year, description)
            VALUES (?, ?, ?)
        """, (title, year, description))

        conn.commit()
        return redirect(url_for("home"))

    return render_template("add_movie.html")

# ---------------------------
# REGISTER
# ---------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"].lower()
        password = generate_password_hash(request.form["password"])

        conn = get_db()
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password),
            )
            conn.commit()
        except:
            return "Email already exists"

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------------------
# LOGIN
# ---------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("review"))
        else:
            return "Invalid login"

    return render_template("login.html")


# --------------------------- 
# LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------
# REVIEW PAGE
# ---------------------------
@app.route("/review", methods=["GET", "POST"])
def review():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    c = conn.cursor()

    # POST new review
    if request.method == "POST":
        title = request.form["title"]
        rating = request.form["rating"]
        text = request.form["text"]
        date = datetime.now().strftime("%Y-%m-%d")

        c.execute(
            """
            INSERT INTO reviews (user_id, title, rating, text, date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session["user_id"], title, rating, text, date),
        )
        conn.commit()

    # GET all reviews
    c.execute(
        """
        SELECT reviews.*, users.name 
        FROM reviews 
        JOIN users ON reviews.user_id = users.id
        ORDER BY reviews.id DESC
        """
    )
    reviews = c.fetchall()

    return render_template("review.html", reviews=reviews, user=session["user_name"])



# ---------------------------
# REVIEW DETAIL PAGE
# ---------------------------
@app.route("/review/<int:review_id>")
def review_detail(review_id):
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        SELECT reviews.*, users.name 
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.id = ?
    """, (review_id,))
    review = c.fetchone()

    if not review:
        return "Review not found"

    return render_template("review_detail.html", review=review)

# ---------------------------
# EDIT REVIEW
# ---------------------------
@app.route("/review/edit/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    c = conn.cursor()

    # Fetch review
    c.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    review = c.fetchone()

    if not review:
        return "Review not found"

    # Ownership check
    if review["user_id"] != session["user_id"]:
        return "Unauthorized"

    # Save changes
    if request.method == "POST":
        title = request.form["title"]
        rating = request.form["rating"]
        text = request.form["text"]

        c.execute(
            """
            UPDATE reviews
            SET title = ?, rating = ?, text = ?
            WHERE id = ?
            """,
            (title, rating, text, review_id),
        )
        conn.commit()

        return redirect(url_for("review"))

    return render_template("edit_review.html", review=review)


# ---------------------------
# DELETE REVIEW
# ---------------------------
@app.route("/review/delete/<int:review_id>")
def delete_review(review_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    c = conn.cursor()

    # Fetch review
    c.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    review = c.fetchone()

    if not review:
        return "Review not found"

    # Ownership check
    if review["user_id"] != session["user_id"]:
        return "Unauthorized"

    # Delete review
    c.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()

    return redirect(url_for("review"))


# ---------------------------
# PROFILE PAGE
# ---------------------------
@app.route("/profile") 
def profile(): 
    if "user_id" not in session:
        return redirect(url_for("login")) 
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)) 
    user = c.fetchone() 
    
    c.execute("SELECT * FROM reviews WHERE user_id = ?", (session["user_id"],)) 
    reviews = c.fetchall() 
    
    return render_template("profile.html", user=user, reviews=reviews)

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
