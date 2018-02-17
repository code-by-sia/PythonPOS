import hashlib
import os

from jdatetime import timedelta
from peewee import *

from common import config
from common.config import *
from common.model import BaseModel


class Cost(BaseModel):
    title 	    = CharField(default='')
    invoiceno   = CharField(default='0')
    amount      = DecimalField(20,default=0)
    regdate     = CharField(10,default='')
    regtime     = CharField(10,default='')

    def amount_string(self):

        return  config.l10n.currency(self.amount,grouping=True)

class User(BaseModel):
    username = CharField(primary_key=True)
    password = CharField()
    name  = CharField()
    family= CharField()
    job   = CharField()
    email = CharField()
    isAdmin  = BooleanField(default=False)

    def fullname(self):
        return self.name + ' ' + self.family

    def SalesByDate(self):
        x= User.select(
            fn.Sum(Sale.fullsale).alias('totalsale'),
            Sale.date.alias('saledate'),
            User
        ) \
            .join(Sale) \
            .where(Sale.user==self) \
            .group_by(User,Sale.date) \
            .order_by(Sale.date)
        # print (x)
        return x

class Role(BaseModel):
    rolename = CharField()

class UserRole(BaseModel):
    user =ForeignKeyField(User)
    role =ForeignKeyField(Role)

class Session(BaseModel):
    token = CharField()
    time  = CharField()
    date  = CharField()
    ip    = CharField()
    user  = ForeignKeyField(User)
    status= IntegerField()

    def generate_token(self):
        m =hashlib.md5()
        m.update(os.urandom(32))
        return m.hexdigest()

    def Login(self,username,password):
        # try:
        fuser = User.get((User.username==username) & (User.password==password))
        session = Session(token=self.generate_token(),time=getTime(),date=getDate(),ip='192.168.1.1',user=fuser,status=1)
        session.save()
        return session
        # except:
        #     print ('error')
        #     return None

        try_stmt

    def Logout(self):
        lquery=self.update(status=2).where(Session.token==self.token)
        lquery.execute()

class Permission(BaseModel):
    name   = CharField()
    parent = ForeignKeyField('self', related_name='children', null=True)

class UserPermission(BaseModel):
    user      = ForeignKeyField(User)
    permission= ForeignKeyField(Permission)

class RolePermission(BaseModel):
    role      = ForeignKeyField(Role)
    permission= ForeignKeyField(Permission)

class SessionPermission(BaseModel):
    session   = ForeignKeyField(Session)
    permission= ForeignKeyField(Permission)

class Menu(BaseModel):
    title = CharField()
    icon = CharField()
    href = CharField()
    order=IntegerField()
    parent = ForeignKeyField('self', related_name='submenus', null=True)
    permission=ForeignKeyField(Permission)

    def i18nTitle(self):return config.i18n(self.title)

    class Meta:
        order_by = ('order','id')

class Group(BaseModel):
    name = CharField(default='')
    unit = CharField(default='')

class Person(BaseModel):
    name = CharField(default='')
    city = CharField(default='')
    phone = CharField(default='')
    email = CharField(default='')
    address = TextField(default='')

    def total_purchase(self):
        r = Sale.select(fn.Sum(Sale.fullsale).alias('total')).where(Sale.customer == self).get()
        try :
            amt = r.total
            if amt == None:
                amt=0
        except:
            return 0
        return config.l10n.currency(amt,grouping=True)

class Supplier(BaseModel):
    name = CharField(default='')
    manager = CharField(default='')
    tell = CharField(default='')
    field = CharField(default='')


    def purchaseamount(self):
        orders = Order.select().where((Order.supplier == self) & (Order.verified == 1))
        sum = 0;
        for order in orders:
            sum += order.amount()
        from core import  config
        return  config.l10n.currency(sum,grouping=True)

