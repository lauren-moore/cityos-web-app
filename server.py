"""Server for CityOS Video Storage App."""
from flask import Flask, render_template, request, flash, session, redirect, send_file
from model import User, Video, db, connect_to_db
from jinja2 import StrictUndefined
from werkzeug.utils import secure_filename
from datetime import date
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['mp4', 'gif'])



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

    return redirect('/')
    
    
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
        session["id"] = user.id
        flash(f"Welcome back, {user.name.title()}!")
        return redirect("/")



@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["user_id"]
    flash("You have logged out!")

    return redirect("/")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=["POST"])
def upload_video():
    """Upload video to database."""

    video = request.files['video']
    filename = secure_filename(video.filename)
    name = request.form.get("name")

    #check if video was uploaded
    if not video:
        return "Bad Request", 400

    #check if video already exists in database
    existing_video = Video.get_video_by_name(filename)
    if existing_video:
        return "File exists", 409

    #check if video has supported media type
    if video and allowed_file(video.filename):

        video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        mimetype = video.mimetype

        new_video = Video.create_video(fileid=filename, name=name, mimetype=mimetype, created_at=date.today())
        db.session.add(new_video)
        db.session.commit()

    else:
        return "Unsupported Media Type", 415

    return "Video has successfully uploaded", 201


@app.route("/videos")
def view_all_videos():
    """View all videos in database."""

    videos = Video.get_videos()

    return render_template("view_videos.html", videos=videos)



@app.route("/delete/<int:video_id>", methods=["POST"])
def delete(video_id):
    """Delete video from database."""

    video_to_delete = Video.get_video_by_id(video_id)

    if not video_to_delete:
        return "File not found", 404

    db.session.delete(video_to_delete)
    db.session.commit()

    return "File was successfully removed", 204


@app.route("/files/<fileid>")
def download(fileid):
    """Download video file."""

    video_to_download = Video.get_video_by_fileid(fileid)

    #check if video exists in database
    if not video_to_download:
        return "File not found", 404

    #add path to file name
    file_path = app.config['UPLOAD_FOLDER'] + video_to_download.fileid
    
    return send_file(file_path, as_attachment=True), 200



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
