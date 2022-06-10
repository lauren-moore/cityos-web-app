"""Server for CityOS Video Storage App."""
from flask import Flask, render_template, request, flash, session, redirect, send_file
from model import Video, db, connect_to_db
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
ALLOWED_EXTENSIONS = set(['mp4', 'mpeg'])


@app.route('/')
def homepage():
    """View homepage."""
  
    return render_template('homepage.html')


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
        flash("Bad Request")
        return render_template("homepage.html"), 400

    #check if video already exists in database
    existing_video = Video.get_video_by_name(filename)
    if existing_video:
        flash("File exists")
        return render_template("homepage.html"), 409

    #check if video has supported media type
    if video and allowed_file(video.filename):

        video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        mimetype = video.mimetype

        #add video to database if supported media type
        new_video = Video.create_video(fileid=filename, name=name, mimetype=mimetype, created_at=date.today())
        db.session.add(new_video)
        db.session.commit()

    #if video has unsupported media type
    else:
        flash("Unsupported Media Type")
        return render_template("homepage.html"), 415

    #video has been uploaded
    flash("Video has successfully uploaded!")
    return render_template("videw_videos.html"), 201


@app.route("/videos")
def view_all_videos():
    """View all videos in database."""

    videos = Video.get_videos()

    return render_template("view_videos.html", videos=videos)



@app.route("/delete/<int:video_id>", methods=["POST"])
def delete(video_id):
    """Delete video from database."""

    video_to_delete = Video.get_video_by_id(video_id)

    #check if file exists in database
    if not video_to_delete:
        flash("File not found")
        return render_template("view_videos.html"), 404


    #remove file from database if it exists
    db.session.delete(video_to_delete)
    db.session.commit()

    flash("File was successfully removed")
    return render_template("view_videos.html"), 203


@app.route("/files/<fileid>")
def download(fileid):
    """Download video file."""

    video_to_download = Video.get_video_by_fileid(fileid)

    #check if video exists in database
    if not video_to_download:
        flash("File not found")
        return render_template("view_videos.html"), 404

    #add path to file name
    file_path = app.config['UPLOAD_FOLDER'] + video_to_download.fileid
    
    return send_file(file_path, as_attachment=True), 200



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