class Storage(BaseModel):
    name = CharField(default='')
    tell = CharField(default='')
    address =  TextField(default='')

    def stock(self):
        try:
            sc = StorageChange.select(fn.Sum(StorageChange.enter * StorageChange.purchase).alias('total')).where((StorageChange.storage == self) & (StorageChange.export == 0) & (StorageChange.reftype == 1)).get()
            total_purchase = sc.total
            sc = StorageChange.select(fn.Sum(StorageChange.export * StorageChange.purchase).alias('total')).where((StorageChange.storage == self) & (StorageChange.enter == 0) & (StorageChange.reftype == 2)).get()
            total_sale = sc.total
            sum = total_purchase - total_sale
        except:
            sum = 0
        return config.l10n.currency(sum,grouping=True)

    def stock_value(self):
        try:
            sc = StorageChange.select(
                fn.Sum(StorageChange.enter * StorageChange.purchase).alias('total')) \
                .where((StorageChange.storage == self)
                       & (StorageChange.export == 0)
                       & (StorageChange.reftype == 1)).get()
            total_purchase = sc.total
            sc = StorageChange.select(
                fn.Sum(StorageChange.export * StorageChange.purchase).alias('total')) \
                .where((StorageChange.storage == self)
                       & (StorageChange.enter == 0)
                       & (StorageChange.reftype == 2)).get()
            total_sale = sc.total
            sum = total_purchase - total_sale
        except:
            sum = 0
        return sum

    def goodlist(self):
        res = StorageChange.select(StorageChange.product,StorageChange.storage,
                                   fn.Sum(StorageChange.enter).alias('enter'),
                                   fn.Sum(StorageChange.export).alias('export'),
                                   fn.Max(StorageChange.sell).alias('sell'),
                                   fn.Avg(StorageChange.purchase).alias('purchase')
                                   ).where(StorageChange.storage == self) \
            .group_by(StorageChange.product,StorageChange.storage)
        return res

    def total_capacity(self):
        try:
            sc = StorageChange.select(
                fn.Sum(StorageChange.enter * StorageChange.purchase).alias('total')) \
                .where((StorageChange.storage == self)
                       & (StorageChange.export == 0)
                       & (StorageChange.reftype == 1)).get()
            sum = sc.total
        except:
            sum = 0
        return sum

    def percentage(self):
        if self.total_capacity() == 0: return 0
        res = 0
        try:
            res = math.ceil((float(self.stock_value()) * 100 / float(self.total_capacity())))
        except:
            pass
        return res

class Order(BaseModel):
    supplier = ForeignKeyField(Supplier,related_name='orderlist')
    storage  = ForeignKeyField(Storage,related_name='orders')
    user     = ForeignKeyField(User,related_name='orderlist')
    date     = CharField(10)
    time     = CharField(8)
    verified = BooleanField()

    class Meta:
        order_by = ('date',)

    def clearDetails(self,pids):
        dq = Product.delete().where((Product.order == self) & (~(Product.id << pids)))
        dq.execute()

    def amount(self):
        r = Product.select(fn.Sum(Product.quantity * Product.purchase).alias('fullamount')).where(Product.order == self).get()
        try :
            amt = r.fullamount
            if amt == None:
                amt=0
            return amt
        except:
            return 0

    def amount_string(self):
        return config.l10n.currency( self.amount(),grouping=True)

    def today(self):
        res = 0
        try:
            list = Order.select().where(Order.date == getDate())
            res = list.count()
        except:
            res = 0
        return res

class Product(BaseModel):
    order   = ForeignKeyField(Order,related_name="details")
    group   = ForeignKeyField(Group,related_name="products")
    name    = CharField(50)
    quantity= FloatField()
    purchase= DecimalField(10,2)
    sale    = DecimalField(10,2)

    def new_id(self):
        return 1
        #
        # max_id = p.select(fn.Max(Product.id).alias('max_id')).get().max_id
        # print 'xxx'
        # if max_id == None :
        #     print 'sss'
        #     return 1
        # else:
        #     return max_id + 1

    def sale_string(self):
        if self.sale == None : slef.sale = 0
        return config.l10n.currency(self.sale,grouping=True)

    def purchase_string(self):
        return config.l10n.currency(self.purchase,grouping=True)

    def full_purchase(self):
        return float(self.purchase) * float(self.quantity)

    def full_sale(self):
        return float(self.sale) * float(self.quantity)

    def full_purchase_string(self):
        return config.l10n.currency(self.full_purchase(),grouping=True)

    def full_sale_string(self):
        return config.l10n.currency(self.full_sale(),grouping=True)

    def groups(self):
        groups = Group.select()
        for group in groups:
            if group.id == self.group.id:
                group.selected=True
        return groups

    def store(self,storage):
        return Product.select().join(Order).where(Order.storage==storage)

class Sale(BaseModel):
    customer = ForeignKeyField(Person,related_name='salelist')
    date     = CharField(10)
    time     = CharField(8)
    fullsale = DecimalField(20,2)
    advance  = DecimalField(20,2)
    payment  = DecimalField(20,2)
    installment = IntegerField(default=0)
    verified = BooleanField()
    user     = ForeignKeyField(User,related_name='salelist')

    class Meta:
        order_by=('date','time')

    def sumqty(self):
        sd = SaleDetails.select(fn.Sum(SaleDetails.quantity).alias('qty')).where(SaleDetails.sale == self).get()
        return sd.qty

    def sumsale(self):
        SDs = SaleDetails.select().where(SaleDetails.sale == self)
        price = 0
        for sd in SDs:
            price += float(sd.saleprice) * float(sd.quantity)

        return price

    def sumsale_string(self):
        return config.l10n.currency(self.sumsale(),grouping=True)

    def remaind(self):
        sumsale = self.sumsale()
        suminst = SaleInstallment.select(fn.Sum(SaleInstallment.amount)).join(Sale).where(SaleInstallment.dateback != None).get()
        if suminst == None:
            suminst = 0
        rem = sumsale - suminst
        return rem

    def remaind_string(self):
        return config.l10n.currency(self.remaind(),grouping=True)

    def clearDetails(self):
        SaleDetails.delete().where(SaleDetails.sale==self).execute()
        SaleInstallment.delete().where(SaleInstallment.sale==self).execute()

        if self.id > 0 :
            StorageChange.delete().where((StorageChange.refid==self.id) & (StorageChange.reftype==2)).execute()

    def remind(self):
        return self.fullsale -  self.advance - self.payment

    def amount_string(self):
        return config.l10n.currency(self.fullsale,grouping=True)

    def remind_string(self):
        return config.l10n.currency(self.remind(),grouping=True)

    def advance_string(self):
        return config.l10n.currency(self.advance,grouping=True)


    def createInstallments(self):
        SaleInstallment.delete().where(SaleInstallment.sale == self).execute()

        qty = self.installment
        pay =math.floor(self.fullsale / (qty))

        sdate = self.date

        for i in range(qty-1):
            si = SaleInstallment()
            si.sale = self
            si.date = sdate
            si.amount = pay
            si.save()
        si = SaleInstallment()
        si.sale = self
        si.date=sdate
        si.amount = int(float(self.fullsale) - ((qty-1) * pay ))
        si.save()

        pass

    def today(self):
        res = 0
        try:
            list = Sale.select().where(Sale.date == getDate())
            res = list.count()
        except:
            res = 0
        return res

