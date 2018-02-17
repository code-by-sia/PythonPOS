import mimetypes

from common.config import config
from common.controller import Controller


class Static(Controller):
    def Process(self, filename):
        filepath = config.server_path + "/views/static/" + filename

        mimetypes.add_type('image/svg+xml', '.svg')
        mimetypes.add_type('application/x-font-woff', '.woff')

        mime = mimetypes.guess_type(filepath)
        if len(mime) > 0:
            self.mimetype = mime[0]
        self.file = filepath
        with open(filepath, 'rb') as cfile:
            self.output = cfile.read()