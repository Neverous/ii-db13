# config: utf-8

DEBUG                   = True
DB_SECRET               = u'!@#!#%@#$RWEFSDVXCqweqwe!#$!#'
DB_ENGINE               = u'sqlite'
DB_DATABASE             = u'ogrodnik.db'
DB_PREFIX               = u'ogrodnik_'

SITE_TITLE              = u'Ogrodnik-Sadownik'
SITE_URL                = u'http://localhost:8080'

SITE_DESCRIPTION        = u'Baza Ogrodnika-Sadownika'
SITE_KEYWORDS           = u'ogrodnik, sadownik'
SITE_CSS                = (
    u'bootstrap.min.css',
#    u'bootstrap-lumen.min.css',
    u'custom-theme/jquery-ui-1.10.3.custom.css',
    u'main.css',
)

SITE_JS                 = (
    u'jquery.min.js',
    u'jquery-ui.min.js',
    u'bootstrap.min.js',
    u'flot/jquery.flot.min.js',
    u'flot/jquery.flot.time.min.js',
    u'main.js',
)

TEMPLATES_DIR           = u'templates/'

try:
    from configlocal import *

except ImportError:
    print u'WARNING: missing local configuration'

DB_OPTIONS              = {
    u'dbn':  DB_ENGINE,
    u'db':   DB_DATABASE,
}
