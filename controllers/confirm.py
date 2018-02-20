from common.config import config, getDate, getTime
from common.controller import Controller
from common.route import Route
from models.models import Order, Product, Storage, Sale, Person,StorageChange

@Route("confirm")
class Confirm(Controller):
    def Process(self, section):
        if section == 'purchase':
            purchases = Order.select().where(Order.verified == 0)
            self.RenderFile('confirm/purchase.htm', {'_': config.i18n, 'purchases': purchases})

        elif section == 'purchase.details':
            id = self.IntReq('id')
            products = Product.select().where(Product.order == Order.get(Order.id == id))
            self.RenderFile('confirm/purchase.details.htm', {'_': config.i18n, 'products': products})

        elif section == 'purchse.confirm':
            id = self.IntReq('id')
            try:
                o = Order().get(Order.id == id)
                o.verified = 1
                o.save()

                # update storage info
                products = Product.select().join(Order).where(Order.id == o.id)
                for product in products:
                    try:
                        sc = StorageChange.get(
                            (StorageChange.product == product) & (StorageChange.storage == o.storage))
                        sc.enter += product.quantity
                    except:
                        sc = StorageChange()
                        sc.storage = o.storage
                        sc.product = product
                        sc.date = getDate()
                        sc.time = getTime()
                        sc.enter = product.quantity
                        sc.purchase = product.purchase
                        sc.sell = product.sale
                        sc.reftype = 1
                        sc.refid = o.id

                    sc.save()

                self.RenderJSON({'result': 'OK'})
            except:
                self.RenderJSON({'result': 'NO'})

        elif section == 'sale':
            sales = Sale.select().where(Sale.verified == 0)
            self.RenderFile('confirm/sale.htm', {'_': config.i18n, 'sales': sales})

        elif section == 'sale.details':
            sale = Sale.get(Sale.id == self.IntReq('id'))
            details = sale.details
            i = 1
            for detail in details:
                detail.index = i
                i = i + 1

            customers = Person.select()
            storages = Storage.select()

            for cus in customers:
                if cus == sale.customer:
                    cus.selected = True

            self.RenderFile('confirm/sale.details.htm', {
                '_': config.i18n,
                'Sale': sale,
                'Sale_details': details,
                'Storages': storages,
                'Customers': customers
            })

        elif section == 'sale.confirm':
            id = self.IntReq('id')
            try:
                s = Sale().get(Sale.id == id)
                s.verified = 1
                s.save()

                # update storage info
                # saledetails = SaleDetails.select().join(Sale).where(Sale.id == s.id)
                # for sd in saledetails:
                #     try:
                #         sc = StorageChange.get((StorageChange.product == sd.product) & (StorageChange.storage == sd.storage))
                #         sc.export += sd.quantity
                #         sc.sell = sd.saleprice
                #         sc.purchase = sd.product.purchase
                #         sc.save()
                #     except:
                #         self.RenderJSON({'result':'NO'})

                self.RenderJSON({'result': 'OK'})
            except:
                self.RenderJSON({'result': 'NO'})

