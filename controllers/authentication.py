from common.config import config
from common.controller import Controller
from common.route import Route
from models.models import User


@Route("auth")
class Authentication(Controller):
    '''
    classdocs
    '''

    def Process(self, section):
        if section == 'users':
            self.RenderFile('auth/user.manage.htm', {'_': config.i18n, 'users': User.select()})
        elif section == 'user.list':
            users = User.select()
            for user in users:
                fields = (user.username)
                self.output = '%s<tr class="bigrow"><td>10000</td><td>%s</td><td></td><td></td><td></td><td></td>s</tr>' % (
                    self.output, fields)
        elif section == 'changepwd':
            self.RenderFile('auth/password.change.htm', {'_': config.i18n})
        elif section == 'roles':
            self.output = 'fch'
        else:
            self.NotImplemented(section)

