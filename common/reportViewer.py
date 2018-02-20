from common.controller import Controller
from common.route import Route

class Viewer(Controller):

    def Process(self, section):
        self.Echo('<iframe class="viewer" src="/report/' + section + '" />')

