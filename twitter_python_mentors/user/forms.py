# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User


class RegisterForm(FlaskForm):
    """Register form."""

    display_name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=3, max=25)],
    )
    email = StringField(
        'Email',
        validators=[Email(), Length(min=6, max=40)],
    )
    twitter = StringField(
        'Twitter',
        validators=[Length(min=0, max=40)],
    )
    reddit = StringField(
        'Reddit',
        validators=[Length(min=0, max=40)],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered')
            return False
        return True
