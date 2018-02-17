import json
import mimetypes
import re
from cgi import FieldStorage, parse_qs

import pystache

from common.config import config


class Controller(object):
    '''
    classdocs
    '''
    output = ""
    mimetype = "text/html"
    statuscode = 200
    request = None
    query = None
    cookies = {}
    authentication = None

    controllers = {}

    query_parts = None
    post_form = None
    post_form_calced = False

    def registerController(name,controller):
        Controller.controllers[name]=controller
        pass

    def setCookie(self, name, value, path='/'):
        self.cookies[name] = value
        pass

    def getForm(self):
        if self.post_form_calced == True:
            return self.post_form

        self.post_form_calced = True
        try:
            req = self.request
            form = FieldStorage(
                fp=req.rfile,
                headers=req.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': req.headers['Content-Type']}
            )
            self.post_form = form
            return form
        except:
            return None

    def Req(self, keyname):
        Obj = self.GET(keyname)

        if Obj == None or Obj == '':
            if self.getForm() != None:
                Obj = self.getForm().getvalue(keyname)
        if Obj == None:
            Obj = 0;
        return Obj

    def ToInt(self, Obj):
        strv = re.sub("[^0-9\-]", "", str(Obj))
        if strv == '':
            return 0
        else:
            try:
                return int(strv)
            except:
                return 0;

    def StringReq(self, keyname):
        Obj = self.Req(keyname)
        if Obj == None:
            return ''
        else:
            return str(Obj)

    def IntReq(self, keyname):
        Obj = self.Req(keyname)
        if Obj == None:
            return 0
        else:
            strv = re.sub("[^0-9\-]", "", str(Obj))
            if strv == '':
                return 0
            else:
                try:
                    return int(strv)
                except:
                    return 0;

    def FloatReq(self, keyname):
        Obj = self.Req(keyname)
        if Obj == None:
            return 0
        else:
            strv = re.sub("[^0-9\-\.]", "", str(Obj))
            if strv == '':
                return 0
            else:
                try:
                    return float(strv)
                except:
                    return 0.0

    def getQueryString(self):
        if self.query_parts == None:
            self.query_parts = parse_qs(self.query)
        return self.query_parts

    def GET(self, keyname):
        qp = self.getQueryString()
        rd = ['']
        if keyname in qp:
            rd = qp[keyname]
        if len(rd) == 1:
            return rd[0]
        else:
            return rd

    def extractCookies(self):

        if len(self.cookies) == 0:
            if "Cookie" in self.request.headers:
                try:
                    data = self.request.headers['Cookie']
                    if len(data) > 0:
                        rows = (data.split(';'))
                        for row in rows:
                            cell = row.strip().split('=')
                            self.cookies[cell[0]] = cell[1]
                except:
                    pass

    def getCookie(self, cookiename):
        try:
            self.extractCookies()
            return self.cookies[cookiename]
        except:
            return None

    def getTemplate(self, filename):
        file = open(config.server_path + "/templates/" + filename, 'r')
        outp = file.read()
        return outp

    def NotImplemented(self, section):
        self.RenderFile('error/not-implemented.htm', {'section': section})

    def RenderJSON(self, data):
        self.output = json.dumps(data)

    def RenderFile(self, filename, args=None):
        fpath = config.server_path + "/views/" + filename
        mimetypes.add_type('image/svg+xml', '.svg')
        mimetypes.add_type('application/x-font-woff', '.woff')
        mime = mimetypes.guess_type(fpath)
        if (len(mime) > 1):
            self.mimetype = mime[0]

        translate = False
        if self.mimetype in ('text/html', 'text/xml', 'application/xml'):
            translate = True

        # try:
        file = open(fpath, 'rb')
        outp = file.read()
        if isinstance(outp, bytes):
            outp = outp.decode('utf-8')
        if translate:
            outp = pystache.render(outp, args)
        # .encode('utf-8')
        self.output += outp

        pass

    def Translate(self):
        outp = self.output

        outp = outp.decode('utf-8')
        outp = pystache.render(outp, {'_': config.i18n})
        outp = outp.encode('utf-8')

        self.output = outp

    def Render(self):
        return self.output

    def Currency(self, number):
        if number == None:
            number = 0
        return config.l10n.currency(number, grouping=True)

    def Echo(self, q):
        self.output += q

    def EchoTag(self, name, value):
        self.Echo("<%s>%s</%s>" % (name, value, name))