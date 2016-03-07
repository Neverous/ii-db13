# coding: utf-8

from main import *

def placement_products_get(placement_id):
    return list(db.query(u'''
        SELECT DISTINCT placement_product.*, product.*
        FROM        {0} AS placement_product
            JOIN    {1} AS product  USING(product_id)
        WHERE placement_product.placement_id = $placement_id
        ORDER BY production_date ASC
        '''.format(DB_PLACEMENT_PRODUCT, DB_PRODUCT),
        vars={
            u'placement_id': placement_id
        }))
