from common.controller import Controller


class Viewer(Controller):

    def Process(self, section):
        self.Echo('<iframe class="viewer" src="/report/' + section + '" />')

