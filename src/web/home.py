# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time
import json
import base64
from google.appengine.api import memcache
from models import User
from tekton import router

AUTH_TOKEN = "AUTH_TOKEN"

def index(_handler, _write_tmpl, _logged_user, errors=""):
    if _logged_user():
        _write_tmpl('index.html', {'page': 'home'})
    else:
        errors = errors.split()
        _write_tmpl('landing.html', {"errors": errors})


def cadastrar(_handler, _resp, name, username, email, passwd):
    errors = []
    if User.get_by_username(username):
        errors.append('username_error')

    if "@" not in email or "." not in email:
        errors.append('invalid_email')

    if len(passwd) < 6:
        errors.append('invalid_pw')

    if errors:
        url = router.to_path(index) + "?errors=" + "+".join(errors)
        _handler.redirect(url)
        return

    u = User(name=name, username=username.strip(), email=email, passwd=passwd)
    u.put()
    
    #to avoid eventually consistency
    time.sleep(0.5)

    logar(_handler, _resp, username, passwd)


def logar(_handler, _resp, username, passwd):
    found = User.get_by_username_and_pw(username.strip(), passwd)
    if not found:
        _handler.redirect(router.to_path(index) + "?errors=loggin_error")
    
    else:
        token = "%s%s" % (username, AUTH_TOKEN)
        _resp.set_cookie('logged_user', str(found.key.id()))
        _handler.redirect(router.to_path(index))

def logout(_resp, _handler):
    _resp.delete_cookie('logged_user')
    _handler.redirect(router.to_path(index))


def despesas(_write_tmpl):
    _write_tmpl('despesas.html', {'page': 'despesas'})
