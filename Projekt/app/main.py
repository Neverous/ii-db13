# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding(u'utf-8')

def date_conv(val):
    import datetime
    year, month, day = map(int, val.split(u'-'))
    return datetime.date(year, month, day)

def time_conv(val):
    import datetime
    val = val.split(u'.')
    hours, minutes, seconds = map(int, val[0].split(u':'))
    microseconds = len(val) == 2 and int(val[1]) or 0
    return datetime.time(hours, minutes, seconds, microseconds)

def datetime_conv(val):
    import datetime
    if u' ' not in val:
        if u':' in val:
            return time_conv(val)

        assert u'-' in val
        return date_conv(val)

    datepart, timepart = val.split(' ')
    return datetime.datetime.combine(date_conv(datepart), time_conv(timepart))

import sqlite3
sqlite3.register_converter('DATETIME', datetime_conv)
sqlite3.register_converter('DATE', datetime_conv)
sqlite3.register_converter('TIME', datetime_conv)
sqlite3.register_converter('TIMESTAMP', datetime_conv)

import time
import config
import web
web.config.debug = config.DEBUG
import urls
from urls import get_url

app     = web.application(urls.URLS, globals())
db      = web.database(**config.DB_OPTIONS)

def _connectWrapper(fn):
    def _connect(*args, **kwargs):
        res = fn(*args, **kwargs)
        res.execute(u'PRAGMA foreign_keys = ON;')
        return res

    return _connect

db._connect = _connectWrapper(db._connect)

store   = web.session.DBStore(db, config.DB_PREFIX + u'session')
session = web.session.Session(app, store, initializer={
    u'messages': list(),
    u'user_id':  None,
    u'admin_id': None,
    u'token':    None,
})

DB_GARDEN               = u'"{0}garden"'.format(config.DB_PREFIX)
DB_FIELD                = u'"{0}field"'.format(config.DB_PREFIX)
DB_PLACEMENT            = u'"{0}placement"'.format(config.DB_PREFIX)
DB_PLACEMENT_FIELD      = u'"{0}placement_field"'.format(config.DB_PREFIX)
DB_PLACEMENT_PRODUCT    = u'"{0}placement_product"'.format(config.DB_PREFIX)
DB_PLANT                = u'"{0}plant"'.format(config.DB_PREFIX)
DB_EVENT                = u'"{0}event"'.format(config.DB_PREFIX)
DB_EVENT_REQUIREMENT    = u'"{0}event_requirement"'.format(config.DB_PREFIX)
DB_USER                 = u'"{0}user"'.format(config.DB_PREFIX)
DB_WAREHOUSE            = u'"{0}warehouse_product"'.format(config.DB_PREFIX)
DB_PRODUCT              = u'"{0}product"'.format(config.DB_PREFIX)
DB_SHOP                 = u'"{0}shop"'.format(config.DB_PREFIX)

from models import *

class layout:
    clean       = web.template.render(config.TEMPLATES_DIR)
    standard    = web.template.render(config.TEMPLATES_DIR, base=u'standard_base')
    authorized  = web.template.render(config.TEMPLATES_DIR, base=u'authorized_base')
    modal       = web.template.render(config.TEMPLATES_DIR, base=u'modal_base')
    admin       = web.template.render(config.TEMPLATES_DIR, base=u'admin_base')

    @classmethod
    def get(cls):
        if session.user_id != None:
            return cls.authorized

        return cls.standard

web.template.Template.globals[u'time']       = time
web.template.Template.globals[u'web']        = web
web.template.Template.globals[u'web']        = web
web.template.Template.globals[u'get_url']    = get_url
web.template.Template.globals[u'session']    = session
web.template.Template.globals[u'config']     = config
web.template.Template.globals[u'layout']     = layout

from lib import *
from views import *

web.template.Template.globals[u'put_message']    = put_message
web.template.Template.globals[u'clear_messages'] = clear_messages
