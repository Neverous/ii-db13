# coding: utf-8

from copy import copy
import time
from datetime import datetime, timedelta

from main import *

from models.event               import *
from models.placement           import *
from models.product             import *
from models.event_requirement   import *

class events_view:
    @check_logged(get_url(u'index_view'))
    def GET(self):
        generate_token()
        return layout.get().events()

class events_json_view:
    @check_logged(get_url(u'index_view'))
    def GET(self):
        req = web.input(**{u'from': None, u'to': None})
        if not req[u'from'] or not req.to:
            return web.notfound()

        events = events_calendar_get(
            session.user_id,
            datetime.fromtimestamp(int(req[u'from']) / 1000),
            datetime.fromtimestamp(int(req.to) / 1000))

        web.header(u'Content-Type', u'application/json')
        return layout.clean.events_json(events)

class event_view:
    @check_logged(get_url(u'index_view'))
    def GET(self, event_id):
        event = event_get2(session.user_id, int(event_id or 0))
        if not event:
            return web.notfound()

        generate_token()
        required_products   = event_requirements_get(session.user_id, event.event_id)
        products            = products_get()
        return layout.modal.event(products, event.event_id, event.name, event.description, event.from_date, event.to_date, event.end_date, event.frequency, event.placement_id, event.placement_name, event.plant_name, required_products)

    @check_logged(get_url(u'index_view'))
    def POST(self, event_id):
        event = event_get2(session.user_id, int(event_id or 0))
        if not event:
            return web.notfound()

        req = web.input(token=u'', action=u'', product_id=-1, product_name=u'', event_description=u'')
        req.action              = req.action.strip()
        req.product_id          = int(req.product_id or -1)
        req.product_name        = req.product_name.strip()
        req.event_description   = req.event_description.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'event_view', event.event_id))

        success = True
        if req.action == u'add_req':
            if not event_requirement_add(session.user_id, event.event_id, req.product_id, req.product_name):
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

            else:
                put_message(u'success', u'Dodano potrzebny produkt')

        elif req.action == u'rem_req':
            if not event_requirement_remove(event.event_id, req.product_id):
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

            else:
                put_message(u'success', u'Usunięto produkt')

        elif req.action == u'remove':
            if not event_remove(event.event_id):
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

            else:
                put_message(u'success', u'Usunięto zdarzenie<script>parent.location.reload();</script>')
                return web.seeother(get_url(u'empty_view'))

        elif req.action == u'edit':
            if event_update(event.event_id, description=req.event_description):
                put_message(u'success', u'Zaktualizowano zabieg.')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        else:
            success = False
            put_message(u'danger', u'Nieprawidłowa akcja!')

        if success:
            return web.seeother(get_url(u'event_view', event.event_id))

        generate_token()
        required_products   = event_requirements_get(session.user_id, event.event_id)
        products            = products_get()
        return layout.modal.event(products, event.event_id, event.name, event.description, event.from_date, event.to_date, event.end_date, event.frequency, event.placement_id, event.placement_name, event.plant_name, required_products)
