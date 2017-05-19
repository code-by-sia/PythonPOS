import hashlib
from symbol import try_stmt

__author__ = 'SiamandMaroufi'

import datetime,math,os,gettext,locale,csv,re
from datetime import date, time, timedelta
from http.server import BaseHTTPRequestHandler,HTTPServer
import collections
from datetime import datetime
from peewee import *
import mimetypes
import pystache
import json
from cgi import FieldStorage, parse_qs
from urllib.parse import urlparse

class config:
    __author__ = 'SiamandMaroufi'

    server_path = os.path.dirname(os.path.realpath(__file__))
    lang_name ='fa'
    app_lang    = [lang_name]
    app_locale  = 'en_US'
    app_db_user = 'root';
    app_db_pass  = '';


    i18n_language = gettext.translation('default','locale',app_lang)
    i18n = i18n_language.gettext
    _ = i18n


    locale.setlocale(locale.LC_ALL,app_locale)
    l10n = locale


    CompanyName = _('CompanyName')



    def makeTempLang(menus):
        fs = getFiles('templates/')
        words = []
        regex =re.compile("\{\{\#\_\}\}(.*)\{\{/\_\}\}")

        for f in fs:
            try:
                data=open(f,'r').read()
                fwords=re.findall(regex, data)
                words.extend(fwords)

            except:
                pass

        clean = (words[4:])
        data='from core import config\n_=config.i18n\n'

        for menu in menus:
            data = "%s_('%s')\n" %(data,menu.title)

        for c in clean:
            data = "%s_('%s')\n"%(data,c)
        open('locale/temp2.py','w+').write(data)

        pass

    def getFiles(spath=''):
        res =[]
        arr = os.listdir(spath)
        for d in arr:
            dpath =os.path.join(spath,d)
            if d.endswith('.htm'):
                res.append(dpath)
            if os.path.isdir(dpath):
                sub=getFiles(dpath)
                if len(sub) > 0 :
                    res.extend(sub)
        return res


sqlitedb_test   = SqliteDatabase(config.server_path + '/test.db')
sqlitedb        = SqliteDatabase(config.server_path + '/database.db')
mysqldb         = MySQLDatabase('accdb',host='127.0.0.1',user=config.app_db_user,passwd=config.app_db_pass)
serverdb    =  sqlitedb

# Classes

class AuthControler:
    Authenticated = False
    SessionObject = None
    Token = 'NONE'

    def __init__(self,router):

        self.router=router
        self.request=router.request
        token = self.router.getCookie('token')

        if(token != None):
            try:
                session = Session.get((Session.token==token) & (Session.status==1))
                self.Authenticated=True
                self.SessionObject=session
                self.Token = session.token
            except:
                self.Authenticated=False
                self.SessionObject=None
                self.Token='NONE'

        pass



class Template(object):


    '''
    classdocs
    '''
    output  = ""
    mimetype="text/html"
    statuscode=200
    request = None
    query   = None
    cookies = {}
    authentication=None

    query_parts = None
    post_form   = None
    post_form_calced = False

    def setCookie(self,name,value,path='/'):
        self.cookies[name]=value
        pass

    def getForm(self):
        if self.post_form_calced == True:
            return self.post_form

        self.post_form_calced =True
        try:
            req   = self.request
            form  = FieldStorage(
                fp=req.rfile,
                headers=req.headers,
                environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':req.headers['Content-Type']}
            )
            self.post_form = form
            return form
        except:
            return None

    def Req(self,keyname):
        Obj = self.GET(keyname)

        if Obj==None or Obj=='' :
            if self.getForm()!=None:
                Obj= self.getForm().getvalue(keyname)
        if Obj==None:
            Obj=0;
        return Obj

    def ToInt(self,Obj):
        strv = re.sub("[^0-9\-]", "",str(Obj))
        if strv=='':
            return 0
        else:
            try:
                return int(strv)
            except:
                return 0;


    def StringReq(self,keyname):
        Obj = self.Req(keyname)
        if Obj==None :
            return ''
        else:
            return str(Obj)

    def IntReq(self,keyname):
        Obj = self.Req(keyname)
        if Obj==None:
            return 0
        else:
            strv = re.sub("[^0-9\-]", "",str(Obj))
            if strv=='':
                return 0
            else:
                try:
                    return int(strv)
                except:
                    return 0;

    def FloatReq(self,keyname):
        Obj = self.Req(keyname)
        if Obj==None:
            return 0
        else:
            strv = re.sub("[^0-9\-\.]", "",str(Obj))
            if strv=='':
                return 0
            else:
                try:
                    return float(strv)
                except:
                    return 0.0

    def getQueryString(self):
        if  self.query_parts == None:
            self.query_parts = parse_qs(self.query)
        return self.query_parts

    def GET(self,keyname):
        qp = self.getQueryString()
        rd = ['']
        if keyname in qp:
            rd = qp[keyname]
        if len(rd)==1 :
            return rd[0]
        else :
            return rd

    def extractCookies(self):

        if len(self.cookies) ==0:
            if "Cookie" in self.request.headers:
                try:
                    data = self.request.headers['Cookie']
                    if len(data)>0:
                        rows = (data.split(';'))
                        for row in rows:
                            cell =row.strip().split('=')
                            self.cookies[cell[0]]=cell[1]
                except:
                    pass

    def getCookie(self,cookiename):
        try:
            self.extractCookies()
            return self.cookies[cookiename]
        except:
            return None

    def getTemplate(self,filename):
        file = open( config.server_path + "/templates/" +filename,'r')
        outp = file.read()
        return outp

    def NotImplemented(self,section):
        self.RenderFile('error/not-implemented.htm',{'section':section})

    def RenderJSON(self,data):
        self.output = json.dumps(data)

    def RenderFile(self,filename,args=None):
        fpath = config.server_path + "/templates/" + filename
        mimetypes.add_type('image/svg+xml','.svg')
        mimetypes.add_type('application/x-font-woff','.woff')
        mime = mimetypes.guess_type(fpath)
        if(len(mime)>1):
            self.mimetype = mime[0]

        translate = False
        if self.mimetype in ('text/html','text/xml','application/xml'):
            translate = True



        # try:
        file = open(fpath,'rb')
        outp = file.read()
        if isinstance(outp,bytes):
            outp = outp.decode('utf-8')
        if translate:
            outp = pystache.render(outp,args)
         #.encode('utf-8')
        self.output += outp

        pass

    def Translate(self):
        outp = self.output

        outp = outp.decode('utf-8')
        outp = pystache.render(outp,{'_':config.i18n})
        outp = outp.encode('utf-8')

        self.output = outp


    def Render(self):
        return self.output

    def Currency(self,number):
        if number == None:
            number = 0
        return config.l10n.currency(number,grouping=True)

    def Echo(self,q):
        self.output += q

    def EchoTag(self,name,value):
        self.Echo("<%s>%s</%s>"%(name,value,name))

