from common.config import config, getDate
from common.controller import Controller
from common.route import Route
from models.models import Person, Supplier, Group, Storage, Cost, Sale, Product, Order, SaleInstallment

@Route('info')
class BasicInfo(Controller):
    '''
    classdocs
    '''

    def Process(self, section):
        # Open a form in order to save or update
        if section == 'person.new':
            person = Person()
            person.id = 0
            self.RenderFile('person/person.htm', {'_': config.i18n, 'person': person})

        elif section == 'supplier.new':
            supplier = Supplier()
            supplier.id = 0
            self.RenderFile('supplier/supplier.htm', {'_': config.i18n, 'supplier': supplier})

        elif section == 'group.new':
            group = Group()
            group.id = 0
            self.RenderFile('group/group.htm', {'_': config.i18n, 'group': group})

        elif section == 'storage.new':
            storage = Storage()
            storage.id = 0
            self.RenderFile('storage/storage.htm', {'_': config.i18n, 'storage': storage})

        elif section == 'cost.new':
            cost = Cost()
            cost.id = 0
            self.RenderFile('cost/cost.htm', {'_': config.i18n, 'cost': cost})

        # Open a form with fields filled with data to update
        elif section == 'person.edit':
            id = self.IntReq('id')
            person = Person.get(Person.id == id)
            self.RenderFile('person/person.htm', {'_': config.i18n, 'person': person})

        elif section == 'supplier.edit':
            id = self.IntReq('id')
            supplier = Supplier.get(Supplier.id == id)
            self.RenderFile('supplier/supplier.htm', {'_': config.i18n, 'supplier': supplier})

        elif section == 'group.edit':
            id = self.IntReq('id')
            group = Group().get(Group.id == id)
            self.RenderFile('group/group.htm', {'_': config.i18n, 'group': group})

        elif section == 'storage.edit':
            id = self.IntReq('id')
            storage = Storage().get(Storage.id == id)
            self.RenderFile('storage/storage.htm', {'_': config.i18n, 'storage': storage})

        elif section == 'cost.edit':
            id = self.IntReq('id')
            cost = Cost().get(Cost.id == id)
            self.RenderFile('cost/cost.htm', {'_': config.i18n, 'cost': cost})


        # Send save operation to the controler
        elif section == 'person.save':
            id = self.IntReq('id')
            try:
                p = Person.get(Person.id == id)
            except:
                p = Person()
            p.name = self.StringReq('name')
            p.city = self.StringReq('city')
            p.phone = self.StringReq('phone')
            p.email = self.StringReq('email')
            p.address = self.StringReq('address')
            p.save()

            self.RenderJSON({'Result': 'success', 'id': p.id});
        elif section == 'supplier.save':
            id = self.IntReq('id')
            try:
                s = Supplier.get(Supplier.id == id)
            except:
                s = Supplier()
            s.name = self.StringReq('name')
            s.manager = self.StringReq('manager')
            s.tell = self.StringReq('tell')
            s.field = self.StringReq('field')
            s.save()

            self.RenderJSON({'Result': 'success', 'id': s.id});

        elif section == 'group.save':
            id = self.IntReq('id')
            try:
                g = Group.get(Group.id == id)
            except:
                g = Group()

            g.name = self.StringReq('name')
            g.unit = self.StringReq('unit')
            g.save()
            self.RenderJSON({'Result': 'success', 'id': g.id})

        elif section == 'storage.save':
            id = self.IntReq('id')
            try:
                st = Storage.get(Storage.id == id)
            except:
                st = Storage()

            st.name = self.StringReq('name')
            st.tell = self.StringReq('tell')
            st.address = self.StringReq('address')
            st.save()
            self.RenderJSON({'Result': 'success', 'id': st.id})

        elif section == 'cost.save':
            id = self.IntReq('id')
            try:
                ct = Cost.get(Cost.id == id)
            except:
                ct = Cost()

            ct.regdate = self.StringReq('regdate')
            ct.regtime = self.StringReq('regtime')
            ct.title = self.StringReq('title')
            ct.invoiceno = self.StringReq('invoiceno')
            ct.amount = self.FloatReq('amount')

            ct.save()
            self.RenderJSON({'Result': 'success', 'id': ct.id})

        elif section == 'person.check':
            self.output = ''

        elif section == 'person.filter':
            list = Person.select()
            args = {'data': list, '_': config.i18n}
            self.RenderFile('person/list.htm', args)


        # Delete section for each item
        elif section == 'group.delete':
            id = self.IntReq('id')
            group = Group.get(Group.id == id)
            group.delete_instance()
            self.RenderJSON({'result': 'OK'})

        elif section == 'supplier.delete':
            id = self.IntReq('id')
            supplier = Supplier.get(Supplier.id == id)
            supplier.delete_instance()
            self.RenderJSON({'result': 'OK'})

        elif section == 'storage.delete':
            id = self.IntReq('id')
            storage = Storage.get(Storage.id == id)
            storage.delete_instance()
            self.RenderJSON({'result': 'OK'})

        elif section == 'person.delete':
            id = self.IntReq('id')
            person = Person.get(Person.id == id)
            person.delete_instance()
            self.RenderJSON({'result': 'OK'})

        elif section == 'cost.delete':
            id = self.IntReq('id')
            cost = Cost.get(Cost.id == id)
            cost.delete_instance()
            self.RenderJSON({'result': 'OK'})


        # Manage section for items
        elif section == 'person.manage':
            self.RenderFile('person/manage.htm', {'_': config.i18n, 'persons': Person.select()})

        elif section == 'supplier.manage':
            args = {'_': config.i18n, 'suppliers': Supplier.select()}
            self.RenderFile('supplier/manage.htm', args)

        elif section == 'group.manage':
            list = Group.select()
            args = {'groups': list, '_': config.i18n}
            self.RenderFile('group/manage.htm', args)

        elif section == 'storage.manage':
            list = Storage.select()
            args = {'storages': list, '_': config.i18n}
            self.RenderFile('storage/manage.htm', args)

        elif section == 'cost.manage':
            list = Cost.select()
            args = {'costs': list, '_': config.i18n}
            self.RenderFile('cost/manage.htm', args)

        elif section == 'person.history':
            id = self.IntReq('id')
            person = Person.get(Person.id == id)
            sales = Sale.select().where(Sale.customer == person)
            i = 1
            for sale in sales:
                sale.index = i
                i += 1
            args = {
                'person': person,
                'sales': sales,
                '_': config.i18n}
            self.RenderFile('person/history.htm', args)

        elif section == 'group.goodlist':
            id = self.IntReq('id')
            g = Group.get(Group.id == id)
            args = {'group': g, 'products': g.products.group_by(Product.name), '_': config.i18n}
            self.RenderFile('group/goodlist.htm', args)

        elif section == 'storage.goodlist':
            id = self.IntReq('id')
            is_JSON = (self.IntReq('json') != 0)
            s = Storage.get(Storage.id == id)
            args = {'_': config.i18n, 'storage': s, 'products': s.goodlist()}
            if is_JSON:
                ps = []
                for p in s.goodlist():
                    pr = p.purchase_string()
                    sl = p.sell_string()
                    ps.append({'id': p.product.id, 'name': p.product.name, 'qty': p.storage_current(s), 'purchase': pr,
                               'sale': sl})
                self.RenderJSON(ps)
            else:
                self.RenderFile('storage/goodlist.htm', args)

        elif section == 'supplier.purchaselist':
            id = self.IntReq('id')
            s = Supplier.get(Supplier.id == id)
            products = Product.select().join(Order).where(Order.supplier == s)
            i = 1
            for p in products:
                p.index = i
                i = i + 1
            args = {'supplier': s, 'products': products, '_': config.i18n}
            self.RenderFile('supplier/purchaselist.htm', args)

        elif section == 'person.instullment':
            id = self.IntReq('id')
            inst = SaleInstallment.get(SaleInstallment.id == id)
            inst.currentdate = getDate()
            args = {'inst': inst, '_': config.i18n}
            self.RenderFile('person/instullment.htm', args)
        elif section == 'person.instullment.save':

            id = self.IntReq('id')
            try:
                si = SaleInstallment.get(SaleInstallment.id == id)
            except:
                si = SaleInstallment()

            si.dateback = self.StringReq('dateback')
            si.amount = self.FloatReq('amount')
            si.save()

            sale = Sale.get(Sale.id == si.sale.id)
            sale.payment = float(sale.payment) + float(si.amount)
            sale.save()

            self.RenderJSON({'result': 'ok', 'id': si.id, 'amount': si.amount, 'dateback': si.dateback})
        else:
            self.NotImplemented(section)