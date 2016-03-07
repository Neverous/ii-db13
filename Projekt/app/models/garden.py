# coding: utf-8

from main import *

def admin_gardens_get():
    return list(db.query(u'''
        SELECT DISTINCT garden.*, user.nick
        FROM        {0} AS garden
            JOIN    {1} AS user     USING(user_id)
        ORDER BY user_id ASC, garden_id ASC
        '''.format(DB_GARDEN, DB_USER)))

def gardens_get(user_id):
    return list(db.select(DB_GARDEN, {u'user_id': user_id}, where=u'user_id = $user_id', order=u'creation_date DESC'))

def garden_get2(user_id, garden_id):
    result = list(db.select(DB_GARDEN, {u'user_id': user_id, u'garden_id': garden_id}, where=u'user_id = $user_id AND garden_id = $garden_id', limit=1))
    if not result:
        return None

    return result[0]

def garden_get1(garden_id):
    result = list(db.select(DB_GARDEN, {u'garden_id': garden_id}, where=u'garden_id = $garden_id', limit=1))
    if not result:
        return None

    return result[0]

def garden_add(user_id, name, fields):
    with db.transaction():
        garden_id   = db.insert(DB_GARDEN, user_id=user_id, name=name)
        for (y, x) in fields:
            db.insert(DB_FIELD, garden_id=garden_id, x=x, y=y)

        return garden_id

def garden_remove(user_id, garden_id):
    return db.delete(DB_GARDEN, vars={u'user_id': user_id, u'garden_id': garden_id}, where=u'user_id = $user_id AND garden_id = $garden_id')

def garden_update(garden_id, name):
    return db.update(DB_GARDEN, vars={u'garden_id': garden_id}, where=u'garden_id = $garden_id', name=name)
