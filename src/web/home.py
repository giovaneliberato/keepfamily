# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import hashlib
from google.appengine.api import memcache
from models import User
from tekton import router

AUTH_TOKEN = "AUTH_TOKEN"

def index(_write_tmpl, _logged_user, error=''):
    _write_tmpl('home.html', {'error': error})


def cadastrar(_handler, _resp, name, username, email, passwd):
    if User.get_by_username(username):
        _handler.redirect(router.to_path(index, "username_error"))
        return
        
    u = User(name=name, username=username.strip(), email=email, passwd=passwd)
    u.put()
    logar(_handler, _resp, username, passwd)


def logar(_handler, _resp, username, passwd):
    found = User.get_by_username_and_pw(username.strip(), passwd)
    if not found:
        _handler.redirect(router.to_path(index, "login_error"))
    
    else:
        token = "%s%s" % (username, AUTH_TOKEN)
        _resp.set_cookie('logged_user', str(found.key.id()))
        _handler.redirect(router.to_path(index))

def logout(_resp, _handler):
    _resp.delete_cookie('logged_user')
    _handler.redirect(router.to_path(index))