class MainRouter(Template):
    def __init__(self,reuqest):

        self.request=reuqest
        self.authentication = AuthControler(self)
        pass

    def RenderFile(self,filename):
        file = open(config.server_path + "/templates/" + filename ,'r')
        outp = file.read()
        self.output += outp
        pass

    def Route(self):
        path = self.request.path
        parsed_path = urlparse(path)

        full_path = parsed_path.path
        spath  = full_path.split('/',2)

        fpath='empty'
        if len(spath)>2 :
            fpath= spath[2]
        section = spath[1]
        mdl = Container()

        if(section == ''):
            mdl=Container()
        elif(section =='static'):
            mdl = Static()
        elif(section=='system'):
            mdl = System()
        elif(self.authentication.Authenticated):

            if(section=='auth'):
                mdl = Authentication()
            elif section=='dashboard':
                mdl = Dashboard()
            elif(section=='info'):
                mdl = BasicInfo()
            elif section=='sale':
                mdl=Sales()
            elif section=='purchase':
                mdl = Purchase()
            elif(section=='test'):
                mdl = TestDev()
            elif section=='report':
                mdl= Report()
            elif section=='viewer':
                mdl= Viewer()
            elif section=='confirm':
                mdl = Confirm()
            elif section=='template':
                mdl = ReportTemplate()

        else:
            mdl= Static()
            fpath='security.htm'

        mdl.router  = self
        mdl.query   = parsed_path.query
        mdl.request = self.request
        mdl.authentication=self.authentication
        mdl.Process(fpath)

        return mdl

class RequestHandler(BaseHTTPRequestHandler):
    '''
    classdocs
    '''

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_GET(self):
        ProcessRequeset(self)

    def do_POST(self):
        ProcessRequeset(self)

class BaseModel(Model):

    # @classmethod
    # def update(cls, **update):
    #     update['modified'] = datetime.now()
    #     return super(Model, cls).update(**update)

    @classmethod
    def backup_table(cls, csvfile):
        """
        Create a schema less backup of this model in a csv file.
        """
        query = cls.select()
        if csvfile.tell():
            desc = csvfile.fileno()
            modified = datetime.fromtimestamp(os.path.getmtime(desc))
            query = query.where(cls.modified > modified)
        writer = csv.writer(csvfile)
        writer.writerows(query.naive().tuples())

    @classmethod
    def restore_table(cls, csvfile):
        """
        Restore this model from a csv file.
        """
        latest_id = cls.select(fn.Max(cls.id).alias('latest_id')).scalar()

        # last_id = cls.select(cls.id).

        # reader = csv.reader(csvfile)

        # for row in reader:
            # print(row[0])

    class Meta:
        database =serverdb

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
                    )\
                    .join(Sale)\
                    .where(Sale.user==self)\
                    .group_by(User,Sale.date)\
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
                                        fn.Sum(StorageChange.enter * StorageChange.purchase).alias('total'))\
                                        .where((StorageChange.storage == self)
                                               & (StorageChange.export == 0)
                                               & (StorageChange.reftype == 1)).get()
            total_purchase = sc.total
            sc = StorageChange.select(
                                        fn.Sum(StorageChange.export * StorageChange.purchase).alias('total'))\
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
                                   ).where(StorageChange.storage == self)\
                                    .group_by(StorageChange.product,StorageChange.storage)
        return res

    def total_capacity(self):
        try:
            sc = StorageChange.select(
                        fn.Sum(StorageChange.enter * StorageChange.purchase).alias('total'))\
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
        list = SaleInstallment.raw("SELECT * ,datediff(date,curdate()) as 'deadline' FROM `saleinstallment` WHERE (dateback is null)  having deadline < 5 order by deadline asc")
        count = 0
        for li in list:
            count += 1
        # try:
        #     list = SaleInstallment.raw("SELECT * ,datediff(date,curdate()) as 'deadline' FROM `saleinstallment` WHERE (dateback is null)  having deadline < 1000 order by deadline asc")
        #     res = list.count()
        #     print(res)
        # except:
        #     res = 0
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
                            .alias('entrance'))\
                            .where(StorageChange.product==self.product)\
                            .get()\
                            .entrance

    def storage_entrance(self,storage):

        et= StorageChange.select(fn.Sum(StorageChange.enter)
                            .alias('entrance'))\
                            .where((StorageChange.product==self.product) & (StorageChange.storage==storage))\
                            .get()\
                            .entrance
        if et==None:
            et=0
        return et

    def egress(self):
        return StorageChange.select(fn.Sum(StorageChange.export)
                            .alias('egress'))\
                            .where(StorageChange.product==self.product)\
                            .get()\
                            .egress

    def storage_egress(self,storage):
        eg= StorageChange.select(fn.Sum(StorageChange.export)
                            .alias('egress'))\
                            .where((StorageChange.product==self.product) & (StorageChange.storage==storage))\
                            .get()\
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

