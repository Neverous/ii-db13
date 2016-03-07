# coding: utf-8
import re
import config

URLS = (
    u'/static/(.*)',                        u'static_view',

    # base
    u'/',                                   u'index_view',
    u'/index.html',                         u'index_view',
    u'/empty.html',                         u'empty_view',

    # authorized
    u'/gardens.html',                       u'gardens_view',
    u'/garden/([0-9]+).html',               u'garden_view',
    u'/add/garden.html',                    u'garden_add_view',
    u'/thumbnail/garden/([0-9]+).svg',      u'garden_thumbnail_view',
    u'/plant/([0-9]+).modal',               u'placement_view',
    u'/events.json',                        u'events_json_view',
    u'/events.html',                        u'events_view',
    u'/event/([0-9]+).modal',               u'event_view',
    u'/warehouse.html',                     u'warehouse_view',
    u'/add/product.modal',                  u'product_add_view',
    u'/add/event.modal',                    u'event_add_view',

    # users
    u'/register.html',                      u'user_register_view',
    u'/login.html',                         u'user_login_view',
    u'/logout.html',                        u'user_logout_view',
    u'/user.html',                          u'user_view',

    # admin
    u'/admin/users.html',                   u'admin_users_view',
    u'/admin/user/([0-9]+).html',           u'admin_user_view',
    u'/admin/gardens.html',                 u'admin_gardens_view',
    u'/admin/garden/([0-9]+).html',         u'admin_garden_view',
    u'/admin/placements.html',              u'admin_placements_view',
    u'/admin/placement/([0-9]+).html',      u'admin_placement_view',
    u'/admin/events.html',                  u'admin_events_view',
    u'/admin/event/([0-9]+).html',          u'admin_event_view',
    u'/admin/plants.html',                  u'admin_plants_view',
    u'/admin/plant/([0-9]+).html',          u'admin_plant_view',
    u'/admin/products.html',                u'admin_products_view',
    u'/admin/product/([0-9]+).html',        u'admin_product_view',
    u'/admin/shops.html',                   u'admin_shops_view',
    u'/admin/shop/([0-9]+).html',           u'admin_shop_view',
    u'/admin/warehouses.html',              u'admin_warehouse_products_view',
    u'/admin/warehouse/([0-9]+).html',      u'admin_warehouse_product_view',
)

def get_url(view_name, *args, **kwargs):
    pattern = None
    for l in range(1, len(URLS), 1):
        if view_name == URLS[l]:
            pattern = URLS[l-1]
            break

    if not pattern:
        return config.SITE_URL

    if args and kwargs:
        raise ValueError(u'*args and **kwargs is not supported.')

    exp_kwarg = re.compile(r'^\(\?P<(\w+)>(.+)\)$')

    new         = u''
    cur_group   = u''
    group_count = 0

    for ch in pattern:
        if ch == u'(':
            group_count += 1
            cur_group += ch

        elif ch == u')':
            group_count -= 1
            cur_group += ch

            if not group_count:
                m_kwarg = exp_kwarg.match(cur_group)
                if m_kwarg:
                    value = unicode(kwargs.pop(m_kwarg.group(1)))

                else:
                    value = unicode(args[0])
                    args = args[1:]

                if re.match(r'^%s$'%cur_group, value):
                    new += value
                    cur_group = ''

        elif group_count:
            cur_group += ch

        else:
            new += ch

    return config.SITE_URL + new
