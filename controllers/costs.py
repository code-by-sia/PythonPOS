from common.config import config
from common.controller import Controller
from common.route import Route
from models.models import Cost

@Route("cost")
class Costs(Controller):
    def Process(self, section):
        if section == 'costs.manage':
            list = Cost.select()
            self.RenderFile('cost/manage.htm', {'_': config.i18n, 'Costs': list})
        elif section == 'costs.new':
            cost = Cost()
            self.RenderFile('cost/cost.htm', {'_': config.i18n, 'Cost': cost})
        elif section == 'costs.delete':
            id = self.IntReq('id')
            cost = Cost.get(Cost.id == id)
            cost.delete_instance()
            self.RenderJSON({'result': 'OK'})
        elif section == 'costs.save':
            id = self.IntReq('id')
            new_title = self.StringReq('title')
            new_invoiceno = self.StringReq('invoiceno')
            new_amount = self.FloatReq('amount')

            try:
                cost = Cost.get(Cost.id == id)
            except:
                cost = Cost()
                cost.regtime = ''
                cost.regdate = ''

            if cost != None:
                cost.title = new_title
                cost.invoiceno = new_invoiceno
                cost.amount = new_amount
                cost.save()

        elif section == 'costs.edit':
            id = self.IntReq('id')
            cost = Cost.select().where(Cost.id == id).get()
            self.RenderFile('cost/cost.htm', {'_': config.i18n, 'Cost': cost})


