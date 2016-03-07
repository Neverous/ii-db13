# coding: utf-8

from main import *

from models.warehouse_product   import *
from models.product             import *
from models.shop                import *

class warehouse_view:
    @check_logged(get_url(u'index_view'))
    def GET(self):
        generate_token()
        warehouse_products = warehouse_products_table_get(session.user_id)
        return layout.get().warehouse(warehouse_products)

    @check_logged(get_url(u'index_view'))
    def POST(self):
        req = web.input(token=u'')

        if not check_token(req.token):
            return web.seeother(get_url(u'warehouse_view'))

        success = warehouse_update(session.user_id, [(int(key[18:] or -1), int(req[key] or -1)) for key in req if key.startswith(u'warehouse_product_')])
        if success:
            put_message(u'success', u'Magazyn został zaktualizowany.')

        else:
            put_message(u'danger', u'Aktualizacja magazynu nie powiodła się!')

        return web.seeother(get_url(u'warehouse_view'))

class product_add_view:
    @check_logged(get_url(u'index_view'))
    def GET(self):
        generate_token()

        shops       = shops_get()
        products    = products_get()
        return layout.modal.warehouse_product_add(shops, products)

    @check_logged(get_url(u'index_view'))
    def POST(self):
        from views.garden import placement_get2
        req = web.input(token=u'', next=u'', placement_id=-1, shop_id=-1, shop_name=u'', shop_address=u'', product_id=-1, product_name=u'', comment=u'', price=0.0, count=0)
        req.next            = req.next.strip()
        req.placement_id    = int(req.placement_id or -1)
        req.shop_id         = int(req.shop_id or -1)
        req.shop_name       = req.shop_name.strip()
        req.shop_address    = req.shop_address.strip()
        req.product_id      = int(req.product_id or -1)
        req.product_name    = req.product_name.strip()
        req.comment         = req.comment.strip()
        req.price           = float(req.price or 0)
        req.count           = int(req.count or 0)

        if not check_token(req.token):
            return web.seeother(get_url(u'product_add_view'))

        success = True
        if req.price < 0:
            put_message(u'danger', u'Nieprawidłowa cena!')
            success = False

        elif req.count <= 0:
            put_message(u'danger', u'Nieprawidłowa ilość!')
            success = False

        elif req.placement_id != -1 and not placement_get2(session.user_id, req,placement_id):
            put_message(u'danger', u'Nieprawidłowe źródło!')
            success = False

        else:
            warehouse_product = warehouse_product_add(session.user_id, req.product_id, req.product_name, req.placement_id, req.shop_id, req.shop_name, req.shop_address, req.comment, req.price, req.count)
            if warehouse_product:
                put_message(u'success', u'Dodano towar do magazynu!<script>setTimeout(function(){parent.location.reload();}, 1000);</script>')

            else:
                put_message(u'danger', u'Wewnętrzny błąd serwera. Prosimy spróbować później.')
                success = False

        if success:
            return web.seeother(req.next or get_url(u'product_add_view'))

        generate_token()
        shops       = shops_get()
        products    = products_get()
        return layout.modal.warehouse_product_add(shops, products, req.shop_id, req.shop_name, req.shop_address, req.product_id, req.product_name, req.price, req.count)
