from datetime import date, datetime
import pytz
import json
import datetime
import io
from odoo import api, fields, models, _
from odoo.tools import date_utils
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ProductOnhandSale(models.Model):
    _name = 'product.onhand.sale'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company,readonly=1)


    def action_submit_xlsx(self):
        data = {
            'company_id': self.company_id.id

        }
        return {
            'type': 'ir_actions_xlsx_download',
            'data': {'model': 'product.onhand.sale',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Current Onhand  - Sale Order ',
                     }
        }


    def merge_analstic(self,data_shop):
        temp = {}
        for rec in data_shop:
            temp[rec['product_id']] = {}
        for rec in data_shop:
            temp[rec['product_id']][rec['analytic_account_id']] = rec['sum']
        return temp

    def merge_location(self,data_shop):
        temp = {}

        for rec in data_shop:
            temp[rec['product_id']] = {}
        for rec in data_shop:
            temp[rec['product_id']][rec['id']] = rec['sum']
        return temp

    def merge_into_main(self,product_list,shope,location):
        result ={}
        for rec in product_list.keys():
            result[rec] ={'shop':{},'location':{}
            }
        for rec in product_list.keys():
            if rec in shope.keys():
                result[rec]['shop'] = shope[rec]
            if rec in location.keys():
                result[rec]['location'] = location[rec]
        return result


    def  print_overall_result(self,worksheet,product_master_list,analystic_account_list,location_list,main,row,col):
        row = row + 1
        print('inside function',location_list)
        for rec in main.keys():
            worksheet.write(row,0,product_master_list[rec])
            # print(product_master_list)
            sum = 0
            for shops in main[rec]['shop'].keys():
                if shops in analystic_account_list.keys():
                    worksheet.write(row,analystic_account_list[shops]['seq'], main[rec]['shop'][shops])
                    sum = sum + main[rec]['shop'][shops]
            for locations in main[rec]['location'].keys():
                if locations in location_list.keys():
                    worksheet.write(row,location_list[locations]['seq'],main[rec]['location'][locations])
            row = row + 1
    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        product_master_list ={}
        analystic_account_list ={}
        location_list ={}
        # analystic account
        count =1

        print(data['company_id'])
        if data['company_id'] == 1:
            for rec in self.env['crm.team'].search([('company_id','=',[data['company_id'],False])]):
                analystic_account_list[rec.id] = {'name':rec.name,'seq':count}
                count = count+1
        if data['company_id'] == 3:
            for rec in self.env['crm.team'].search([('company_id','=',[data['company_id'],False,1])]):
                analystic_account_list[rec.id] = {'name':rec.name,'seq':count}
                count = count+1
        if data['company_id'] == 2:
            for rec in self.env['crm.team'].search([('company_id','=',[data['company_id'],False])]):
                analystic_account_list[rec.id] = {'name':rec.name,'seq':count}
                count = count+1

        for rec in self.env['stock.location'].search([('usage','=','internal'),('company_id','=',[data['company_id'],False])]):
            location_list[rec.id] = {'name':rec.name,'seq':count}
            count = count+1

        print()
        #location
        # product master list
        for rec in self.env['product.product'].search([( 'company_id','in',[data['company_id'],False])]):
            product_master_list[rec.id] = rec.product_tmpl_id.name
        # shop
        current_time = fields.datetime.now()
        timeout_ago = fields.datetime.now()-datetime.timedelta(days=365)
        print("current_time",current_time)
        print("timeout_ago",timeout_ago)

        sql = '''select product_id,team_id as analytic_account_id,sum(product_uom_qty) from sale_report,crm_team where 
        crm_team.id = sale_report.team_id 
        and crm_team.active = true AND sale_report.company_id  ='''+str(data['company_id'])+" and  date  between '"+ str(timeout_ago)\
              +"'  and  '"+str(current_time)+"' "+'''  and sale_report.state not in ('draft', 'cancel', 'sent') 
        group by product_id,team_id
              '''
        print(sql)
        self.env.cr.execute(sql)
        data_shop =self.env.cr.dictfetchall()
        shope=self.merge_analstic(data_shop)

        #sale order

        sql =''' 
        select product_id, stock_location.id,sum(quantity) from stock_quant, stock_location
        where stock_quant.location_id = stock_location.id
        and 
        stock_location.usage = 'internal'  and  stock_quant.company_id ='''+str(data['company_id'])+''' 
        group by stock_quant.product_id, quantity, stock_location.id

        '''


        # label of shope
        merge_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
        'font_name': 'Arial, Helvetica, sans-serif',

            'fg_color': '#f09834'})

        sub_heading_location = workbook.add_format({'align': 'center',
                                           'fg_color': '#fef2cc'



                                           })
        sub_heading_shop = workbook.add_format({'align': 'center',
                                           'fg_color': '#faee2d'



                                           })

        worksheet.merge_range(0,0,1,0,"Products",merge_format)
        cell_1 = workbook.add_format({
        'align': 'center',
        'font_name': 'Arial, Helvetica, sans-serif',
        'fg_color': '#87e922'})

        cell_2 = workbook.add_format({
            'align': 'center',
            'font_name': 'Arial, Helvetica, sans-serif',
            'fg_color': '#d0e0e3'})

        col_last = 0
        for rec  in  analystic_account_list.keys():
            col_last = analystic_account_list[rec]['seq']
            worksheet.write(1,analystic_account_list[rec]['seq'],analystic_account_list[rec]['name'],cell_1)
        worksheet.merge_range(0,1,0,col_last,"Shop(Sale)",sub_heading_shop)
        cell_1 = workbook.add_format({'bold': True, 'font_color': 'green'})
        col_last2 = 0
        for rec in location_list.keys():
            col_last2 = location_list[rec]['seq']
            worksheet.write(1, location_list[rec]['seq'], location_list[rec]['name'], cell_2)
        if col_last+1 == col_last2:
            worksheet.write(0,col_last2,"Location(On Hand)",sub_heading_location)
        else:
            worksheet.merge_range(0,col_last+1,0,col_last2,"Location(On Hand)",sub_heading_location)


        self.env.cr.execute(sql)
        data_location =self.env.cr.dictfetchall()
        location=self.merge_location(data_location)
        main = self.merge_into_main(product_master_list,shope,location)
        print('list_image',location_list)
        self.print_overall_result(worksheet,product_master_list,analystic_account_list,location_list,main,1,0)


        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()






