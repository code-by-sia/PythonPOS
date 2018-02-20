from common.config import getDate, getTime
from common.report import Report
from common.reportName import ReportName
from models.models import Order

@ReportName("order")
class OrderReport(Report):
    Name = "order"

    def generate(self):
        orderId = self.IntReq('Id')

        try:
            order = Order.get(Order.id == orderId)
        except:
            order = Order.get()

        self.headers.append(('Id', str(order.id)))
        self.headers.append(('SupplierId', str(order.supplier.id)))
        self.headers.append(('SupplierName', order.supplier.name))
        self.headers.append(('Date', order.date))
        self.headers.append(('Time', order.time))
        self.headers.append(('DateTime', getDate() + ' ' + getTime()))
        self.headers.append(('Storage', order.storage.name))
        self.headers.append(('UserName', order.user.fullname()))

        self.Echo('<Page>')
        for row in order.details:
            self.Echo('<Row>')
            self.EchoTag('ProductId', row.id)
            self.EchoTag('ProductName', row.name)
            self.EchoTag('Category', row.group.name)
            self.EchoTag('Quantity', row.quantity)
            self.EchoTag('UnitPrice', row.purchase)
            self.EchoTag('FullPrice', row.full_purchase())
            self.Echo('</Row>')
        self.Echo('</Page>')

