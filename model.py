"""Model for CityOS Video Storage App."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Video(db.Model):
    """A video uploaded by a user."""

    __tablename__ = 'videos'

    video_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    fileid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    mimetype = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)



    def __repr__(self):
        return f'<id={self.video_id} name={self.name}>'


    @classmethod
    def create_video(self, fileid, name, mimetype, created_at):
        """Create and return a new video."""
        new_video = Video(name=name, fileid=fileid, mimetype=mimetype, created_at=created_at)

        return new_video

    @classmethod
    def get_videos(self):
        return Video.query.all()

    @classmethod
    def get_video_by_id(self, id):
        return Video.query.get(id)
    
    @classmethod
    def get_video_by_name(self, name):
        return Video.query.filter(Video.name == name).first()

    @classmethod
    def get_video_by_fileid(self, fileid):
        return Video.query.filter(Video.fileid == fileid).first()




def connect_to_db(flask_app, db_uri="postgresql:///videos", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
