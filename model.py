"""Model for CityOS Video Storage App."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Video(db.Model):
    """A video uploaded by a user."""

    __tablename__ = 'videos'

    id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    img = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    mimetype = db.Column(db.String, nullable=False)



    def __repr__(self):
        return f'<id={self.id} name={self.name}>'


    @classmethod
    def create_video(self, img, name, mimetype):
        """Create and return a new video."""
        new_video = Video(img=img, 
                        name=name,
                        mimetype=mimetype)

        return new_video

    @classmethod
    def get_videos(self):
        return Video.query.all()

    @classmethod
    def get_video_by_id(self, id):
        return Video.query.get(id)
    
    # @classmethod
    # def get_video_by_name(self, name):
    #     return Video.query.filter(Video.name == name).first()



class User(db.Model):
    """A user."""
 
    __tablename__ = "users"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


    def __repr__(self):
        return f'<User id={self.id} name={self.name} email={self.email}>'


    @classmethod
    def create_user(self, name, email, password):
        """Create and return a new user."""
        user = User(name=name,
                    email=email, 
                    password=password)

        return user

    @classmethod
    def get_user_by_id(self, user_id):
        '''get user by id.'''

        return User.query.get(user_id)

    @classmethod
    def get_user_by_email(self, email):
        '''get user by email.'''
    
        return User.query.filter(User.email == email).first()


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
