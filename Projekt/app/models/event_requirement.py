# coding: utf-8

from main import *

def event_requirements_get(user_id, event_id):
    return list(db.query(u'''
        SELECT DISTINCT product.*, (
            SELECT SUM(warehouse.count)
            FROM    {0} AS warehouse
            WHERE   warehouse.user_id = $user_id
                AND warehouse.product_id = product.product_id
        ) AS available
        FROM        {1} AS event
            JOIN    {2} AS event_requirement    USING(event_id)
            JOIN    {3} AS product              USING(product_id)
            JOIN    {4} AS placement            USING(placement_id)
            JOIN    {5} AS placement_field      USING(placement_id)
            JOIN    {6} AS field                USING(field_id)
            JOIN    {7} AS garden               USING(garden_id)
        WHERE   event.event_id = $event_id
            AND garden.user_id = $user_id
        ORDER BY product_id ASC;
        '''.format(DB_WAREHOUSE, DB_EVENT, DB_EVENT_REQUIREMENT, DB_PRODUCT, DB_PLACEMENT, DB_PLACEMENT_FIELD, DB_FIELD, DB_GARDEN),
        vars={
            u'user_id':  user_id,
            u'event_id': event_id,
        }))

def event_requirement_add(user_id, event_id, product_id, product_name):
    from product import product_get
    with db.transaction():
        product = product_get(product_id)
        if not product or product.name.lower() != product_name.lower():
            product_id = -1

        if product_id == -1:
            product_id = db.insert(DB_PRODUCT, user_id=user_id, name=product_name)

        return db.insert(DB_EVENT_REQUIREMENT, event_id=event_id, product_id=product_id)

def event_requirement_remove(event_id, product_id):
    return db.delete(DB_EVENT_REQUIREMENT, vars={u'event_id': event_id, u'product_id': product_id}, where=u'event_id = $event_id AND product_id = $product_id')

