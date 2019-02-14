from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """
    class modelling the users
    """

    __tablename__ = 'users'

    #create the columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    pitch = db.relationship('Pitch', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    like = db.relationship('Like', backref='user', lazy='dynamic')
    dislike = db.relationship('Dislike', backref='user', lazy='dynamic')


    # securing passwords

    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'



class Pitch(db.Model):
    """
    List of pitches in each category
    """

    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment = db.relationship("Comment", backref="pitches", lazy="dynamic")
    like = db.relationship("Like", backref="pitches", lazy="dynamic")
    dilike = db.relationship("Dislike", backref="pitches", lazy="dynamic")


    def save_pitch(self):
        """
        Save the pitches
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()

    # display pitches

    def get_pitches(id):
        pitches = Pitch.query.filter_by(category_id=id).all()
        return pitches



class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db. Integer, primary_key=True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))


    def save_comment(self):
        db.session.add(self)
        db.session.commit()



    @classmethod
    def get_comments(self, id):
        comment = Comment.query.order_by(Comment.time_posted.desc()).filter_by(pitches_id=id).all()
        return comment


class PitchCategory(db.Model):

    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls):
        categories = PitchCategory.query.all()
        return categories

class Like(db.Model):
    __tablename__ = 'likes'
    '''
    class that takes number of upvote in aparticular pitch
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    likes = db.Column(db.Integer,default=1)

    def save_like(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Like {self.id}'


class Dislike(db.Model):
    __tablename__ = 'dislike'
    '''
    class that define my comments
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    dislikes = db.Column(db.Integer,default=1)

    def save_Dislike(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Dislike {self.id}'


class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer, primary_key=True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
