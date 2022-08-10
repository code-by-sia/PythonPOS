import gettext
from datetime import datetime
from datetime import  date

import  locale
# import locale
import os
import re

from peewee import SqliteDatabase, MySQLDatabase


class config:
    __author__ = 'Siamand'

    server_path = os.path.dirname(os.path.realpath(__file__ + "/..") )
    lang_name = os.getenv('APP_LANG', 'fa')
    app_lang = [lang_name]
    app_locale = os.getenv('APP_LOCALE', 'en_US')
    app_db_user = 'root';
    app_db_pass = '';

    i18n_language = gettext.translation('default', 'locale', app_lang)
    i18n = i18n_language.gettext
    _ = i18n


    print(app_locale)


    locale.setlocale(locale.LC_ALL, app_locale)
    l10n = locale

    CompanyName = _('CompanyName')

    def makeTempLang(menus):
        fs = getFiles('templates/')
        words = []
        regex = re.compile("\{\{\#\_\}\}(.*)\{\{/\_\}\}")

        for f in fs:
            try:
                data = open(f, 'r').read()
                fwords = re.findall(regex, data)
                words.extend(fwords)

            except:
                pass

        clean = (words[4:])
        data = 'from core import config\n_=config.i18n\n'

        for menu in menus:
            data = "%s_('%s')\n" % (data, menu.title)

        for c in clean:
            data = "%s_('%s')\n" % (data, c)
        open('locale/temp2.py', 'w+').write(data)

        pass

    def getFiles(spath=''):
        res = []
        arr = os.listdir(spath)
        for d in arr:
            dpath = os.path.join(spath, d)
            if d.endswith('.htm'):
                res.append(dpath)
            if os.path.isdir(dpath):
                sub = getFiles(dpath)
                if len(sub) > 0:
                    res.extend(sub)
        return res


_max_rows_ = 40;


def getDate():
    return date.today().strftime("%Y-%m-%d")


def getTime():
    return datetime.now().strftime("%H-%M-%S")


def addDate(date, y, m, d):
    date = datetime.datetime.strptime(date)
    return date + dated


def split(arr, size):
    if size < 1:
        size = 1
    arrs = []
    while len(arr) > size:
        right = arr[:size]
        arrs.append(right)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def ChangeLanguage(language):
    # from core import config
    # config.app_lang = [language]
    # config.i18n_language = gettext.translation('default', 'locale', app_lang)
    # config.i18n = i18n_language.gettext
    pass


# sqlitedb_test = SqliteDatabase(config.server_path + '/test.db')
sqlitedb = SqliteDatabase(config.server_path + '/database.db')
# mysqldb = MySQLDatabase('accdb', host='127.0.0.1', user=config.app_db_user, passwd=config.app_db_pass)

serverdb = sqlitedb


def makeTempLang(menus):
    fs = getFiles('templates/')
    words = []
    regex = re.compile("\{\{\#\_\}\}(.*)\{\{/\_\}\}")

    for f in fs:
        try:
            data = open(f, 'r').read()
            fwords = re.findall(regex, data)
            words.extend(fwords)

        except:
            pass

    clean = (words[4:])
    data = 'from core import config\n_=config.i18n\n'

    for menu in menus:
        data = "%s_('%s')\n" % (data, menu.title)

    for c in clean:
        data = "%s_('%s')\n" % (data, c)
    open('locale/temp2.py', 'w+').write(data)

    pass


def getFiles(spath=''):
    res = []
    arr = os.listdir(spath)
    for d in arr:
        dpath = os.path.join(spath, d)
        if d.endswith('.htm'):
            res.append(dpath)
        if os.path.isdir(dpath):
            sub = getFiles(dpath)
            if len(sub) > 0:
                res.extend(sub)
    return res