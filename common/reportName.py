from common.report import Report


def ReportName(name):
    def wrapper(type):
        print("Report %s registered by %s" % (name,type))
        Report.registerReport(name,type)
        pass

    return  wrapper
