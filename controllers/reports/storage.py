from common.config import _max_rows_, getDate, getTime, split
from common.report import Report
from models.models import Storage


class StorageReport(Report):
    Name = 'storage'

    def generate(self):

        storageId = self.IntReq('Id')
        try:
            storage = Storage.get(Storage.id == storageId)
        except:
            storage = Storage.get()

        self.headers.append(('StorageName', storage.name))
        self.headers.append(('DateTime', getDate() + ' ' + getTime()))

        storages = Storage.select()
        for st in storages:
            self.Echo('<Storage>');
            self.EchoTag('Id', st.id)
            self.EchoTag('Name', st.name)
            self.Echo('</Storage>');

        list = storage.goodlist()
        list = [d for d in list]

        pages = split(list, _max_rows_)
        for list in pages:
            self.Echo('<Page>')
            for row in list:
                self.Echo('<Row>')
                self.EchoTag('ProductId', row.product.id)
                self.EchoTag('StorageName', row.storage.name)
                self.EchoTag('ProductName', row.product.name)
                self.EchoTag('CategoryName', row.product.group.name)
                self.EchoTag('Entrance', row.storage_entrance(storage))
                self.EchoTag('Egress', row.storage_egress(storage))
                self.EchoTag('Current', row.storage_current(storage))

                # self.EchoTag('UnitPrice',row.saleprice)
                # self.EchoTag('FullPrice',str(row.full_sale()))
                self.Echo('</Row>')
            self.Echo('</Page>')

