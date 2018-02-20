from common.config import config, getDate, getTime
from common.controller import Controller
from common.report import Report
from common.reportViewer import Viewer
from controllers.container import Container
from controllers.reportController import ReportController
from controllers.static import Static
from controllers.system import System
from models.models import Session

__author__ = 'SiamandMaroufi'

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# Classes

class AuthControler:
    Authenticated = False
    SessionObject = None
    Token = 'NONE'

    def __init__(self, router):

        self.router = router
        self.request = router.request
        token = self.router.getCookie('token')

        if (token != None):
            try:
                session = Session.get((Session.token == token) & (Session.status == 1))
                self.Authenticated = True
                self.SessionObject = session
                self.Token = session.token
            except:
                self.Authenticated = False
                self.SessionObject = None
                self.Token = 'NONE'

        pass

class MainRouter(Controller):
    def __init__(self, reuqest):

        self.request = reuqest
        self.authentication = AuthControler(self)
        pass

    def Route(self):
        path = self.request.path
        parsed_path = urlparse(path)

        full_path = parsed_path.path
        spath = full_path.split('/', 2)

        fpath = 'empty'
        if len(spath) > 2:
            fpath = spath[2]
        section = spath[1]
        mdl = Container()

        if (section == ''):
            mdl = Container()
        elif (section == 'static'):
            mdl = Static()
        elif (section == 'system'):
            mdl = System()
        elif(section=='report'):
            mdl = Report()
        elif(section=='viewer'):
            mld=Viewer()
        elif (section=='template'):
            mdl = ReportController()
        elif (self.authentication.Authenticated):
            mdl = Controller.controllers[section]

            if mdl is None:
                mdl = Static()
                fpath = 'security.htm'
            else:
                mdl = mdl()

        mdl.router = self
        mdl.query = parsed_path.query
        mdl.request = self.request
        mdl.authentication = self.authentication
        mdl.Process(fpath)

        return mdl

class RequestHandler(BaseHTTPRequestHandler):
    '''
    classdocs
    '''

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        ProcessRequeset(self)

    def do_POST(self):
        ProcessRequeset(self)


def ProcessRequeset(req):
    template = MainRouter(req).Route()
    template.Render()
    req.send_response(template.statuscode)
    req.send_header("Content-type", template.mimetype)
    if len(template.cookies) > 0:
        # cookies_output = template.cookies.output(header='')
        cookies_output = ""
        for key in template.cookies:
            cookies_output += ("%s=%s;Path=/;" % (key, template.cookies[key]))
        req.send_header('Set-Cookie', cookies_output)
    req.end_headers()

    fout = template.output
    if isinstance(fout, str):
        fout = bytes(fout.encode('utf-8'))

    req.wfile.write(fout)


if __name__ == '__main__':

    # glrobal _
    _ = config.i18n

    PORT = int(os.getenv('PORT', '8000'))
    HOST = os.getenv('HOST', 'localhost')
    httpd = HTTPServer((HOST, PORT), RequestHandler)


    # config.makeTempLang(Menu.select())
    # DbSetup().SetupDataBase()
    # DbSetup().BackUp()

    IS_TEST = os.getenv('BUILD_TEST')

    if IS_TEST != 'TEST':
        try:
            print (_('Samal web application server'))
            print (_('Starting server at') + ' http://%s:%s' % (HOST, PORT))
            print ('>  %s - %s' % (getDate(), getTime()))
            httpd.serve_forever()
            httpd.server_close()
            print (_('End server listening'))
        except KeyboardInterrupt:
            print (_('Server is Stopped'))
            print ('>  %s - %s' % (getDate(), getTime()))
        pass
