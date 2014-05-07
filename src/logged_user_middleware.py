# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from google.appengine.api import memcache
from models import User
from tekton.gae.middleware import Middleware


def get_user(user_id):
    if not user_id:
        return None
    
    return User.get_by_id(long(user_id))

def execute(next_process, handler, dependencies, **kwargs):
    def _logged_user():
        cookies = handler.request.cookies
        user_id = cookies.get('logged_user')
        return get_user(auth_cookie)

    dependencies["_logged_user"] = _logged_user
    next_process(dependencies, **kwargs)

class LoggedUserMiddleare(Middleware):
    def set_up(self):
        def _logged_user():
            cookies = self.handler.request.cookies
            user_id = cookies.get('logged_user')
            return get_user(user_id)

        self.dependencies["_logged_user"] = _logged_user
