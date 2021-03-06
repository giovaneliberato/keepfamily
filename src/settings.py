# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from middlewares.tmpl_middleware import TemplateMiddleware
from middlewares.logged_user_middleware import LoggedUserMiddleare
from tekton.gae.middleware.email_errors import EmailMiddleware
from tekton.gae.middleware.json_middleware import JsonMiddleare
from tekton.gae.middleware.parameter import RequestParamsMiddleware
from tekton.gae.middleware.router_middleware import RouterMiddleware
from tekton.gae.middleware.webapp2_dependencies import Webapp2Dependencies

SENDER_EMAIL = 'renzon@gmail.com'
WEB_BASE_PACKAGE = "web"
MIDDLEWARES = [LoggedUserMiddleare,
               TemplateMiddleware,
               JsonMiddleare,
               EmailMiddleware,
               Webapp2Dependencies,
               RequestParamsMiddleware,
               RouterMiddleware]

