# coding: utf-8

from main import *

def plants_get():
    return list(db.select(DB_PLANT))

def admin_plants_get():
    return list(db.query(u'''
        SELECT DISTINCT plant.*, user.nick
        FROM        {0} AS plant
            JOIN    {1} AS user USING(user_id)
        ORDER BY plant.name ASC, plant_id ASC
        '''.format(DB_PLANT, DB_USER)))

def plant_get(plant_id):
    result = list(db.select(DB_PLANT, {u'plant_id': plant_id}, where=u'plant_id = $plant_id', limit=1))
    if not result:
        return None

    return result[0]

def plant_update(plant_id, name):
    return db.update(DB_PLANT, vars={u'plant_id': plant_id}, where=u'plant_id = $plant_id', name=name)

def plant_remove(plant_id):
    return db.delete(DB_PLANT, vars={u'plant_id': plant_id}, where=u'plant_id = $plant_id')

def plant_add(user_id, plant_name):
    return db.insert(DB_PLANT, user_id=user_id, name=plant_name)
