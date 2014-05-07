import md5
from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    passwd = ndb.StringProperty(required=True)

    @classmethod
    def get_by_username_and_pw(cls, username, pw):
        return cls.query(cls.username == username, cls.passwd == pw).get()

    @classmethod
    def get_by_username(cls, username):
        return cls.query(cls.username == username).get()
