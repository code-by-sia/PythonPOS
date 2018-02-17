from common.config import config
from common.controller import Controller


class TestDev(Controller):
    '''
    classdocs
    '''

    def ReadCookie(self):
        if "Cookie" in self.headers:
            c = SimpleCookie(self.headers["Cookie"])
            return c['value'].value
        return None

    def Process(self, fpath):
        '''
        Constructor
        '''
        if (fpath == 'save'):
            self.Save()
        elif fpath == 'lang':
            self.output = config.app_lang[0]
        elif fpath == 'ch-lang':
            config.ChangeLanguage(self.StringReq('lang'))
        else:
            self.output = fpath + "<br ><form action='/test/save' method='post' ><input name='a'/><button>send</button></form>"

    def Save(self):
        a = self.FloatReq('a')
        self.output = self.Currency(a) + ' is value'


