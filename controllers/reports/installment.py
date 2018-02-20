from common.config import getDate, getTime
from common.report import Report
from common.reportName import ReportName
from models.models import SaleInstallment

@ReportName("instullment")
class InstallmentReport(Report):
    Name = 'installment'

    def generate(self):
        id = self.IntReq('id')
        pay = SaleInstallment.get(SaleInstallment.id == id)
        self.headers.append(('Serial', str(id)))
        self.headers.append(('Amount', str(pay.amount)))
        self.headers.append(('DateBack', pay.dateback))
        self.headers.append(('Date', pay.date))
        self.headers.append(('Remain', str(pay.sale.remind())))
        self.headers.append(('DateTime', getDate() + ' ' + getTime()))
        self.headers.append(('SaleId', pay.sale.id))
        self.headers.append(('SaleDate', pay.sale.date))
        self.headers.append(('Customer', pay.sale.customer.name))

        self.Echo('<Page />');
