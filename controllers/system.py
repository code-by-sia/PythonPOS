from common.controller import Controller
from models.models import Session


class System(Controller):

    def Process(self, fpath):
        if (fpath == 'login'):
            self.Login()
        elif (fpath == 'logout'):
            self.Logout()
        pass

    def Login(self):

        self.mimetype = 'application/json'
        # form = self.getQueryString()

        username = self.Req('username')
        password = self.Req('password')

        session = None
        # if(form.has_key('username') and form.has_key('password')):
        if username != None and password != None:
            # username = form['username']
            # passowrd = form['password']
            session = Session().Login(username, password)

        if (session != None):
            self.setCookie('token', session.token)
            self.output = '{status:1}'
        else:
            self.output = '{status:0}'

    def Logout(self):
        try:
            if (self.authentication.Authenticated):
                session = self.authentication.SessionObject
                session.Logout()
            self.output = '<script>location.reload()</script>'
        except:
            self.output = '{status=-1}'