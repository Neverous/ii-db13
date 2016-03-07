# coding: utf-8

import re
import hashlib
import email.utils
from datetime import datetime

from main import *

def admin_users_get():
    return list(db.select(DB_USER, order=u'user_id ASC'))

def user_get(user_id):
    result = list(db.select(DB_USER, {u'user_id': user_id}, where=u'user_id = $user_id', limit=1))
    if not result:
        return None

    return result[0]

def user_login(nick, password):
    with db.transaction():
        password    = password_hash(nick, password)
        result      = list(db.select(DB_USER, {u'nick': nick, u'password': password}, where=u'nick = $nick AND password = $password', limit=1))
        if not result:
            return None

        db.update(DB_USER, vars={u'user_id': result[0].user_id}, where=u'user_id = $user_id', last_login=datetime.now())
        return result[0]

def user_register(nick, name, surname, password, email):
    password = password_hash(nick, password)
    return db.insert(DB_USER, nick=nick, password=password, email=email, name=name, surname=surname)

def user_update(user_id, password, email, name, surname):
    upd = {
        u'name':     name,
        u'surname':  surname,
    }

    if password:
        upd[u'password'] = password = password_hash(nick, password)

    if email:
        upd[u'email'] = email

    db.update(DB_USER, vars={u'user_id': user_id}, where=u'user_id = $user_id', **upd)
    return True

def user_remove(user_id):
    return db.delete(DB_USER, vars={u'user_id': user_id}, where=u'user_id = $user_id')

def password_hash(nick, password):
    return hashlib.sha512(nick + config.DB_SECRET + password).hexdigest()

def email_exists(email, notid=-1):
    return bool(db.select(DB_USER, {u'email': email, u'id': notid}, where=u'email = $email AND user_id != $id', limit=1))

def nick_exists(nick):
    return bool(db.select(DB_USER, {u'nick': nick}, where=u'nick = $nick', limit=1))
