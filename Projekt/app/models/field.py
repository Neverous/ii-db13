# coding: utf-8

from main import *

def fields_get(user_id, garden_id):
    return list(db.query(u'''
        SELECT DISTINCT field.*
        FROM        {0} AS field
            JOIN    {1} AS garden   USING(garden_id)
        WHERE   field.garden_id = $garden_id
            AND garden.user_id = $user_id
        ORDER BY y DESC, x ASC;
        '''.format(DB_FIELD, DB_GARDEN),
        vars={
            u'user_id':      user_id,
            u'garden_id':    garden_id,
        }))

def fields_data_get(user_id, garden_id, start_date, end_date):
    return list(db.query(u'''
        SELECT DISTINCT field.*, (
            SELECT group_concat(placement_id, ',')
            FROM        {2} AS placement_field
                JOIN    {1} AS placement    USING(placement_id)
            WHERE   field_id = field.field_id
                AND (finish_date IS NULL OR date(finish_date) >= $start_date)
                AND date(placement_date) < $end_date
        ) AS placements, (
            SELECT group_concat(event_id, ',')
            FROM        {3} AS event
                JOIN    {2} AS placement_field  USING(placement_id)
                JOIN    {1} AS placement        USING(placement_id)
            WHERE   field_id = field.field_id
                AND (finish_date IS NULL OR date(finish_date) >= $start_date)
                AND date(placement_date) < $end_date
        ) AS events
        FROM        {0} AS field
            JOIN    {4} AS garden   USING(garden_id)
        WHERE   field.garden_id = $garden_id
            AND garden.user_id = $user_id
        ORDER BY y DESC, x ASC;
        '''.format(DB_FIELD, DB_PLACEMENT, DB_PLACEMENT_FIELD, DB_EVENT, DB_GARDEN),
        vars={
            u'user_id':      user_id,
            u'garden_id':    garden_id,
            u'start_date':   start_date,
            u'end_date':     end_date,
        }))
