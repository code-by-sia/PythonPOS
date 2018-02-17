from common.config import config
from common.controller import Controller


class Report(Controller):
    report = None
    headers = None

    reports = {}

    Name = 'Report'

    def registerReport(name,type):
        Report.reports[name] = type
        pass

    def __init__(self):
        self.headers = []

    def Header(self):
        _ = config.i18n
        self.output = '<?xml version="1.0" encoding="UTF-8" ?>'
        self.output += '<?xml-stylesheet type="text/xsl" href="/template/' + self.report.Name + '" ?>'
        self.output += '<Viewer>'
        self.output += '<Report name="' + _(self.report.Name) + '" >'
        if (len(self.report.headers) > 0):
            self.Echo("<Header>")
            for header in self.report.headers:
                key = str(header[0])
                val = (header[1])
                val = str(val)
                self.EchoTag(key, val)
            self.Echo("</Header>")

    def Footer(self):
        self.output += '</Report>'
        self.output += '</Viewer>'

    def generate(self):

        pass

    def Process(self, section):
        self.report = Report.reports.get(section)
        if self.report is None :
            self.report = Report()
        else:
            self.report = self.report()

        self.report.query = self.query
        self.request = self.request
        self.report.generate()

        self.mimetype = 'text/xml'
        self.Header()
        self.output += self.report.output
        self.Footer()


