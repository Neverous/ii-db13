# coding: utf-8

import re
from datetime import datetime, timedelta

from main import *

from models.garden              import *
from models.field               import *
from models.product             import *
from models.placement           import *
from models.placement_product   import *
from models.plant               import *
from models.event               import *

def name_validate(name):
    return re.match(r'[\w ]+', name, re.UNICODE)

class gardens_view:
    @check_logged(get_url(u'index_view'))
    def GET(self):
        generate_token()
        gardens = gardens_get(session.user_id)
        return layout.get().gardens(gardens)

    @check_logged(get_url(u'index_view'))
    def POST(self):
        req = web.input(actio=u'', garden_id=-1, token=u'')
        req.action      = req.action.strip()
        req.garden_id   = int(req.garden_id.strip() or 0)

        if not check_token(req.token):
            return web.seeother(get_url(u'gardens_view'))

        if req.action == u'remove':
            garden = garden_remove(session.user_id, req.garden_id)
            if garden:
                put_message(u'success', u'Ogród został usunięty.')

            else:
                put_message(u'danger', u'Nie udało się usunąć ogrodu!')

            return web.seeother(get_url(u'gardens_view'))

        put_message(u'danger', u'Niepoprawna akcja!')
        return web.seeother(get_url(u'gardens_view'))

