from common.config import config
from common.controller import Controller

class ReportController(Controller):

    def Process(self, section):
        self.mimetype = 'text/xsl'

        self.output = '<?xml version="1.0" encoding="UTF-8"?>'
        self.output += '<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">'
        self.output += '<xsl:output method="html" />'
        self.RenderFile('reports/' + section + '.xsl', {'_': config.i18n, 'CompanyName': config.CompanyName})
        self.RenderFile('reports/report-footer.xsl', {'_': config.i18n})

