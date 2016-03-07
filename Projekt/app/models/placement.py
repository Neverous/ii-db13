# coding: utf-8

from datetime import datetime

from main import *

def admin_placements_get():
    return list(db.query(u'''
        SELECT DISTINCT placement.*, user.nick
        FROM        {0} AS placement
            JOIN    {1} AS placement_field  USING(placement_id)
            JOIN    {2} AS field            USING(field_id)
            JOIN    {3} AS garden           USING(garden_id)
            JOIN    {4} AS user             USING(user_id)
        ORDER BY user_id ASC, placement_id ASC
        '''.format(DB_PLACEMENT, DB_PLACEMENT_FIELD, DB_FIELD, DB_GARDEN, DB_USER)))

def placements_data_get(user_id, garden_id, from_date, to_date):
    return list(db.query(u'''
        SELECT DISTINCT placement.*, plant.name AS plant_name, plant.plant_id AS plant_id, (
            SELECT group_concat(y || ',' || x, ';')
            FROM        {3} AS placement_field
                JOIN    {1} AS field    USING(field_id)
            WHERE placement_id = placement.placement_id
        ) AS fields
        FROM        {2} AS placement
            JOIN    {4} AS plant            USING(plant_id)
            JOIN    {3} AS placement_field  USING(placement_id)
            JOIN    {1} AS field            USING(field_id)
            JOIN    {0} AS garden           USING(garden_id)
        WHERE   garden_id = $garden_id
            AND garden.user_id = $user_id
            AND (finish_date IS NULL OR date(finish_date) >= $from_date)
            AND date(placement_date) < $to_date
        ORDER BY placement.placement_id DESC;
        '''.format(DB_GARDEN, DB_FIELD, DB_PLACEMENT, DB_PLACEMENT_FIELD, DB_PLANT),
        vars={
            u'user_id':      user_id,
            u'garden_id':    garden_id,
            u'from_date':    from_date,
            u'to_date':      to_date,
        }))

def placement_get1(placement_id):
    result = list(db.select(DB_PLACEMENT, {u'placement_id': placement_id}, where=u'placement_id = $placement_id', limit=1))
    if not result:
        return None

    return result[0]

def placement_get2(user_id, placement_id):
    result = list(db.query(u'''
        SELECT DISTINCT placement.*, plant.name AS plant_name
        FROM        {0} AS placement
            JOIN    {1} AS placement_field  USING(placement_id)
            JOIN    {2} AS field            USING(field_id)
            JOIN    {3} AS garden           USING(garden_id)
            JOIN    {4} AS plant            USING(plant_id)
        WHERE   placement_id = $placement_id
            AND garden.user_id = $user_id
        ORDER BY placement_id DESC
        LIMIT 1;
        '''.format(DB_PLACEMENT, DB_PLACEMENT_FIELD, DB_FIELD, DB_GARDEN, DB_PLANT),
        vars={
            u'user_id':      user_id,
            u'placement_id': placement_id,
        }))

    if not result:
        return None

    return result[0]

def placement_add(user_id, plant_id, plant_name, placement_name, placement_comment, placement_date, selected_fields):
    from plant import plant_get
    with db.transaction():
        plant = plant_get(plant_id)
        if not plant or plant.name.lower() != plant_name.lower():
            plant_id = -1

        if plant_id == -1:
            plant_id = db.insert(DB_PLANT, user_id=user_id, name=plant_name)

        placement_id = db.insert(DB_PLACEMENT, plant_id=plant_id, name=placement_name, comment=placement_comment, placement_date=placement_date)
        for field in selected_fields:
            db.insert(DB_PLACEMENT_FIELD, placement_id=placement_id, field_id=field)

        return placement_id

def placement_update(placement_id, **kwargs):
    return db.update(DB_PLACEMENT, vars={u'placement_id': placement_id}, where=u'placement_id = $placement_id AND finish_date IS NULL', **kwargs)

def placement_finish(placement_id):
    return placement_update(placement_id, finish_date=datetime.now())

def placement_remove(placement_id):
    return db.delete(DB_PLACEMENT, vars={u'placement_id': placement_id}, where=u'placement_id = $placement_id')
