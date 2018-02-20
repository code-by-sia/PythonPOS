from common.config import _max_rows_, getDate, getTime, split
from common.report import Report
from common.reportName import ReportName
from models.models import User

@ReportName("sale-list")
class SaleListReport(Report):
    Name = 'sale-list'

    def generate(self):

        username = self.StringReq('User')

        try:
            user = User.get(User.username == username)
        except:
            user = User.get()

        self.headers.append(('DateTime', getDate() + ' ' + getTime()))
        self.headers.append(('UserName', user.fullname()))

        list = user.salelist
        list = [d for d in list]

        users = User.select()
        for user in users:
            self.Echo('<User>')
            self.EchoTag('Id', user.username)
            self.EchoTag('UserName', user.fullname())
            self.Echo('</User>')

        pages = split(list, _max_rows_)
        for list in pages:
            self.Echo('<Page>')
            for row in list:
                self.Echo('<Row>')
                self.EchoTag('Id', row.id)
                self.EchoTag('Time', row.time)
                self.EchoTag('Customer', row.customer.name)
                self.EchoTag('FullSale', row.fullsale)
                self.EchoTag('Prepaid', row.advance)
                self.EchoTag('Remain', row.remind())
                self.Echo('</Row>')
            self.Echo('</Page>')

