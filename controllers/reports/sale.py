from common.config import _max_rows_, getDate, getTime, split
from common.report import Report
from models.models import Sale


class SaleReport(Report):
    Name = "sale"

    def generate(self):

        saleId = self.IntReq('Id')
        try:
            sale = Sale.get(Sale.id == saleId)
        except:
            sale = Sale.get()

        self.headers.append(('Id', str(sale.id)))
        self.headers.append(('CustomerId', str(sale.customer.id)))
        self.headers.append(('CustomerName', sale.customer.name))
        self.headers.append(('Date', sale.date))
        self.headers.append(('Time', sale.time))
        self.headers.append(('DateTime', getDate() + ' ' + getTime()))
        self.headers.append(('Remain', '0'))
        self.headers.append(('UserName', sale.user.fullname()))

        details = [d for d in sale.details]
        pages = split(details, _max_rows_)

        for page_details in pages:
            self.Echo('<Page>')
            for row in page_details:
                self.Echo('<Row>')
                self.EchoTag('ProductId', row.id)
                self.EchoTag('StorageName', row.storage.name)
                self.EchoTag('ProductName', row.product.name)
                self.EchoTag('Quantity', row.quantity)
                self.EchoTag('UnitPrice', row.saleprice)
                self.EchoTag('FullPrice', str(row.full_sale()))
                self.Echo('</Row>')
            self.Echo('</Page>')

