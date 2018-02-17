from common.config import config, getDate, getTime
from common.controller import Controller
from models.models import Group, Order, Product, Storage, Supplier


class Purchase(Controller):
    '''
    classdocs
    '''

    def Process(self, section):

        if section == 'new':
            order = Order()
            storages = Storage.select()
            suppliers = Supplier.select()
            groups = Group.select();
            order.id = 0
            self.RenderFile('purchase/order.htm', {
                '_': config.i18n,
                'order': order,
                'storages': storages,
                'suppliers': suppliers,
                'group-list': groups
            })
        elif section == 'edit':
            order = Order.get(Order.id == self.IntReq('id'))

            storages = Storage.select()
            suppliers = Supplier.select()
            groups = Group.select();
            products = order.details

            for sup in suppliers:
                if sup == order.supplier:
                    sup.selected = True

            for stg in storages:
                if stg == order.storage:
                    stg.selected = True

            self.RenderFile('purchase/order.htm', {
                '_': config.i18n,
                'order': order,
                'storages': storages,
                'suppliers': suppliers,
                'group-list': groups,
                'products': products
            })
        elif section == 'save':
            id = self.IntReq('id')
            storageId = self.IntReq('storageId')
            supplierId = self.IntReq('supplierId')

            try:
                order = Order.get(Order.id == id)
            except:
                order = Order()
                order.date = getDate()
                order.time = getTime()
                order.verified = False

            supplier = Supplier.get(Supplier.id == supplierId)
            storage = Storage.get(Storage.id == storageId)

            order.supplier = supplier
            order.storage = storage
            order.user = self.authentication.SessionObject.user
            order.save()

            form = self.getForm()
            row_ids = []
            for key in form.keys():
                if key[0] == 'g':
                    id = self.ToInt(key[(key.find('[') + 1):key.find(']')])
                    row_ids.append(id)
            row_ids.sort()
            keep_rows = []

            pids = []
            # order.clearDetails()

            for row_id in row_ids:
                x = str(row_id)
                group_id = self.IntReq('g[' + x + ']')
                product_id = self.IntReq('i[' + x + ']')

                group = Group.get(Group.id == group_id)
                p = Product()

                if product_id > 0:
                    p = Product.get(Product.id == product_id)

                p.order = order
                p.group = group
                p.name = self.StringReq('n[' + x + ']')
                p.purchase = self.FloatReq('p[' + x + ']')
                p.sale = self.FloatReq('s[' + x + ']')
                p.quantity = self.FloatReq('q[' + x + ']')
                p.save()
                pids.append(p.id)
            order.clearDetails(pids)
            self.RenderJSON({'Id': order.id})
        elif section == 'manage':
            orders = Order.select()
            self.RenderFile('purchase/manage.htm', {'_': config.i18n, 'purchases': orders})

