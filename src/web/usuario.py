#coding: utf-8
import time
from models import User
from home import index as site_index
from tekton import router

AUTH_TOKEN = "AUTH_TOKEN"

def cadastrar(_handler, _resp, name, username, email, passwd):
    errors = []
    if User.get_by_username(username):
        errors.append('username_error')

    if "@" not in email or "." not in email:
        errors.append('invalid_email')

    if len(passwd) < 6:
        errors.append('invalid_pw')

    if errors:
        url = router.to_path(site_index) + "?errors=" + "+".join(errors)
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
        _handler.redirect(router.to_path(site_index) + "?errors=loggin_error")
    
    else:
        token = "%s%s" % (username, AUTH_TOKEN)
        _resp.set_cookie('logged_user', str(found.key.id()))
        _handler.redirect(router.to_path(site_index))

def logout(_resp, _handler):
    _resp.delete_cookie('logged_user')
    _handler.redirect(router.to_path(site_index))
