"""Server for CityOS Video Storage App."""
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import User, Video, db, connect_to_db
from jinja2 import StrictUndefined
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def homepage():
    """View homepage."""
  
    return render_template('homepage.html')



@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_user_by_email(email)

    if user:
        flash("An account has already been created with that email address. Try again.")
    else:
        user = User.create_user(name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect('/login')
    
    
@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")

        return redirect(request.referrer)

    else:
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.name.title()}!")
        return redirect("/")



@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["user_id"]
    flash("You have logged out!")

    return redirect("/")



@app.route('/upload', methods=["POST"])
def upload_video():

    video = request.files['video']

    if not video:
        flash("No video uploaded.")

    filename = secure_filename(video.filename)
    mimetype = video.mimetype

    new_video = Video.create_video(video=video.read(), name=filename, mimetype=mimetype)
    db.session.add(new_video)
    db.session.commit()

    return "Video has successfully uploaded", 200



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
