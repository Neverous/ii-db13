# coding: utf-8

from copy import copy
import time
from datetime import datetime, timedelta

from main import *

def events_get1(user_id):
    return list(db.query(u'''
        SELECT DISTINCT event.*
        FROM        {0} AS event
            JOIN    {1} AS placement_field  USING(placement_id)
            JOIN    {2} AS field            USING(field_id)
            JOIN    {3} AS garden           USING(garden_id)
        WHERE   garden.user_id = $user_id
        ORDER BY event.event_id DESC;
        '''.format(DB_EVENT, DB_PLACEMENT_FIELD, DB_FIELD, DB_GARDEN),
        vars={
            u'user_id':      user_id,
        }))

def events_get2(user_id, garden_id):
    return list(db.query(u'''
        SELECT DISTINCT event.*
        FROM        {0} AS event
            JOIN    {1} AS placement_field  USING(placement_id)
            JOIN    {2} AS field            USING(field_id)
            JOIN    {3} AS garden           USING(garden_id)
        WHERE   garden.user_id = $user_id
            AND garden.garden_id = $garden_id
        ORDER BY event.event_id DESC;
        '''.format(DB_EVENT, DB_PLACEMENT_FIELD, DB_FIELD, DB_GARDEN),
        vars={
            u'garden_id':    garden_id,
            u'user_id':      user_id,
        }))

def placement_events_get(user_id, placement_id):
    return list(db.query(u'''
        SELECT DISTINCT event.*
        FROM        {0} AS event
            JOIN    {1} AS placement_field  USING(placement_id)
            JOIN    {2} AS field            USING(field_id)
            JOIN    {3} AS garden           USING(garden_id)
        WHERE   garden.user_id = $user_id
            AND placement_id = $placement_id
        ORDER BY event.event_id DESC;
        '''.format(DB_EVENT, DB_PLACEMENT_FIELD, DB_FIELD, DB_GARDEN),
        vars={
            u'placement_id': placement_id,
            u'user_id':      user_id,
        }))

def events_calendar_get(user_id, from_date, to_date):
    events = []
    for event in db.query(u'''
        SELECT DISTINCT event.*, (
            SELECT COUNT(*) FROM (
                SELECT DISTINCT product_id
                FROM    {4} AS event_requirement
                WHERE event_id = event.event_id
                EXCEPT
                SELECT DISTINCT product_id
                FROM    {5} AS warehouse
                WHERE warehouse.user_id = $user_id
            )
        ) AS needed
        FROM        {0} AS event
            JOIN    {1} AS placement_field  USING(placement_id)
            JOIN    {2} AS field            USING(field_id)
            JOIN    {3} AS garden           USING(garden_id)
        WHERE   garden.user_id = $user_id
            AND event.from_date < $to_date AND event.end_date > $from_date
        ORDER BY event.event_id DESC;
        '''.format(DB_EVENT, DB_PLACEMENT_FIELD, DB_FIELD, DB_GARDEN, DB_EVENT_REQUIREMENT, DB_WAREHOUSE),
        vars={
            u'user_id':      user_id,
            u'from_date':    from_date.strftime(u'%Y-%m-%d %H:%M'),
            u'to_date':      to_date.strftime(u'%Y-%m-%d %H:%M'),
        }):
        ev = web.storage()
        ev.event_id     = event.event_id
        ev.name         = event.name
        ev.description  = event.description
        ev.start        = event.from_date
        ev.end          = event.to_date
        ev.ok           = event.needed == 0
        if event.frequency:
            delta = timedelta(weeks=event.frequency)
            while ev.start < to_date and ev.start < event.end_date:
                _ev = copy(ev)
                _ev.start   = time.mktime(_ev.start.timetuple()) * 1000
                _ev.end     = time.mktime(_ev.end.timetuple()) * 1000

                events.append(_ev)
                ev.start    += delta
                ev.end      += delta

        else:
            ev.start    = time.mktime(ev.start.timetuple()) * 1000
            ev.end      = time.mktime(ev.end.timetuple()) * 1000
            events.append(ev)

    return events

def events_data_get(user_id, garden_id, from_date, to_date):
    return list(db.query(u'''
        SELECT DISTINCT event.*, placement.name as placement_name, (
            SELECT group_concat(y || ',' || x, ';')
            FROM        {3} AS placement_field
                JOIN    {1} AS field        USING(field_id)
                JOIN    {2} AS placement    USING(placement_id)
            WHERE   placement_id = event.placement_id
                AND (finish_date IS NULL OR date(finish_date) >= $from_date)
                AND date(placement_date) < $to_date
        ) AS fields
        FROM        {4} AS event
            JOIN    {2} AS placement        USING(placement_id)
            JOIN    {3} AS placement_field  USING(placement_id)
            JOIN    {1} AS field            USING(field_id)
            JOIN    {0} AS garden           USING(garden_id)
        WHERE   garden_id = $garden_id
            AND garden.user_id = $user_id
            AND (finish_date IS NULL OR date(finish_date) >= $from_date)
            AND date(placement_date) < $to_date
        ORDER BY event.event_id DESC;
        '''.format(DB_GARDEN, DB_FIELD, DB_PLACEMENT, DB_PLACEMENT_FIELD, DB_EVENT),
        vars={
            u'user_id':      user_id,
            u'garden_id':    garden_id,
            u'from_date':    from_date,
            u'to_date':      to_date,
        }))

def event_get1(event_id):
    result = list(db.select(DB_EVENT, {u'event_id': event_id}, where=u'event_id = $event_id', limit=1))
    if not result:
        return None

    return result[0]

def event_get2(user_id, event_id):
    result = list(db.query(u'''
        SELECT DISTINCT event.*, placement.name AS placement_name, plant.name AS plant_name
        FROM        {0} AS event
            JOIN    {1} AS placement_field  USING(placement_id)
            JOIN    {5} AS placement        USING(placement_id)
            JOIN    {2} AS field            USING(field_id)
            JOIN    {3} AS garden           USING(garden_id)
            JOIN    {4} AS plant            USING(plant_id)
        WHERE   garden.user_id = $user_id
            AND event.event_id = $event_id
        LIMIT 1;
        '''.format(DB_EVENT, DB_PLACEMENT_FIELD, DB_FIELD, DB_GARDEN, DB_PLANT, DB_PLACEMENT),
        vars={
            u'user_id':  user_id,
            u'event_id': event_id,
        }))

    if not result:
        return None

    return result[0]

def event_add(placement_id, name, description, from_date, to_date, end_date, frequency):
    return db.insert(DB_EVENT, placement_id=placement_id, name=name, description=description, from_date=from_date, to_date=to_date, end_date=end_date, frequency=frequency)

def event_update(event_id, **kwargs):
    return db.update(DB_EVENT, vars={u'event_id': event_id}, where=u'event_id = $event_id', **kwargs)

def event_remove(event_id):
    return db.delete(DB_EVENT, vars={u'event_id': event_id}, where=u'event_id = $event_id')

def admin_events_get():
    return list(db.query(u'''
        SELECT DISTINCT event.*, user.nick
        FROM        {0} AS event
            JOIN    {1} AS placement_field  USING(placement_id)
            JOIN    {2} AS field            USING(field_id)
            JOIN    {3} AS garden           USING(garden_id)
            JOIN    {4} AS user             USING(user_id)
        ORDER BY user_id ASC, event_id ASC
        '''.format(DB_EVENT, DB_PLACEMENT_FIELD, DB_FIELD, DB_GARDEN, DB_USER)))
