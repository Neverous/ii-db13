# coding: utf-8

import re
import hashlib
import email.utils
from datetime import datetime

from main import *

from models.user import *

def email_validate(_email):
    return email.utils.parseaddr(_email)[1] != u''

def nick_validate(nick):
    return 4 <= len(nick) <= 64 and nick.lower() == nick and re.match(r'\w+', nick)

def name_validate(name):
    return len(name) <= 256 and re.match(r'[\w ]+', name, re.UNICODE)

def surname_validate(surname):
    return len(surname) <= 256 and re.match(r'[\w ]+', surname, re.UNICODE)

class user_view:
    @check_logged(get_url(u'user_login_view'))
    def GET(self):
        generate_token()
        user = user_get(session.user_id)
        return layout.get().user(user.nick, user.email, user.name, user.surname)

    @check_logged(get_url(u'user_login_view'))
    def POST(self):
        req = web.input(password=u'', password_repeat=u'', email=u'', name=u'', surname=u'', token=u'')
        req.email   = req.email.strip()
        req.name    = req.name.strip()
        req.surname = req.surname.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'user_view'))

        success = True
        if req.password and req.password != req.password_repeat:
            put_message(u'danger', u'Hasła się nie zgadzają!')
            success = False

        elif not email_validate(req.email):
            put_message(u'danger', u'Ten adres e-mail jest niepoprawny!')
            success = False

        elif email_exists(req.email, session.user_id):
            put_message(u'danger', u'Ten adres e-mail już istnieje w bazie danych!')
            success = False

        elif not name_validate(req.name) or not surname_validate(req.surname):
            put_message(u'danger', u'Niepoprawne imię lub nazwisko')
            success = False

        else:
            user = user_update(session.user_id, req.password, req.email, req.name, req.surname)

            if user:
                put_message(u'success', u'Zapisano dane!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        if success:
            return web.seeother(req.next or get_url(u'users_view'))

        generate_token()
        return layout.get().user(user.nick, req.email, req.name, req.surname)

class user_login_view:
    def GET(self):
        req = web.input(next=u'')
        req.next = req.next.strip()
        if session.user_id != None:
            return web.seeother(req.next or get_url(u'gardens_view'))

        generate_token()
        return layout.get().user_login(next=req.next)

    def POST(self):
        req = web.input(nick=u'', password=u'', token=u'', next=u'')
        req.nick        = req.nick.strip()
        req.password    = req.password.strip()
        req.next        = req.next.strip()
        if session.user_id != None:
            return web.seeother(req.next or get_url(u'gardens_view'))

        if not check_token(req.token):
            return web.seeother(get_url(u'user_login_view'))

        user = user_login(req.nick, req.password)
        if not user:
            put_message(u'danger', u'Niepoprawna nazwa użytkownika lub hasło!')
            generate_token()
            return layout.get().user_login(req.nick, req.next)

        session.user_id     = user.user_id
        session.admin_id    = user.admin == True and user.user_id or None
        return web.seeother(req.next or get_url(u'gardens_view'))

class user_logout_view:
    def GET(self):
        session.kill()
        return web.seeother(web.input(next=u'').next.strip() or get_url(u'index_view'))

    POST = GET

class user_register_view:
    def GET(self):
        req = web.input(next=u'')
        req.next = req.next.strip()
        if session.user_id != None:
            return web.seeother(req.next or get_url(u'gardens_view'))

        generate_token()
        return layout.get().user_register(next=req.next)

    def POST(self):
        req = web.input(nick=u'', password=u'', password_repeat=u'', email=u'', name=u'', surname=u'', token=u'', next=u'')
        req.nick    = req.nick.strip()
        req.email   = req.email.strip()
        req.name    = req.name.strip()
        req.surname = req.surname.strip()
        req.next    = req.next.strip()

        if session.user_id != None:
            return web.seeother(req.next or get_url(u'user_view'))

        if not check_token(req.token):
            return web.seeother(get_url(u'user_register_view'))

        success = True
        if not nick_validate(req.nick):
            put_message(u'danger', u'Niepoprawny login!')
            success = False

        elif nick_exists(req.nick):
            put_message(u'danger', u'Nick już zajęty!')
            success = False

        elif not req.password:
            put_message(u'danger', u'Hasło nie może być puste!')
            success = False

        elif req.password != req.password_repeat:
            put_message(u'danger', u'Hasła się nie zgadzają!')
            success = False

        elif not email_validate(req.email):
            put_message(u'danger', u'Ten adres e-mail jest niepoprawny!')
            success = False

        elif email_exists(req.email):
            put_message(u'danger', u'Ten adres e-mail już istnieje w bazie danych!')
            success = False

        elif not name_validate(req.name) or not surname_validate(req.surname):
            put_message(u'danger', u'Niepoprawne imię lub nazwisko')
            success = False

        else:
            user = user_register(req.nick, req.name, req.surname, req.password, req.email)

            if user:
                put_message(u'success', u'Zostałeś zarejestrowany!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        if success:
            return web.seeother(req.next or get_url(u'gardens_view'))

        generate_token()
        return layout.get().user_register(req.nick, req.email, req.name, req.surname, req.next)
