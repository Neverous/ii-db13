# coding: utf-8

from main import *

def admin_shops_get():
    return list(db.query(u'''
        SELECT DISTINCT shop.*, user.nick
        FROM        {0} AS shop
            JOIN    {1} AS user USING(user_id)
        ORDER BY shop.name ASC, shop_id ASC
        '''.format(DB_SHOP, DB_USER)))


def shops_get():
    return list(db.select(DB_SHOP))

def shop_get(shop_id):
    result = list(db.select(DB_SHOP, {u'shop_id': shop_id}, where=u'shop_id = $shop_id', limit=1))
    if not result:
        return None

    return result[0]

def shop_remove(shop_id):
    return db.delete(DB_SHOP, vars={u'shop_id': shop_id}, where=u'shop_id = $shop_id')

def shop_update(shop_id, name, address):
    return db.update(DB_SHOP, vars={u'shop_id': shop_id}, where=u'shop_id = $shop_id', name=name, address=address)

def shop_add(user_id, shop_name, shop_address):
    return db.insert(DB_SHOP, user_id=user_id, name=shop_name, address=shop_address)
