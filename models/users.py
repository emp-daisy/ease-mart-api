from mongoengine import (Document,
                         EmbeddedDocument,
                         EmbeddedDocumentField,
                         ListField,
                         StringField,
                         EmailField,
                         BooleanField,
                         ReferenceField)
from flask_bcrypt import generate_password_hash, check_password_hash
import re

class Access(EmbeddedDocument):
    """
    Custom EmbeddedDocument to set user authorizations.

    :param user: boolean value to signify if user is a user
    :param admin: boolean value to signify if user is an admin
    """
    user = BooleanField(default=True)
    admin = BooleanField(default=False)


class Users(Document):
    """
    Template for a mongoengine document, which represents a user.
    Password is automatically hashed before saving.

    :param email: unique required email-string value
    :param password: required string value, longer than 6 characters
    :param access: Access object
    :param fav_items: List of Meal objects
    :param name: option unique string username
    :param phone: optional string phone-number, must be valid via regex

    :Example:

    >>> import mongoengine
    >>> from app import default_config

    >>> mongoengine.connect(**default_config['MONGODB_SETTINGS'])
    MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True, read_preference=Primary())

    # Create test user
    >>> new_user = Users(email="spam@ham-and-eggs.com", password="hunter2", access={"admin": True})
    >>> new_user.save()
    >>> new_user.name = "spammy"
    >>> new_user.save()

    # Remove test user
    >>> new_user.delete()

    .. seealso:: :class:`Access`
    """
    meta = {'collection': 'users'}
    email = EmailField(required=True, unique=True)
    full_name = StringField(required=True, unique=False)
    logon_key = StringField(required=True, min_length=6, regex=None)
    access = EmbeddedDocumentField(Access, default=Access(user=True, admin=False))

    def generate_hash(self):
        self.logon_key = generate_password_hash(password=self.logon_key).decode('utf-8')
    # Use documentation from BCrypt for password hashing
    generate_hash.__doc__ = generate_password_hash.__doc__

    def check_hash(self, password: str) -> bool:
        return check_password_hash(pw_hash=self.logon_key, password=password)
    # Use documentation from BCrypt for password hashing
    check_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        self.generate_hash()
        super(Users, self).save(*args, **kwargs)