class DbSetup(object):
    def BackUp(self):
        with open('backups/menu.csv','a+') as csvfile:
            Menu.backup_table(csvfile)

    def SetupDataBase(self):
        serverdb.connect()

        # print "start"

        User.create_table()
        Role.create_table()
        UserRole.create_table()
        Session.create_table()
        Permission.create_table()
        UserPermission.create_table()
        RolePermission.create_table()
        SessionPermission.create_table()
        Menu.create_table()
        Person.create_table()
        Cost.create_table()
        Supplier.create_table()
        Group.create_table()
        Storage.create_table()
        Person.create_table()
        Order.create_table()
        Product.create_table()
        Sale.create_table()
        SaleDetails.create_table()
        SaleInstallment.create_table()
        StorageChange.create_table()

        # print "complete"

class Costs(Template):
    def Process(self,section):
        if section=='costs.manage':
            list = Cost.select()
            self.RenderFile('cost/manage.htm',{'_':config.i18n,'Costs':list})
        elif section=='costs.new':
            cost = Cost()
            self.RenderFile('cost/cost.htm',{'_':config.i18n,'Cost':cost})
        elif section=='costs.delete':
            id=self.IntReq('id')
            cost = Cost.get(Cost.id==id)
            cost.delete_instance()
            self.RenderJSON({'result':'OK'})
        elif section=='costs.save':
            id = self.IntReq('id')
            new_title = self.StringReq('title')
            new_invoiceno = self.StringReq('invoiceno')
            new_amount = self.FloatReq('amount')

            try:
                cost = Cost.get(Cost.id == id)
            except:
                cost=Cost()
                cost.regtime=''
                cost.regdate=''

            if cost != None:
                cost.title=new_title
                cost.invoiceno=new_invoiceno
                cost.amount=new_amount
                cost.save()

        elif section=='costs.edit':
            id = self.IntReq('id')
            cost = Cost.select().where(Cost.id==id).get()
            self.RenderFile('cost/cost.htm',{'_':config.i18n,'Cost':cost})

class Authentication(Template):
    '''
    classdocs
    '''

    def Process(self, section):
        if section=='users':
            self.RenderFile('auth/user.manage.htm',{'_':config.i18n,'users':User.select()})
        elif section=='user.list':
            users = User.select()
            for user in users:
                fields = (user.username)
                self.output = '%s<tr class="bigrow"><td>10000</td><td>%s</td><td></td><td></td><td></td><td></td>s</tr>' % (self.output,fields)
        elif section=='changepwd':
            self.RenderFile('auth/password.change.htm',{'_':config.i18n})
        elif section=='roles':
            self.output='fch'
        else:
            self.NotImplemented(section)

class Static(Template):
    def Process(self, filename):
        filepath = config.server_path + "/templates/static/" + filename

        mimetypes.add_type('image/svg+xml','.svg')
        mimetypes.add_type('application/x-font-woff','.woff')

        mime = mimetypes.guess_type(filepath)
        if len(mime)>0:
            self.mimetype = mime[0]
        self.file=filepath
        with open(filepath,'rb') as cfile:
            self.output=cfile.read()

class Container(Template):
    def Process(self,args):
        if(self.authentication.Authenticated==True):
            menu = Menu.select().where((Menu.parent>>None)|(Menu.parent>>0))

            now  = getDate()
            _ = config.i18n
            user = self.authentication.SessionObject.user
            fullname = "%s %s" % (user.name,user.family)

            args = {'Title':_('Accounting Web Application'),'Today':now,'lang':config.lang_name,'UserName':fullname,'Navigation':menu,'_':_}

            self.RenderFile("container/main.htm",args)
        else:
            self.RenderFile("container/login.htm",{'_':config.i18n,'time':getTime()})

class Dashboard(Template):

    def Process(self,section):

        if section == 'instulments':
            insts = SaleInstallment.raw("SELECT * ,datediff(date,curdate()) as 'deadline' FROM `saleinstallment` WHERE (dateback is null)  having deadline < 5  order by deadline asc")
            i = 1
            for inst in insts:
                inst.index = i
                i += 1
            self.RenderFile('dashboard/instulments.htm',{'insts':insts,'_':config.i18n})

        elif section == 'charts':
            users = User.select()
            storages = Storage.select()

            order = Order()
            inst = SaleInstallment()
            sale = Sale()

            self.RenderFile('dashboard/charts.htm',{
                'users':users,
                'storages':storages,
                'order':order,
                'inst':inst,
                'sale':sale,
                '_':config.i18n})
        else:
            users = User.select()
            storages = Storage.select()

            order = Order()
            inst = SaleInstallment()
            sale = Sale()

            self.RenderFile('dashboard/home.htm',{
                'users':users,
                'storages':storages,
                'order':order,
                'inst':inst,
                'sale':sale,
                '_':config.i18n})

