# coding: utf-8

from main       import *
from views.user import nick_validate, nick_exists, name_validate, surname_validate, email_validate, email_exists

from models.user                import *
from models.garden              import *
from models.placement           import *
from models.plant               import *
from models.product             import *
from models.shop                import *
from models.warehouse_product   import *
from models.event               import *

class admin_users_view:
    @check_admin(get_url(u'index_view'))
    def GET(self):
        generate_token()
        users = admin_users_get()
        return layout.admin.admin_users(users)

    def POST(self):
        req = web.input(action=u'', nick=u'', password=u'', email=u'', name=u'', surname=u'', token=u'')
        req.nick    = req.nick.strip()
        req.name    = req.name.strip()
        req.surname = req.surname.strip()
        req.email   = req.email.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_users_view'))

        if req.action != u'add':
            put_message(u'danger', u'Niepoprawna akcja')

        elif not nick_validate(req.nick):
            put_message(u'danger', u'Niepoprawny login!')

        elif nick_exists(req.nick):
            put_message(u'danger', u'Nick już zajęty!')

        elif not req.password:
            put_message(u'danger', u'Hasło nie może być puste!')

        elif not email_validate(req.email):
            put_message(u'danger', u'Ten adres e-mail jest niepoprawny!')

        elif email_exists(req.email):
            put_message(u'danger', u'Ten adres e-mail już istnieje w bazie danych!')

        elif not name_validate(req.name) or not surname_validate(req.surname):
            put_message(u'danger', u'Niepoprawne imię lub nazwisko')

        else:
            user = user_register(req.nick, req.name, req.surname, req.password, req.email)

            if user:
                put_message(u'success', u'Dodano użytkownika!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        return web.seeother(get_url('admin_users_view'))

class admin_user_view:
    @check_admin(get_url(u'index_view'))
    def GET(self, user_id):
        user = user_get(user_id)
        if not user:
            return web.notfound()

        generate_token()
        return layout.modal.admin_user(user.nick, user.email, user.name, user.surname)

    @check_admin(get_url(u'index_view'))
    def POST(self, user_id):
        user = user_get(int(user_id or 0))
        if not user:
            return web.notfound()

        req = web.input(action=u'', password=u'', email=u'', name=u'', surname=u'', token=u'')
        req.name    = req.name.strip()
        req.surname = req.surname.strip()
        req.email   = req.email.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_user_view', user.user_id))

        if req.action == u'impersonate':
            session.user_id = user.user_id
            put_message(u'success', u'Przełączono na użytkownika {0}!'.format(user.nick))
            return web.seeother(get_url('index_view'))

        elif req.action == u'remove':
            if session.user_id == user.user_id:
                session.user_id = session.admin_id

            if user.user_id > 1 and user_remove(user.user_id):
                put_message(u'success', u'Usunięto użytkownika!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

            return web.seeother(get_url('admin_users_view'))

        elif req.action == u'edit':
            if req.email and not email_validate(req.email):
                put_message(u'danger', u'Ten adres e-mail jest niepoprawny!')

            elif req.email and email_exists(req.email, user.user_id):
                put_message(u'danger', u'Ten adres e-mail już istnieje w bazie danych!')

            elif not name_validate(req.name) or not surname_validate(req.surname):
                put_message(u'danger', u'Niepoprawne imię lub nazwisko')

            else:
                if user_update(user.user_id, req.password, req.email, req.name, req.surname):
                    put_message(u'success', u'Zapisano dane!')

                else:
                    put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        else:
            put_message(u'danger', u'Niepoprawna akcja')

        generate_token()
        return layout.modal.admin_user(user.nick, req.email, req.name, req.surname)

class admin_gardens_view:
    @check_admin(get_url(u'index_view'))
    def GET(self):
        generate_token()
        gardens = admin_gardens_get()
        return layout.admin.admin_gardens(gardens)

    POST = GET

class admin_garden_view:
    @check_admin(get_url(u'index_view'))
    def GET(self, garden_id):
        garden = garden_get1(int(garden_id or 0))
        if not garden:
            return web.notfound()

        generate_token()
        return layout.modal.admin_garden(garden.name)

    @check_admin(get_url(u'index_view'))
    def POST(self, garden_id):
        garden = garden_get1(int(garden_id or 0))
        if not garden:
            return web.notfound()

        req = web.input(action=u'', name=u'')
        req.name    = req.name.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_garden_view', garden.garden_id))

        if req.action == u'remove':
            if garden_remove(garden.user_id, garden.garden_id):
                put_message(u'success', u'Usunięto ogród!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

            return web.seeother(get_url('admin_gardens_view'))

        elif req.action == u'edit':
            if not name_validate(req.name):
                put_message(u'danger', u'Niepoprawna nazwa')

            else:
                if garden_update(garden.garden_id, req.name):
                    put_message(u'success', u'Zapisano dane!')

                else:
                    put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        else:
            put_message(u'danger', u'Niepoprawna akcja')

        generate_token()
        return layout.modal.admin_garden(req.name)

class admin_placements_view:
    @check_admin(get_url(u'index_view'))
    def GET(self):
        generate_token()
        placements = admin_placements_get()
        return layout.admin.admin_placements(placements)

    POST = GET

class admin_placement_view:
    @check_admin(get_url(u'index_view'))
    def GET(self, placement_id):
        placement = placement_get1(int(placement_id or 0))
        if not placement:
            return web.notfound()

        generate_token()
        return layout.modal.admin_placement(placement.name, placement.comment)

    @check_admin(get_url(u'index_view'))
    def POST(self, placement_id):
        placement = placement_get1(int(placement_id or 0))
        if not placement:
            return web.notfound()

        req = web.input(action=u'', name=u'', comment=u'')
        req.name    = req.name.strip()
        req.comment = req.comment.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_placement_view', placement.placement_id))

        if req.action == u'remove':
            if placement_remove(placement.placement_id):
                put_message(u'success', u'Usunięto uprawę!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

            return web.seeother(get_url('admin_placements_view'))

        elif req.action == u'edit':
            if not name_validate(req.name):
                put_message(u'danger', u'Niepoprawna nazwa')

            else:
                if placement_update(placement.placement_id, name=req.name, comment=req.comment):
                    put_message(u'success', u'Zapisano dane!')

                else:
                    put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        else:
            put_message(u'danger', u'Niepoprawna akcja')

        generate_token()
        return layout.modal.admin_placement(req.name, req.comment)

class admin_events_view:
    @check_admin(get_url(u'index_view'))
    def GET(self):
        generate_token()
        events = admin_events_get()
        return layout.admin.admin_events(events)

    POST = GET

class admin_event_view:
    @check_admin(get_url(u'index_view'))
    def GET(self, event_id):
        event = event_get1(int(event_id or 0))
        if not event:
            return web.notfound()

        generate_token()
        return layout.modal.admin_event(event.name, event.description)

    @check_admin(get_url(u'index_view'))
    def POST(self, event_id):
        event = event_get1(int(event_id or 0))
        if not event:
            return web.notfound()

        req = web.input(action=u'', name=u'', description=u'')
        req.name    = req.name.strip()
        req.description = req.description.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_event_view', event.event_id))

        if req.action == u'remove':
            if event_remove(event.event_id):
                put_message(u'success', u'Usunięto zabieg!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

            return web.seeother(get_url('admin_events_view'))

        elif req.action == u'edit':
            if not name_validate(req.name):
                put_message(u'danger', u'Niepoprawna nazwa')

            else:
                if event_update(event.event_id, name=req.name, description=req.description):
                    put_message(u'success', u'Zapisano dane!')

                else:
                    put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        else:
            put_message(u'danger', u'Niepoprawna akcja')

        generate_token()
        return layout.modal.admin_event(req.name, req.description)

class admin_plants_view:
    @check_admin(get_url(u'index_view'))
    def GET(self):
        generate_token()
        plants = admin_plants_get()
        return layout.admin.admin_plants(plants)

    @check_admin(get_url(u'index_view'))
    def POST(self):
        req = web.input(action=u'', name=u'')
        req.name    = req.name.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_plants_view'))

        if req.action != u'add':
            put_message(u'danger', u'Niepoprawna akcja')

        elif not name_validate(req.name):
            put_message(u'danger', u'Niepoprawna nazwa')

        else:
            if plant_add(session.admin_id, req.name):
                put_message(u'success', u'Dodano roślinę!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        return web.seeother(get_url('admin_plants_view'))

class admin_plant_view:
    @check_admin(get_url(u'index_view'))
    def GET(self, plant_id):
        plant = plant_get(int(plant_id or 0))
        if not plant:
            return web.notfound()

        generate_token()
        return layout.modal.admin_plant(plant.name)

    @check_admin(get_url(u'index_view'))
    def POST(self, plant_id):
        plant = plant_get(int(plant_id or 0))
        if not plant:
            return web.notfound()

        req = web.input(action=u'', name=u'')
        req.name    = req.name.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_plant_view', plant.plant_id))

        if req.action == u'remove':
            if plant_remove(plant.plant_id):
                put_message(u'success', u'Usunięto roślinę!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

            return web.seeother(get_url('admin_plants_view'))

        elif req.action == u'edit':
            if not name_validate(req.name):
                put_message(u'danger', u'Niepoprawna nazwa')

            else:
                if plant_update(plant.plant_id, req.name):
                    put_message(u'success', u'Zapisano dane!')

                else:
                    put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        else:
            put_message(u'danger', u'Niepoprawna akcja')

        generate_token()
        return layout.modal.admin_plant(req.name)

class admin_products_view:
    @check_admin(get_url(u'index_view'))
    def GET(self):
        generate_token()
        products = admin_products_get()
        return layout.admin.admin_products(products)

    @check_admin(get_url(u'index_view'))
    def POST(self):
        req = web.input(action=u'', name=u'')
        req.name    = req.name.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_plants_view'))

        if req.action != u'add':
            put_message(u'danger', u'Niepoprawna akcja')

        elif not name_validate(req.name):
            put_message(u'danger', u'Niepoprawna nazwa')

        else:
            if product_add(session.admin_id, req.name):
                put_message(u'success', u'Dodano produkt!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        return web.seeother(get_url('admin_products_view'))

class admin_product_view:
    @check_admin(get_url(u'index_view'))
    def GET(self, product_id):
        product = product_get(int(product_id or 0))
        if not product:
            return web.notgound()

        generate_token()
        return layout.modal.admin_product(product.name)

    @check_admin(get_url(u'index_view'))
    def POST(self, product_id):
        product = product_get(int(product_id or 0))
        if not product:
            return web.notgound()

        req = web.input(action=u'', name=u'')
        req.name    = req.name.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_product_view', product.product_id))

        if req.action == u'remove':
            if product_remove(product.product_id):
                put_message(u'success', u'Usunięto produkt!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

            return web.seeother(get_url('admin_products_view'))

        elif req.action == u'edit':
            if not name_validate(req.name):
                put_message(u'danger', u'Niepoprawna nazwa')

            else:
                if product_update(product.product_id, req.name):
                    put_message(u'success', u'Zapisano dane!')

                else:
                    put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        else:
            put_message(u'danger', u'Niepoprawna akcja')

        generate_token()
        return layout.modal.admin_product(req.name)

class admin_shops_view:
    @check_admin(get_url(u'index_view'))
    def GET(self):
        generate_token()
        shops = admin_shops_get()
        return layout.admin.admin_shops(shops)

    @check_admin(get_url(u'index_view'))
    def POST(self):
        req = web.input(action=u'', name=u'', address=u'')
        req.name    = req.name.strip()
        req.address = req.address.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_shops_view'))

        if req.action != u'add':
            put_message(u'danger', u'Niepoprawna akcja')

        elif not name_validate(req.name):
            put_message(u'danger', u'Niepoprawna nazwa')

        else:
            if shop_add(session.admin_id, req.name, req.address):
                put_message(u'success', u'Dodano sklep!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        return web.seeother(get_url('admin_shops_view'))

class admin_shop_view:
    @check_admin(get_url(u'index_view'))
    def GET(self, shop_id):
        shop = shop_get(int(shop_id or 0))
        if not shop:
            return web.notfound()

        generate_token()
        return layout.modal.admin_shop(shop.name, shop.address)

    @check_admin(get_url(u'index_view'))
    def POST(self, shop_id):
        shop = shop_get(int(shop_id or 0))
        if not shop:
            return web.notfound()

        req = web.input(action=u'', name=u'', address=u'')
        req.name    = req.name.strip()
        req.address = req.address.strip()

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_shop_view', shop.shop_id))

        if req.action == u'remove':
            if shop_remove(shop.shop_id):
                put_message(u'success', u'Usunięto sklep!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

            return web.seeother(get_url('admin_shops_view'))

        elif req.action == u'edit':
            if not name_validate(req.name):
                put_message(u'danger', u'Niepoprawna nazwa')

            else:
                if shop_update(shop.shop_id, req.name, req.address):
                    put_message(u'success', u'Zapisano dane!')

                else:
                    put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        else:
            put_message(u'danger', u'Niepoprawna akcja')

        generate_token()
        return layout.modal.admin_shop(req.name, req.address)

class admin_warehouse_products_view:
    @check_admin(get_url(u'index_view'))
    def GET(self):
        generate_token()
        warehouse_products = admin_warehouse_products_get()
        return layout.admin.admin_warehouse_products(warehouse_products)

    POST = GET

class admin_warehouse_product_view:
    @check_admin(get_url(u'index_view'))
    def GET(self, warehouse_id):
        warehouse_product = warehouse_product_get(int(warehouse_id or 0))
        if not warehouse_product:
            return web.notfound()

        generate_token()
        return layout.modal.admin_warehouse_product(warehouse_product.comment, warehouse_product.count, warehouse_product.price)

    @check_admin(get_url(u'index_view'))
    def POST(self, warehouse_id):
        warehouse_product = warehouse_product_get(int(warehouse_id or 0))
        if not warehouse_product:
            return web.notfound()

        req = web.input(action=u'', comment=u'', count=0, price=0)
        req.comment = req.comment.strip()
        req.count   = int(req.count or 0)
        req.price   = float(req.price or 0)

        if not check_token(req.token):
            return web.seeother(get_url(u'admin_warehouse_product_view', warehouse_product.warehouse_product_id))

        if req.action == u'remove':
            if warehouse_product_remove(warehouse_product.warehouse_product_id):
                put_message(u'success', u'Usunięto produkt z magazynu!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

            return web.seeother(get_url('admin_warehouse_products_view'))

        elif req.action == u'edit':
            if warehouse_product_update(warehouse_product.warehouse_product_id, req.comment, req.count, req.price):
                put_message(u'success', u'Zapisano dane!')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')

        else:
            put_message(u'danger', u'Niepoprawna akcja')

        generate_token()
        return layout.modal.admin_warehouse_product(req.comment, req.count, req.price)
