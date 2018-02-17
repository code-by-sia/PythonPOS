from app import config
from common.config import getDate, getTime
from common.controller import Controller
from models.models import Product, Storage, StorageChange, Sale, SaleDetails, SaleInstallment, Person


class Sales(Controller):
    def Process(self, section):
        if section == 'new':
            customers = Person.select()
            storages = Storage.select()
            sale = Sale()
            sale.id = 0
            sale.advance = 0
            sale.date = getDate()
            self.RenderFile('sale/sale.htm', {
                '_': config.i18n,
                'Customers': customers,
                'Storages': storages,
                'Sale': sale
            })
        elif section == 'edit':
            sale = Sale.get(Sale.id == self.IntReq('id'))

            details = sale.details
            i = 1
            for detail in details:
                detail.index = i
                i = i + 1
            i = 1

            installments = sale.installments
            for si in installments:
                si.index = i
                i = i + 1

            customers = Person.select()
            storages = Storage.select()

            for cus in customers:
                if cus == sale.customer:
                    cus.selected = True

            self.RenderFile('sale/sale.htm', {
                '_': config.i18n,
                'Sale': sale,
                'Sale_details': details,
                'Sale_installments': installments,
                'Storages': storages,
                'Customers': customers
            })
        elif section == 'save':
            id = self.IntReq('id')
            pays = self.IntReq('pays')
            prepaid = self.FloatReq('prepaid')
            customerId = self.IntReq('customerId')

            try:
                sale = Sale.get(Sale.id == id)
            except:
                sale = Sale()
                sale.date = getDate()
                sale.time = getTime()
                sale.user = self.authentication.SessionObject.user
                sale.verified = False
            customer = Person.get(Person.id == customerId)

            sale.customer = customer
            sale.installment = pays
            sale.advance = prepaid
            sale.payment = 0
            sale.fullsale = 0

            sale.save()

            form = self.getForm()
            row_ids = []
            srow_ids = []
            for key in form.keys():
                if key[0] == 'g':
                    id = self.ToInt(key[(key.find('[') + 1):key.find(']')])
                    row_ids.append(id)
                elif key[0] == 'b':
                    id = self.ToInt(key[(key.find('[') + 1):key.find(']')])
                    srow_ids.append(id)

            row_ids.sort()
            srow_ids.sort()

            sale.clearDetails()
            full_sale = 0

            for row_id in row_ids:
                x = str(row_id)
                storage_id = self.IntReq('g[' + x + ']')
                product_id = self.IntReq('p[' + x + ']')
                sale_price = self.FloatReq('s[' + x + ']')
                sale_qty = self.FloatReq('q[' + x + ']')
                full_sale += sale_price * sale_qty

                detail = SaleDetails()
                detail.sale = sale
                detail.product = Product.get(Product.id == product_id)
                detail.quantity = sale_qty
                detail.saleprice = sale_price
                detail.storage = Storage.get(Storage.id == storage_id)
                detail.save()

                schange = StorageChange()
                schange.storage = detail.storage
                schange.product = detail.product
                schange.enter = 0
                schange.export = sale_qty
                schange.purchase = detail.product.purchase
                schange.sell = sale_price
                schange.date = sale.date
                schange.time = sale.time
                schange.reftype = 2
                schange.refid = sale.id
                schange.save()

            for row_id in srow_ids:
                x = str(row_id)
                date = self.StringReq('b_d[' + x + ']')
                pay = self.FloatReq('y_p[' + x + ']')

                sins = SaleInstallment()
                sins.sale = sale
                sins.date = date
                sins.amount = pay
                sins.save()

            sale.fullsale = full_sale
            sale.save()
            self.RenderJSON({'Id': sale.id})

        elif section == 'manage':
            sales = Sale.select()
            self.RenderFile('sale/manage.htm', {'_': config.i18n, 'sales': sales})
        elif section == 'return':
            self.output = 'Return'
        elif section == 'installments':
            saleId = self.IntReq('SaleId')
            pqty = self.IntReq('Pays')
            sale = Sale.get(Sale.id == saleId)

            if pqty != sale.installment:
                sale.installment = pqty
                sale.save()
                sale.createInstallments()

            i = 0
            for ins in sale.installments:
                i = i + 1
                ins.index = i
            self.RenderFile('sale/installments.htm', {'_': config.i18n, 'sale': sale})

