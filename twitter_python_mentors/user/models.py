# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from twitter_python_mentors.database import Column, Model, SurrogatePK, db, reference_col, relationship
from twitter_python_mentors.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class UserDisciplinesAssoc(SurrogatePK, Model):
    __tablename__ = 'user_disciplines_assoc'

    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    discipline_id = Column(db.Integer, db.ForeignKey('disciplines.id'))


class UserLanguageAssoc(SurrogatePK, Model):
    __tablename__ = 'user_language_assoc'

    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    language_id = Column(db.Integer, db.ForeignKey('languages.id'))


class Language(SurrogatePK, Model):
    __tablename__ = 'languages'

    language = Column(db.String(20))


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)

    email = Column(db.String(80), unique=True, nullable=True)
    twitter = Column(db.String(80), unique=True, nullable=True)
    reddit = Column(db.String(80), unique=True, nullable=True)

    disciplines = relationship('Discipline', secondary=UserDisciplinesAssoc)
    spoken_languages = relationship('Language', secondary=UserLanguageAssoc)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class Discipline(SurrogatePK, Model):
    __tablename__ = 'disciplines'

    name = Column(db.String(80), unique=True, nullable=False)


class CommentDisciplinesAssoc(SurrogatePK, Model):
    __tablename__ = 'comment_disciplines_assoc'

    comment_id = Column(db.Integer, db.ForeignKey('comments.id'))
    discipline_id = Column(db.Integer, db.ForeignKey('disciplines.id'))


class Comment(SurrogatePK, Model):
    __tablename__ = 'comments'

    text = Column(db.String(500), unique=False, nullable=True)
    for_user_id = Column(db.Integer, db.ForeignKey('users.id'))
    was_helped = Column(db.Boolean, nullable=False)
    on_disciplines = relationship('Discipline', secondary=CommentDisciplinesAssoc)
