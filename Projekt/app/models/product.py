# coding: utf-8

from main import *

def products_get():
    return db.select(DB_PRODUCT)

def admin_products_get():
    return list(db.query(u'''
        SELECT DISTINCT product.*, user.nick
        FROM        {0} AS product
            JOIN    {1} AS user USING(user_id)
        ORDER BY product.name ASC, product_id ASC
        '''.format(DB_PRODUCT, DB_USER)))

def product_get(product_id):
    result = list(db.select(DB_PRODUCT, {u'product_id': product_id}, where=u'product_id = $product_id', limit=1))
    if not result:
        return None

    return result[0]

def product_update(product_id, name):
    return db.update(DB_PRODUCT, vars={u'product_id': product_id}, where=u'product_id = $product_id', name=name)

def product_remove(product_id):
    return db.delete(DB_PRODUCT, vars={u'product_id': product_id}, where=u'product_id = $product_id')

def product_add(user_id, product_name):
    return db.insert(DB_PRODUCT, user_id=user_id, name=product_name)

def produce_product(user_id, placement_id, placement_name, product_id, product_name, product_count):
    #with db.transaction():
    if True: # sqlite doesnt support nested transaction resulting in infinite recursion
        from product import product_get
        product = product_get(product_id)
        if not product or product.name.lower() != product_name.lower():
            product_id = -1

        if product_id == -1:
            product_id = db.insert(DB_PRODUCT, user_id=user_id, name=product_name)

        from warehouse_product import warehouse_product_add
        warehouse_product_add(user_id, product_id, product_name, placement_id, None, None, None, u'Produkcja z {0}'.format(placement_name), None, product_count)
        return db.insert(DB_PLACEMENT_PRODUCT, placement_id=placement_id, product_id=product_id, count=product_count)
