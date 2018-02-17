from common.controller import Controller
from common.report import Report
from common.reportViewer import Viewer
from controllers.authentication import Authentication
from controllers.basicInfo import BasicInfo
from controllers.confirm import Confirm
from controllers.costs import Costs
from controllers.dashboard import Dashboard
from controllers.reportController import ReportController
from controllers.sales import Sales
from controllers.testDev import TestDev
from common.report import Report
from controllers.reports.cost import CostReport
from controllers.reports.installment import InstallmentReport
from controllers.reports.order import OrderReport
from controllers.reports.sale import SaleReport
from controllers.reports.saleList import SaleListReport
from controllers.reports.storage import StorageReport


Controller.registerController('auth',Authentication)
Controller.registerController('info',BasicInfo)
Controller.registerController('confirm',Confirm)
Controller.registerController('sale',Sales)
Controller.registerController('test',TestDev)
Controller.registerController('costs',Costs)
Controller.registerController('dashboard',Dashboard)

Controller.registerController('viewer',Viewer)
Controller.registerController('report',Report)
Controller.registerController('template',ReportController)



Report.registerReport('cost',CostReport)
Report.registerReport('instullment',InstallmentReport)
Report.registerReport('order',OrderReport)
Report.registerReport('sale',SaleReport)
Report.registerReport('sale-list',SaleListReport)
Report.registerReport('storage',StorageReport)
