# coding: utf-8

from main import *

def admin_warehouse_products_get():
    return list(db.query(u'''
        SELECT DISTINCT warehouse_product.*, user.nick, product.name AS product_name, placement.name AS placement_name, shop.name || ', ' || shop.address AS shop_name_address
        FROM            {0} AS warehouse_product
            JOIN        {1} AS user         USING(user_id)
            JOIN        {4} AS product      USING(product_id)
            LEFT JOIN   {2} AS placement    USING(placement_id)
            LEFT JOIN   {3} AS shop         USING(shop_id)
        ORDER BY user_id ASC, warehouse_product_id ASC
        '''.format(DB_WAREHOUSE, DB_USER, DB_PLACEMENT, DB_SHOP, DB_PRODUCT)))

def warehouse_product_get(warehouse_product_id):
    result = list(db.select(DB_WAREHOUSE, vars={u'warehouse_product_id': warehouse_product_id}, where=u'warehouse_product_id = $warehouse_product_id'))

    if not result:
        return None

    return result[0]

def warehouse_products_table_get(user_id):
    products    = []
    prev_id     = None
    product     = None
    for warehouse_product in db.query(u'''
        SELECT DISTINCT warehouse.*, product.name AS product_name, shop.name AS shop_name, shop.address AS shop_address, plant.name AS plant_name
        FROM            {0} AS warehouse
            JOIN        {1} AS product      USING(product_id)
            LEFT JOIN   {2} AS placement    USING(placement_id)
            LEFT JOIN   {3} AS plant        USING(plant_id)
            LEFT JOIN   {4} AS shop         USING(shop_id)
        WHERE warehouse.user_id = $user_id
        ORDER BY product_id ASC, obtained_date ASC;
        '''.format(DB_WAREHOUSE, DB_PRODUCT, DB_PLACEMENT, DB_PLANT, DB_SHOP),
        vars={
            u'user_id': user_id,
        }):
        if prev_id != warehouse_product.product_id:
            prev_id = warehouse_product.product_id
            product = web.storage()
            product.product_id      = warehouse_product.product_id
            product.product_name    = warehouse_product.product_name
            product.count           = 0
            product.elements        = []
            products.append(product)

        element = web.storage()
        element.warehouse_product_id    = warehouse_product.warehouse_product_id
        element.obtained_date           = warehouse_product.obtained_date
        element.shop_id                 = warehouse_product.shop_id
        element.shop_name               = warehouse_product.shop_name
        element.shop_address            = warehouse_product.shop_address
        element.shop_price              = warehouse_product.price
        element.placement_id            = warehouse_product.placement_id
        element.plant_name              = warehouse_product.plant_name
        element.comment                 = warehouse_product.comment
        element.count                   = warehouse_product.count
        product.count                   += element.count
        product.elements.append(element)

    return products

def warehouse_product_add(user_id, product_id, product_name, placement_id, shop_id, shop_name, shop_address, comment, price, count):
    from product    import product_get
    from shop            import shop_get
    with db.transaction():
        product = product_get(product_id)
        if not product or product.name.lower() != product_name.lower():
            product_id = -1

        if product_id == -1:
            product_id = db.insert(DB_PRODUCT, user_id=user_id, name=product_name)

        if placement_id != -1:
            return db.insert(DB_WAREHOUSE, user_id=user_id, product_id=product_id, count=count, placement_id=placement_id, comment=comment)

        else:
            shop = shop_get(shop_id)
            if not shop or shop.name.lower() != shop_name.lower() or shop.address.lower() != shop_address.lower():
                shop_id = -1

            if shop_id == -1:
                shop_id = db.insert(DB_SHOP, user_id=user_id, name=shop_name, address=shop_address)

            return db.insert(DB_WAREHOUSE, user_id=user_id, product_id=product_id, count=count, shop_id=shop_id, comment=comment, price=price)

def warehouse_product_update(warehouse_product_id, comment, count, price):
    return db.update(DB_WAREHOUSE, vars={u'warehouse_product_id': warehouse_product_id}, where=u'warehouse_product_id = $warehouse_product_id', comment=comment, count=count, price=price)

def warehouse_product_remove(warehouse_product_id):
    return db.delete(DB_WAREHOUSE, vars={u'warehouse_product_id': warehouse_product_id}, where=u'warehouse_product_id = $warehouse_product_id')

def warehouse_update(user_id, products):
    with db.transaction():
        for (warehouse_product_id, count) in products:
            if count > 0:
                db.update(DB_WAREHOUSE, vars={u'user_id': user_id, u'warehouse_product_id': warehouse_product_id}, where=u'user_id = $user_id AND warehouse_product_id = $warehouse_product_id', count=count)

            else:
                db.delete(DB_WAREHOUSE, vars={u'user_id': user_id, u'warehouse_product_id': warehouse_product_id}, where=u'user_id = $user_id AND warehouse_product_id = $warehouse_product_id')

        return True

