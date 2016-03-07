# coding: utf-8

import time
import hashlib

from main import *

def put_message(_type, body):
    session.messages.append({u'type': _type, u'body': body})
    return True

def clear_messages():
    del session.messages[:]

def generate_token():
    session.token = hashlib.sha256(web.ctx.get(u'ip') + unicode(time.time())).hexdigest()

def check_token(token):
    token = token.strip()
    if not token or not session.get(u'token') or token != session.token:
        session.token = u''
        del session.token
        return False

    session.token = u''
    del session.token
    return True

def check_logged(url):
    def wrap(fn):
        def check(*args, **kwargs):
            if session.user_id == None:
                return web.seeother(url)

            return fn(*args, **kwargs)

        return check

    return wrap

def check_admin(url):
    def wrap(fn):
        def check(*args, **kwargs):
            if session.admin_id == None:
                return web.seeother(url)

            return fn(*args, **kwargs)

        return check

    return wrap
