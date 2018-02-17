from common.config import _max_rows_, getDate, getTime, split
from common.report import Report
from models.models import Cost


class CostReport(Report):
    Name = 'cost'

    def generate(self):

        self.headers.append(('DateTime', getDate() + ' ' + getTime()))

        list = Cost().select()
        list = [d for d in list]

        pages = split(list, _max_rows_)
        for list in pages:
            self.Echo('<Page>')
            for row in list:
                self.Echo('<Row>')
                self.EchoTag('Title', row.title)
                self.EchoTag('InvoiceId', row.invoiceno)
                self.EchoTag('RegDate', row.regdate)
                self.EchoTag('Amount', row.amount)
                self.Echo('</Row>')
            self.Echo('</Page>')