class garden_add_view:
    @check_logged(get_url(u'index_view'))
    def GET(self):
        generate_token()
        return layout.get().garden_add(web.input(name=u'').name.strip())

    @check_logged(get_url(u'index_view'))
    def POST(self):
        req = web.input(name=u'', fields=[], token=u'')
        req.name    = req.name.strip()
        req.fields  = tuple(sorted(map(lambda x: tuple(map(int, x.split(u','))), req.fields), key=lambda x: (-x[0], x[1])))
        movY        = int((max([y for y, _ in req.fields] or [0]) + min([y for y, _ in req.fields] or [0])) / 2)
        movX        = int((max([x for _, x in req.fields] or [0]) + min([x for _, x in req.fields] or [0])) / 2)
        req.fields  = tuple(map(lambda (y, x): (y - movY, x - movX), req.fields))

        if not check_token(req.token):
            return web.seeother(get_url(u'garden_add_view'))

        success = True
        if not req.fields:
            success = False

        elif not name_validate(req.name):
            put_message(u'danger', u'Niepoprawna nazwa ogrodu!')
            success = False

        else:
            garden = garden_add(session.user_id, req.name, req.fields)
            if garden:
                put_message(u'success', u'Ogród został dodany!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        if success:
            return web.seeother(get_url(u'gardens_view'))

        generate_token()
        return layout.get().garden_add(req.name, req.fields)

class garden_thumbnail_view:
    @check_logged(get_url(u'static_view', u'not_found'))
    def GET(self, garden_id):
        garden      = garden_get2(session.user_id, int(garden_id or 0))
        if not garden:
            return web.notfound()

        fields = fields_get(session.user_id, garden.garden_id)
        if not fields:
            return web.notfound()

        web.header(u'Content-Type', u'image/svg+xml')
        return layout.clean.garden_thumbnail(garden.garden_id, fields)

    POST = GET

class garden_view:
    @check_logged(get_url(u'index_view'))
    def GET(self, garden_id):
        garden      = garden_get2(session.user_id, int(garden_id or 0))
        if not garden:
            return web.notfound()

        req = web.input(current_start=datetime.now().strftime(u'%Y-%m-%d'), current_end=(datetime.now().date() + timedelta(1000*360)).strftime(u'%Y-%m-%d'))

        fields = fields_data_get(session.user_id, garden.garden_id, req.current_start, req.current_end)
        if not fields:
            return web.notfound()

        generate_token()
        from views.event import events_data_get
        placements = placements_data_get(session.user_id, garden.garden_id, req.current_start, req.current_end)
        events = events_data_get(session.user_id, garden.garden_id, req.current_start, req.current_end)
        plants      = plants_get()
        return layout.get().garden(req.current_start, req.current_end, garden.name, fields, placements, events, plants, placement_date=datetime.now().date())

    @check_logged(get_url(u'index_view'))
    def POST(self, garden_id):
        garden      = garden_get2(session.user_id, int(garden_id or 0))
        if not garden:
            return web.notfound()

        req = web.input(token=u'', selected_fields=u'', plant_id=-1, plant_name=u'', placement_name=u'', placement_comment=u'', palcement_date=u'', current_start=datetime.now().strftime(u'%Y-%m-%d'), current_end=(datetime.now().date() + timedelta(1000*360)).strftime(u'%Y-%m-%d'))
        req.selected_fields     = req.selected_fields.strip()
        if req.selected_fields:
            req.selected_fields     = tuple(map(int, req.selected_fields[:-1].split(u',')))

        req.plant_id            = int(req.plant_id or -1)
        req.plant_name          = req.plant_name.strip()
        req.placement_name      = req.placement_name.strip()
        req.placement_comment   = req.placement_comment.strip()
        req.placement_date      = datetime.strptime(req.placement_date.strip() or unicode(datetime.now()), u'%Y-%m-%d').date()

        if not check_token(req.token):
            return web.seeother(get_url(u'garden_view', garden_id))

        success = True
        if not name_validate(req.placement_name):
            put_message(u'danger', u'Nieprawidłowa nazwa posadzenia!')
            success = False

        elif not req.selected_fields:
            put_message(u'danger', u'Wybierz jakieś pola!')
            success = False

        else:
            placement = placement_add(session.user_id, req.plant_id, req.plant_name, req.placement_name, req.placement_comment, req.placement_date, req.selected_fields)
            if placement:
                put_message(u'success', u'Posadzono roślinę.')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        if success:
            return web.seeother(get_url(u'garden_view', garden_id))

        fields = fields_data_get(session.user_id, garden.garden_id, req.current_start, req.current_end)
        if not fields:
            return web.notfound()

        generate_token()
        from views.event import events_data_get
        placements = placements_data_get(session.user_id, garden.garden_id, req.current_start, req.current_end)
        events = events_data_get(session.user_id, garden.garden_id, req.current_start, req.current_end)
        plants      = plants_get()
        return layout.get().garden(req.current_start, req.current_end, garden.name, fields, placements, events, plants, u';'.join(map(lambda x: u','.join(x), req.selected_fields)), req.plant_id, req.plant_name, req.placement_name, req.placement_comment, req.placement_date)

class placement_view:
    @check_logged(get_url(u'index_view'))
    def GET(self, placement_id):
        placement   = placement_get2(session.user_id, int(placement_id or 0))
        if not placement:
            return web.notfound()

        generate_token()
        products            = products_get()
        placement_products  = placement_products_get(placement.placement_id)
        placement_events    = placement_events_get(session.user_id, placement.placement_id)
        return layout.modal.placement(products, placement_products, placement_events, placement.placement_id, placement.name, placement.plant_name, placement.comment, placement.placement_date, placement.finish_date)

    @check_logged(get_url(u'index_view'))
    def POST(self, placement_id):
        placement   = placement_get2(session.user_id, int(placement_id or 0))
        if not placement:
            return web.notfound()

        req = web.input(token=u'', action=u'', placement_comment=u'', product_id=-1, product_name=u'', product_count=0, event_name=u'', event_description=u'', event_from_date=u'', event_to_date=u'', event_end_date=u'', event_frequency=u'')
        req.placement_comment   = req.placement_comment.strip()
        req.action              = req.action.strip()
        req.product_id          = int(req.product_id or -1)
        req.product_name        = req.product_name.strip()
        req.product_count       = int(req.product_count or 0)
        req.event_name          = req.event_name.strip()
        req.event_description   = req.event_description.strip()
        req.event_frequency     = int(req.event_frequency or 0)
        try:
            req.event_from_date = datetime.strptime(req.event_from_date.strip(), u'%Y-%m-%dT%H:%M')

        except ValueError:
            req.event_from_date = datetime.now()

        try:
            req.event_to_date   = datetime.strptime(req.event_to_date.strip(), u'%Y-%m-%dT%H:%M')

        except ValueError:
            req.event_to_date   = datetime.now()

        if req.event_frequency:
            req.event_end_date      = datetime.strptime(req.event_end_date.strip(), u'%Y-%m-%d')

        else:
            req.event_end_date = req.event_to_date

        if not check_token(req.token):
            return web.seeother(get_url(u'placement_view', placement.placement_id))

        success = True
        if req.action == u'finish':
            if placement_finish(placement.placement_id):
                put_message(u'success', u'Uprawa {0} zakończona.'.format(placement.name))

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        elif req.action == u'produce':
            if produce_product(session.user_id, placement.placement_id, placement.name, req.product_id, req.product_name, req.product_count):
                put_message(u'success', u'Dodano produkt')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        elif req.action == u'add_event':
            from event import event_add
            if event_add(placement.placement_id, req.event_name, req.event_description, req.event_from_date, req.event_to_date, req.event_end_date, req.event_frequency):
                put_message(u'success', u'Dodano zabieg')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        elif req.action == u'edit':
            if placement_update(placement_id, comment=req.placement_comment):
                put_message(u'success', u'Zaktualizowano uprawę.')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        else:
            success = False
            put_message(u'danger', u'Nieprawidłowa akcja!')

        if success:
            return web.seeother(get_url(u'placement_view', placement.placement_id))

        generate_token()
        from event import placement_events_get
        products            = products_get()
        placement_products  = placement_products_get(placement.placement_id)
        placement_events    = placement_events_get(session.user_id, placement.placement_id)
        return layout.modal.placement(products, placement_products, placement_events, placement.placement_id, placement.name, placement.plant_name, placement.comment, placement.placement_date, placement.finish_date)
