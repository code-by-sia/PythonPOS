import datetime
from datetime import timedelta

from common.config import config
from common.controller import Controller
from common.route import Route
from models.models import Order, Storage, Sale, SaleInstallment, User

@Route("dashboard")
class Dashboard(Controller):

    def Process(self, section):

        if section == 'instulments':
            today = datetime.today()
            enddate = today + timedelta(days=7)
            insts = SaleInstallment.select() \
                .where((SaleInstallment.dateback.is_null(True)) & (SaleInstallment.date < enddate))
            i = 1
            for inst in insts:
                inst.index = i
                i += 1
            self.RenderFile('dashboard/instulments.htm', {'insts': insts, '_': config.i18n, 'today': today})

        elif section == 'charts':
            users = User.select()
            storages = Storage.select()

            order = Order()
            inst = SaleInstallment()
            sale = Sale()

            self.RenderFile('dashboard/charts.htm', {
                'users': users,
                'storages': storages,
                'order': order,
                'inst': inst,
                'sale': sale,
                '_': config.i18n})
        else:
            users = User.select()
            storages = Storage.select()

            order = Order()
            inst = SaleInstallment()
            sale = Sale()

            self.RenderFile('dashboard/home.htm', {
                'users': users,
                'storages': storages,
                'order': order,
                'inst': inst,
                'sale': sale,
                '_': config.i18n})