class SaleDetails(BaseModel):
    sale    = ForeignKeyField(Sale,related_name= 'details')
    storage  = ForeignKeyField(Storage,related_name='sales')
    product = ForeignKeyField(Product,related_name='sales')
    quantity= FloatField()
    saleprice= DecimalField(20,2)

    def saleprice_string(self):
        return config.l10n.currency(self.saleprice,grouping=True)

    def full_sale(self):
        return  self.quantity *  float(self.saleprice)

    def full_sale_string(self):
        try:
            fsale= float(self.saleprice) * float(self.quantity) # * self.saleprice
        except:
            fsale=0
        return config.l10n.currency(fsale,grouping=True)

    def StorageList(self):
        storages = Storage.select()
        for stg in storages:
            if stg.id == self.storage.id:
                stg.selected=True
        return storages

    def ProductList(self):
        glist= self.storage.goodlist();
        for gd in glist:
            if gd.product == self.product :
                gd.selected=True
        return glist;

class SaleInstallment(BaseModel):
    sale    = ForeignKeyField(Sale,related_name='installments')
    date    = CharField(10)
    dateback= CharField(10)
    amount  = DecimalField(20,2)

    def amount_string(self):
        return config.l10n.currency(self.amount,grouping=True)

    def today(self):
        res = 0
        try:
            list = SaleInstallment.select().where(SaleInstallment.dateback == getDate())
            res = list.count()
        except:
            res = 0
        return res

    def appointed(self):
        today = datetime.today()
        enddate = today + timedelta(days=7)
        count = SaleInstallment.select() \
            .where((SaleInstallment.dateback.is_null()) & (SaleInstallment.date > enddate)) \
            .count()

        return count

class StorageChange(BaseModel):
    storage = ForeignKeyField(Storage,related_name='storages')
    product = ForeignKeyField(Product,related_name='products')
    enter = IntegerField(default=0)
    export = IntegerField(default=0)
    purchase = DecimalField(20,2,default=0.0)
    sell = DecimalField(20,2,default=0.0)
    date = CharField()
    time = CharField()
    reftype = IntegerField()
    refid = IntegerField()

    def current(self):
        return self.storage_current(self.storage)
        #self.entrance() - self.egress()

    def entrance(self):
        return StorageChange.select(fn.Sum(StorageChange.enter)
                                    .alias('entrance')) \
            .where(StorageChange.product==self.product) \
            .get() \
            .entrance

    def storage_entrance(self,storage):

        et= StorageChange.select(fn.Sum(StorageChange.enter)
                                 .alias('entrance')) \
            .where((StorageChange.product==self.product) & (StorageChange.storage==storage)) \
            .get() \
            .entrance
        if et==None:
            et=0
        return et

    def egress(self):
        return StorageChange.select(fn.Sum(StorageChange.export)
                                    .alias('egress')) \
            .where(StorageChange.product==self.product) \
            .get() \
            .egress

    def storage_egress(self,storage):
        eg= StorageChange.select(fn.Sum(StorageChange.export)
                                 .alias('egress')) \
            .where((StorageChange.product==self.product) & (StorageChange.storage==storage)) \
            .get() \
            .egress
        if eg==None:
            eg=0
        return eg

    def storage_current(self,storage):
        et = self.storage_entrance(storage)
        eg = self.storage_egress(storage)
        return et - eg

    def purchase_string(self):
        return config.l10n.currency(self.purchase,grouping=True)

    def sell_string(self):
        return config.l10n.currency(self.sell,grouping=True)

    def total_purchase(self):
        return self.current() * self.purchase

    def total_purchase_string(self):
        return config.l10n.currency((self.current() * self.purchase),grouping=True)

    def total_sale(self):
        q = float(self.current())
        s = float(self.sell)
        return q * s

    def total_sale_string(self):
        return config.l10n.currency((self.current() * self.sell),grouping=True)
