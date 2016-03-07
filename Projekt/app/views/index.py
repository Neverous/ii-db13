# coding: utf-8

from main import *

class index_view:
    def GET(self):
        generate_token()
        return layout.get().index()

    POST = GET

class empty_view:
    def GET(self):
        return layout.modal.empty()

    POST = GET