class BasicInfo(Template):
    '''
    classdocs
    '''

    def Process(self, section):
        # Open a form in order to save or update
        if section=='person.new':
            person = Person()
            person.id = 0
            self.RenderFile('person/person.htm',{'_':config.i18n,'person':person})

        elif section=='supplier.new':
            supplier = Supplier()
            supplier.id = 0
            self.RenderFile('supplier/supplier.htm',{'_':config.i18n,'supplier':supplier})

        elif section == 'group.new':
            group = Group()
            group.id = 0
            self.RenderFile('group/group.htm',{'_':config.i18n,'group':group})

        elif section == 'storage.new':
            storage = Storage()
            storage.id = 0
            self.RenderFile('storage/storage.htm',{'_':config.i18n,'storage':storage})

        elif section=='cost.new':
            cost = Cost()
            cost.id = 0
            self.RenderFile('cost/cost.htm',{'_':config.i18n,'cost':cost})

        # Open a form with fields filled with data to update
        elif section=='person.edit':
            id = self.IntReq('id')
            person = Person.get(Person.id==id)
            self.RenderFile('person/person.htm',{'_':config.i18n,'person':person})

        elif section=='supplier.edit':
            id = self.IntReq('id')
            supplier = Supplier.get(Supplier.id==id)
            self.RenderFile('supplier/supplier.htm',{'_':config.i18n,'supplier':supplier})

        elif section == 'group.edit':
            id = self.IntReq('id')
            group = Group().get(Group.id == id)
            self.RenderFile('group/group.htm',{'_':config.i18n,'group':group})

        elif section == 'storage.edit':
            id = self.IntReq('id')
            storage = Storage().get(Storage.id == id)
            self.RenderFile('storage/storage.htm',{'_':config.i18n,'storage':storage})

        elif section == 'cost.edit':
            id = self.IntReq('id')
            cost = Cost().get(Cost.id == id)
            self.RenderFile('cost/cost.htm',{'_':config.i18n,'cost':cost})


        # Send save operation to the controler
        elif section=='person.save':
            id = self.IntReq('id')
            try:
                p = Person.get(Person.id == id)
            except:
                p=Person()
            p.name = self.StringReq('name')
            p.city = self.StringReq('city')
            p.phone = self.StringReq('phone')
            p.email = self.StringReq('email')
            p.address = self.StringReq('address')
            p.save()

            self.RenderJSON({'Result': 'success','id':p.id});
        elif section=='supplier.save':
            id = self.IntReq('id')
            try:
                s = Supplier.get(Supplier.id == id)
            except:
                s=Supplier()
            s.name      = self.StringReq('name')
            s.manager   = self.StringReq('manager')
            s.tell      = self.StringReq('tell')
            s.field     = self.StringReq('field')
            s.save()

            self.RenderJSON({'Result': 'success','id':s.id});

        elif section == 'group.save':
            id = self.IntReq('id')
            try:
                g = Group.get(Group.id == id)
            except:
                g = Group()

            g.name = self.StringReq('name')
            g.unit = self.StringReq('unit')
            g.save()
            self.RenderJSON({'Result':'success','id':g.id})

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
            self.RenderJSON({'Result':'success','id':st.id})

        elif section == 'cost.save':
            id = self.IntReq('id')
            try:
                ct = Cost.get(Cost.id == id)
            except:
                ct = Cost()

            ct.regdate = self.StringReq('regdate')
            ct.regtime = self.StringReq('regtime')
            ct.title        = self.StringReq('title')
            ct.invoiceno    = self.StringReq('invoiceno')
            ct.amount       = self.FloatReq('amount')

            ct.save()
            self.RenderJSON({'Result':'success','id':ct.id})

        elif section=='person.check':
            self.output =''

        elif section=='person.filter':
            list = Person.select()
            args = {'data':list,'_':config.i18n}
            self.RenderFile('person/list.htm',args)


         # Delete section for each item
        elif section == 'group.delete':
            id = self.IntReq('id')
            group = Group.get(Group.id==id)
            group.delete_instance()
            self.RenderJSON({'result':'OK'})

        elif section == 'supplier.delete':
            id = self.IntReq('id')
            supplier = Supplier.get(Supplier.id==id)
            supplier.delete_instance()
            self.RenderJSON({'result':'OK'})

        elif section == 'storage.delete':
            id = self.IntReq('id')
            storage = Storage.get(Storage.id==id)
            storage.delete_instance()
            self.RenderJSON({'result':'OK'})

        elif section == 'person.delete':
            id = self.IntReq('id')
            person = Person.get(Person.id==id)
            person.delete_instance()
            self.RenderJSON({'result':'OK'})

        elif section == 'cost.delete':
            id = self.IntReq('id')
            cost = Cost.get(Cost.id==id)
            cost.delete_instance()
            self.RenderJSON({'result':'OK'})


        # Manage section for items
        elif section=='person.manage':
            self.RenderFile('person/manage.htm',{'_':config.i18n,'persons':Person.select()})

        elif section=='supplier.manage':
            args = {'_':config.i18n,'suppliers':Supplier.select()}
            self.RenderFile('supplier/manage.htm', args)

        elif section == 'group.manage':
            list = Group.select()
            args = {'groups':list,'_':config.i18n}
            self.RenderFile('group/manage.htm',args)

        elif section == 'storage.manage':
            list = Storage.select()
            args = {'storages':list,'_':config.i18n}
            self.RenderFile('storage/manage.htm',args)

        elif section == 'cost.manage':
            list = Cost.select()
            args = {'costs':list,'_':config.i18n}
            self.RenderFile('cost/manage.htm',args)

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
                    '_':config.i18n}
            self.RenderFile('person/history.htm',args)

        elif section == 'group.goodlist':
            id = self.IntReq('id')
            g = Group.get(Group.id == id)
            args = {'group':g,'products':g.products.group_by(Product.name),'_':config.i18n}
            self.RenderFile('group/goodlist.htm',args)

        elif section == 'storage.goodlist':
            id = self.IntReq('id')
            is_JSON = (self.IntReq('json') != 0)
            s = Storage.get(Storage.id == id)
            args = {'_':config.i18n,'storage':s,'products':s.goodlist()}
            if is_JSON :
                ps = []
                for p in s.goodlist():
                    pr = p.purchase_string()
                    sl = p.sell_string()
                    ps.append({'id':p.product.id,'name':p.product.name,'qty':p.storage_current(s),'purchase':pr,'sale':sl})
                self.RenderJSON(ps)
            else:
                self.RenderFile('storage/goodlist.htm',args)

        elif section == 'supplier.purchaselist':
            id = self.IntReq('id')
            s = Supplier.get(Supplier.id == id)
            products = Product.select().join(Order).where(Order.supplier == s)
            i=1
            for p in products:
                p.index = i
                i=i+1
            args = {'supplier':s,'products':products,'_':config.i18n}
            self.RenderFile('supplier/purchaselist.htm',args)

        elif section == 'person.instullment':
            id = self.IntReq('id')
            inst = SaleInstallment.get(SaleInstallment.id == id)
            inst.currentdate = getDate()
            args = {'inst':inst,'_':config.i18n}
            self.RenderFile('person/instullment.htm',args)
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

            self.RenderJSON({'result':'ok','id':si.id,'amount':si.amount,'dateback':si.dateback})
        else:
            self.NotImplemented(section)

