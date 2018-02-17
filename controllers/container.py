from common.config import config, getDate, getTime
from common.controller import Controller
from models.models import Menu


class Container(Controller):
    def Process(self, args):
        if (self.authentication.Authenticated == True):
            menu = Menu.select().where((Menu.parent >> None) | (Menu.parent >> 0))

            now = getDate()
            _ = config.i18n
            user = self.authentication.SessionObject.user
            fullname = "%s %s" % (user.name, user.family)

            args = {'Title': _('Accounting Web Application'), 'Today': now, 'lang': config.lang_name,
                    'UserName': fullname, 'Navigation': menu, '_': _}

            self.RenderFile("container/main.htm", args)
        else:
            self.RenderFile("container/login.htm", {'_': config.i18n, 'time': getTime()})