class Confirm(Template):
    def Process(self,section):
        if section == 'purchase':
            purchases = Order.select().where(Order.verified == 0)
            self.RenderFile('confirm/purchase.htm',{'_':config.i18n,'purchases':purchases})

        elif section =='purchase.details':
            id = self.IntReq('id')
            products = Product.select().where(Product.order == Order.get(Order.id == id))
            self.RenderFile('confirm/purchase.details.htm',{'_':config.i18n,'products':products})

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
                        sc = StorageChange.get((StorageChange.product == product) & (StorageChange.storage == o.storage))
                        sc.enter += product.quantity
                    except:
                        sc          = StorageChange()
                        sc.storage  = o.storage
                        sc.product  = product
                        sc.date     = getDate()
                        sc.time     = getTime()
                        sc.enter    = product.quantity
                        sc.purchase = product.purchase
                        sc.sell     = product.sale
                        sc.reftype = 1
                        sc.refid = o.id

                    sc.save()


                self.RenderJSON({'result':'OK'})
            except:
                self.RenderJSON({'result':'NO'})

        elif section == 'sale':
            sales = Sale.select().where(Sale.verified == 0)
            self.RenderFile('confirm/sale.htm',{'_':config.i18n,'sales':sales})

        elif section =='sale.details':
            sale = Sale.get(Sale.id==self.IntReq('id'))
            details = sale.details
            i=1
            for detail in details:
                detail.index=i
                i=i+1

            customers= Person.select()
            storages  = Storage.select()

            for cus in customers:
                if cus == sale.customer:
                    cus.selected=True


            self.RenderFile('confirm/sale.details.htm',{
                '_':config.i18n,
                'Sale':sale,
                'Sale_details':details,
                'Storages':storages,
                'Customers':customers
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

                self.RenderJSON({'result':'OK'})
            except:
                self.RenderJSON({'result':'NO'})

class Purchase(Template):
    '''
    classdocs
    '''

    def Process(self, section):

        if section=='new':
            order = Order()
            storages = Storage.select()
            suppliers= Supplier.select()
            groups   = Group.select();
            order.id=0
            self.RenderFile('purchase/order.htm',{
                '_':config.i18n,
                'order':order,
                'storages':storages,
                'suppliers':suppliers,
                'group-list':groups
            })
        elif section=='edit':
            order = Order.get(Order.id==self.IntReq('id'))

            storages = Storage.select()
            suppliers= Supplier.select()
            groups   = Group.select();
            products = order.details

            for sup in suppliers:
                if sup == order.supplier :
                    sup.selected=True

            for stg in storages:
                if stg==order.storage:
                    stg.selected=True

            self.RenderFile('purchase/order.htm',{
                '_':config.i18n,
                'order':order,
                'storages':storages,
                'suppliers':suppliers,
                'group-list':groups,
                'products':products
            })
        elif section=='save':
            id          = self.IntReq('id')
            storageId   = self.IntReq('storageId')
            supplierId  = self.IntReq('supplierId')



            try:
                order = Order.get(Order.id == id)
            except:
                order = Order()
                order.date=getDate()
                order.time=getTime()
                order.verified= False

            supplier = Supplier.get(Supplier.id == supplierId)
            storage  = Storage.get(Storage.id == storageId)

            order.supplier = supplier
            order.storage  = storage
            order.user     = self.authentication.SessionObject.user
            order.save()


            form = self.getForm()
            row_ids =[]
            for key in form.keys():
                if key[0]=='g':
                    id = self.ToInt(key[(key.find('[')+1):key.find(']')])
                    row_ids.append(id)
            row_ids.sort()
            keep_rows=[]

            pids =[]
            #order.clearDetails()

            for row_id in row_ids:
                x=str(row_id)
                group_id    = self.IntReq('g[' + x + ']')
                product_id  = self.IntReq('i[' + x + ']')

                group = Group.get(Group.id == group_id)
                p = Product()

                if product_id > 0 :
                    p= Product.get(Product.id==product_id)

                p.order     = order
                p.group     = group
                p.name      = self.StringReq('n[' + x + ']')
                p.purchase  = self.FloatReq ('p[' + x + ']')
                p.sale      = self.FloatReq ('s[' + x + ']')
                p.quantity  = self.FloatReq ('q[' + x + ']')
                p.save()
                pids.append(p.id)
            order.clearDetails(pids)
            self.RenderJSON({'Id':order.id})
        elif section == 'manage':
            orders = Order.select()
            self.RenderFile('purchase/manage.htm',{'_':config.i18n,'purchases':orders})

class Sales(Template):
    def Process(self,section):
        if section=='new':
            customers = Person.select()
            storages  = Storage.select()
            sale = Sale()
            sale.id = 0
            sale.advance = 0
            sale.date = getDate()
            self.RenderFile('sale/sale.htm',{
                '_':config.i18n,
                'Customers':customers,
                'Storages' :storages,
                'Sale':sale
            })
        elif section=='edit':
            sale = Sale.get(Sale.id==self.IntReq('id'))

            details = sale.details
            i=1
            for detail in details:
                detail.index=i
                i=i+1
            i=1

            installments = sale.installments
            for si in installments:
                si.index = i
                i=i+1

            customers= Person.select()
            storages  = Storage.select()

            for cus in customers:
                if cus == sale.customer:
                    cus.selected=True


            self.RenderFile('sale/sale.htm',{
                '_':config.i18n,
                'Sale':sale,
                'Sale_details':details,
                'Sale_installments':installments,
                'Storages':storages,
                'Customers':customers
            })
        elif section=='save':
            id     = self.IntReq('id')
            pays   = self.IntReq('pays')
            prepaid= self.FloatReq('prepaid')
            customerId  = self.IntReq('customerId')

            try:
                sale = Sale.get(Sale.id == id)
            except:
                sale      = Sale()
                sale.date = getDate()
                sale.time = getTime()
                sale.user = self.authentication.SessionObject.user
                sale.verified= False
            customer = Person.get(Person.id == customerId)

            sale.customer    = customer
            sale.installment = pays
            sale.advance    = prepaid
            sale.payment    = 0
            sale.fullsale   = 0

            sale.save()

            form = self.getForm()
            row_ids =[]
            srow_ids=[]
            for key in form.keys():
                if key[0]=='g':
                    id = self.ToInt(key[(key.find('[')+1):key.find(']')])
                    row_ids.append(id)
                elif key[0]=='b':
                    id = self.ToInt(key[(key.find('[')+1):key.find(']')])
                    srow_ids.append(id)

            row_ids.sort()
            srow_ids.sort()

            sale.clearDetails()
            full_sale = 0

            for row_id in row_ids:
                x=str(row_id)
                storage_id  = self.IntReq('g[' + x + ']')
                product_id  = self.IntReq('p[' + x + ']')
                sale_price  = self.FloatReq('s[' + x + ']')
                sale_qty    = self.FloatReq('q[' + x + ']')
                full_sale  += sale_price * sale_qty


                detail = SaleDetails()
                detail.sale = sale
                detail.product = Product.get(Product.id==product_id)
                detail.quantity= sale_qty
                detail.saleprice =sale_price
                detail.storage = Storage.get(Storage.id==storage_id)
                detail.save()

                schange = StorageChange()
                schange.storage = detail.storage
                schange.product = detail.product
                schange.enter   = 0
                schange.export  = sale_qty
                schange.purchase= detail.product.purchase
                schange.sell    = sale_price
                schange.date    = sale.date
                schange.time    = sale.time
                schange.reftype = 2
                schange.refid   = sale.id
                schange.save()



            for row_id in srow_ids:
                x=str(row_id)
                date= self.StringReq('b_d[' + x + ']')
                pay = self.FloatReq('y_p[' + x + ']')

                sins = SaleInstallment()
                sins.sale=sale
                sins.date = date
                sins.amount=pay
                sins.save()

            sale.fullsale = full_sale
            sale.save()
            self.RenderJSON({'Id':sale.id})

        elif section=='manage':
            sales = Sale.select()
            self.RenderFile('sale/manage.htm',{'_':config.i18n,'sales':sales})
        elif section=='return':
            self.output='Return'
        elif section=='installments':
            saleId = self.IntReq('SaleId')
            pqty   = self.IntReq('Pays')
            sale = Sale.get(Sale.id == saleId)

            if pqty != sale.installment:
                sale.installment = pqty
                sale.save()
                sale.createInstallments()

            i=0
            for ins in sale.installments:
                i = i + 1
                ins.index = i
            self.RenderFile('sale/installments.htm',{'_':config.i18n,'sale':sale})

class System(Template):

    def Process(self,fpath):
        if(fpath=='login'):
            self.Login()
        elif(fpath=='logout'):
            self.Logout()
        pass

    def Login(self):

        self.mimetype='application/json'
        # form = self.getQueryString()

        username = self.Req('username')
        password = self.Req('password')

        session =None
        # if(form.has_key('username') and form.has_key('password')):
        if username != None and password != None:
            # username = form['username']
            # passowrd = form['password']
            session= Session().Login(username,password)


        if(session != None):
            self.setCookie('token',session.token)
            self.output='{status:1}'
        else:
            self.output= '{status:0}'

    def Logout(self):
        try:
            if(self.authentication.Authenticated):
                session= self.authentication.SessionObject
                session.Logout()
            self.output='<script>location.reload()</script>'
        except:
            self.output='{status=-1}'

class TestDev(Template):
    '''
    classdocs
    '''

    def ReadCookie(self):
        if "Cookie" in self.headers:
            c = SimpleCookie(self.headers["Cookie"])
            return c['value'].value
        return None



    def Process(self,fpath):
        '''
        Constructor
        '''
        if(fpath=='save'):
            self.Save()
        elif fpath=='lang':
            self.output = config.app_lang[0]
        elif fpath=='ch-lang':
            config.ChangeLanguage(self.StringReq('lang'))
        else :
            self.output=fpath +  "<br ><form action='/test/save' method='post' ><input name='a'/><button>send</button></form>"

    def Save(self):
        a=self.FloatReq('a')
        self.output = self.Currency(a) + ' is value'

class Viewer(Template):

    def Process(self,section):
        self.Echo('<iframe class="viewer" src="/report/' + section+'" />')

class Report(Template):

    report = None
    headers= None

    Name ='Report'

    def __init__(self):
        self.headers=[]

    def Header(self):
        _ = config.i18n
        self.output  = '<?xml version="1.0" encoding="UTF-8" ?>'
        self.output += '<?xml-stylesheet type="text/xsl" href="/template/' + self.report.Name + '" ?>'
        self.output += '<Viewer>'
        self.output += '<Report name="'+ _(self.report.Name) +'" >'
        if(len(self.report.headers)>0):
            self.Echo("<Header>")
            for header in self.report.headers:
                key = str(header[0])
                val = (header[1])
                val=str(val)
                self.EchoTag(key,val)
            self.Echo("</Header>")


    def Footer(self):
        self.output += '</Report>'
        self.output += '</Viewer>'


    def generate(self):

        pass

    def Process(self,section):
        if section=='order':
            self.report = OrderReport()
        elif section=='sale':
            self.report = SaleReport()
        elif section=='sale-list':
            self.report = SaleListReport()
        elif section=='storage':
            self.report = StorageReport()
        elif section=='cost':
            self.report = CostReport()
        elif section=='instullment':
            self.report = InstallmentReport()
        else:
            self.report = Report()

        self.report.query = self.query
        self.request = self.request
        self.report.generate()

        self.mimetype='text/xml'
        self.Header()
        self.output += self.report.output
        self.Footer()

class ReportTemplate(Template):

    def Process(self,section):

        self.mimetype='text/xsl'

        self.output  = '<?xml version="1.0" encoding="UTF-8"?>'
        self.output += '<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">'
        self.output += '<xsl:output method="html" />'
        self.RenderFile('reports/'+ section + '.xsl',{'_':config.i18n,'CompanyName':config.CompanyName})
        self.RenderFile('reports/report-footer.xsl',{'_':config.i18n})

class OrderReport(Report):
    Name ="order"

    def generate(self):
        orderId = self.IntReq('Id')

        try:
            order   = Order.get(Order.id==orderId)
        except:
            order   = Order.get()

        self.headers.append(('Id',str(order.id)))
        self.headers.append(('SupplierId',str(order.supplier.id)))
        self.headers.append(('SupplierName',order.supplier.name))
        self.headers.append(('Date',order.date))
        self.headers.append(('Time',order.time))
        self.headers.append(('DateTime',getDate()+' '+getTime()))
        self.headers.append(('Storage',order.storage.name))
        self.headers.append(('UserName',order.user.fullname()))

        self.Echo('<Page>')
        for row in order.details:
            self.Echo('<Row>')
            self.EchoTag('ProductId',row.id)
            self.EchoTag('ProductName',row.name)
            self.EchoTag('Category',row.group.name)
            self.EchoTag('Quantity',row.quantity)
            self.EchoTag('UnitPrice',row.purchase)
            self.EchoTag('FullPrice',row.full_purchase())
            self.Echo('</Row>')
        self.Echo('</Page>')

class SaleReport(Report):
    Name ="sale"

    def generate(self):

        saleId = self.IntReq('Id')
        try:
            sale   = Sale.get(Sale.id==saleId)
        except:
            sale   = Sale.get()

        self.headers.append(('Id',str(sale.id)))
        self.headers.append(('CustomerId',str(sale.customer.id)))
        self.headers.append(('CustomerName',sale.customer.name))
        self.headers.append(('Date',sale.date))
        self.headers.append(('Time',sale.time))
        self.headers.append(('DateTime',getDate()+' '+getTime()))
        self.headers.append(('Remain','0'))
        self.headers.append(('UserName',sale.user.fullname()))


        details = [d for d in sale.details]
        pages= split(details,_max_rows_)

        for page_details in pages:
            self.Echo('<Page>')
            for row in page_details:
                self.Echo('<Row>')
                self.EchoTag('ProductId',row.id)
                self.EchoTag('StorageName',row.storage.name)
                self.EchoTag('ProductName',row.product.name)
                self.EchoTag('Quantity',row.quantity)
                self.EchoTag('UnitPrice',row.saleprice)
                self.EchoTag('FullPrice',str(row.full_sale()))
                self.Echo('</Row>')
            self.Echo('</Page>')

class StorageReport(Report):
    Name = 'storage'

    def generate(self):

        storageId = self.IntReq('Id')
        try:
            storage = Storage.get(Storage.id == storageId)
        except:
            storage   = Storage.get()

        self.headers.append(('StorageName',storage.name))
        self.headers.append(('DateTime',getDate()+' '+getTime()))

        storages = Storage.select()
        for st in storages:
            self.Echo('<Storage>');
            self.EchoTag('Id',st.id)
            self.EchoTag('Name',st.name)
            self.Echo('</Storage>');

        list = storage.goodlist()
        list = [d for d in list]

        pages = split(list,_max_rows_)
        for list in pages:
            self.Echo('<Page>')
            for row in list:
                self.Echo('<Row>')
                self.EchoTag('ProductId',row.product.id)
                self.EchoTag('StorageName',row.storage.name)
                self.EchoTag('ProductName',row.product.name)
                self.EchoTag('CategoryName',row.product.group.name)
                self.EchoTag('Entrance',row.storage_entrance(storage))
                self.EchoTag('Egress',row.storage_egress(storage))
                self.EchoTag('Current',row.storage_current(storage))

                # self.EchoTag('UnitPrice',row.saleprice)
                # self.EchoTag('FullPrice',str(row.full_sale()))
                self.Echo('</Row>')
            self.Echo('</Page>')

class CostReport(Report):
    Name = 'cost'

    def generate(self):

        self.headers.append(('DateTime',getDate()+' '+getTime()))


        list = Cost().select()
        list = [d for d in list]

        pages = split(list,_max_rows_)
        for list in pages:
            self.Echo('<Page>')
            for row in list:
                self.Echo('<Row>')
                self.EchoTag('Title'    , row.title)
                self.EchoTag('InvoiceId', row.invoiceno)
                self.EchoTag('RegDate'  , row.regdate)
                self.EchoTag('Amount'   , row.amount)
                self.Echo('</Row>')
            self.Echo('</Page>')

class SaleListReport(Report):
    Name  = 'sale-list'

    def generate(self):

        username = self.StringReq('User')

        try:
            user = User.get(User.username == username)
        except:
            user = User.get()

        self.headers.append(('DateTime',getDate()+' '+getTime()))
        self.headers.append(('UserName',user.fullname()))

        list = user.salelist
        list = [d for d in list]

        users= User.select()
        for user in users:
            self.Echo('<User>')
            self.EchoTag('Id',user.username)
            self.EchoTag('UserName',user.fullname())
            self.Echo('</User>')

        pages = split(list,_max_rows_)
        for list in pages:
            self.Echo('<Page>')
            for row in list:
                self.Echo('<Row>')
                self.EchoTag('Id'  , row.id)
                self.EchoTag('Time', row.time)
                self.EchoTag('Customer' , row.customer.name)
                self.EchoTag('FullSale' , row.fullsale)
                self.EchoTag('Prepaid' , row.advance)
                self.EchoTag('Remain' , row.remind())
                self.Echo('</Row>')
            self.Echo('</Page>')

class InstallmentReport(Report):
    Name = 'installment'

    def generate(self):
        id= self.IntReq('id')
        pay = SaleInstallment.get(SaleInstallment.id==id)
        self.headers.append(('Serial',str(id)))
        self.headers.append(('Amount',str(pay.amount)))
        self.headers.append(('DateBack',pay.dateback))
        self.headers.append(('Date',pay.date))
        self.headers.append(('Remain',str(pay.  sale.remind())))
        self.headers.append(('DateTime',getDate()+' '+getTime()))
        self.headers.append(('SaleId',pay.sale.id))
        self.headers.append(('SaleDate',pay.sale.date))
        self.headers.append(('Customer',pay.sale.customer.name))


        self.Echo('<Page />');


_max_rows_ = 40;

def getDate():
    return date.today().strftime("%Y-%m-%d")

def getTime():
    return datetime.now().strftime("%H-%M-%S")

def addDate(date,y,m,d):
    date = datetime.datetime.strptime(date)
    return date + dated

def split(arr, size):
    if size < 1:
        size=1
    arrs = []
    while len(arr) > size:
        right = arr[:size]
        arrs.append(right)
        arr   = arr[size:]
    arrs.append(arr)
    return arrs

def ChangeLanguage(language):
    from  core import  config
    config.app_lang =[language]
    config.i18n_language = gettext.translation('default','locale',app_lang)
    config.i18n = i18n_language.gettext

def makeTempLang(menus):
    fs = getFiles('templates/')
    words = []
    regex =re.compile("\{\{\#\_\}\}(.*)\{\{/\_\}\}")

    for f in fs:
        try:
            data=open(f,'r').read()
            fwords=re.findall(regex, data)
            words.extend(fwords)

        except:
            pass

    clean = (words[4:])
    data='from core import config\n_=config.i18n\n'

    for menu in menus:
        data = "%s_('%s')\n" %(data,menu.title)

    for c in clean:
        data = "%s_('%s')\n"%(data,c)
    open('locale/temp2.py','w+').write(data)

    pass

def getFiles(spath=''):
    res =[]
    arr = os.listdir(spath)
    for d in arr:
        dpath =os.path.join(spath,d)
        if d.endswith('.htm'):
            res.append(dpath)
        if os.path.isdir(dpath):
            sub=getFiles(dpath)
            if len(sub) > 0 :
                res.extend(sub)
    return res

def ProcessRequeset(req):
    template = MainRouter(req).Route()
    template.Render()
    req.send_response(template.statuscode)
    req.send_header("Content-type", template.mimetype)
    if len(template.cookies) >0:
        # cookies_output = template.cookies.output(header='')
        cookies_output =""
        for key in template.cookies:
            cookies_output += ("%s=%s;Path=/;"%(key,template.cookies[key]))
        req.send_header('Set-Cookie',cookies_output )
    req.end_headers()


    fout = template.output
    if isinstance(fout,str):
        fout = bytes(fout.encode('utf-8'))

    req.wfile.write(fout)

if __name__ == '__main__':

   # glrobal _
    _= config.i18n

    PORT= int(os.getenv('PORT','8000'))
    HOST='localhost'
    httpd = HTTPServer((HOST,PORT),RequestHandler)

#    config.makeTempLang(Menu.select())
     #DbSetup().SetupDataBase()
    # DbSetup().BackUp()

    try:
        print (_('Samal web application server'))
        print (_('Starting server at')+' http://%s:%s' % (HOST,PORT))
        print ('>  %s - %s' % (getDate(),getTime()))
        httpd.serve_forever()
        httpd.server_close()
        print (_('End server listening'))
    except KeyboardInterrupt:
        print (_('Server is Stopped'))
        print ('>  %s - %s' % (getDate(),getTime()))
    pass
