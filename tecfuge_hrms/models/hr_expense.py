from odoo import api, fields, models

class ExpenseForPublic(models.Model):
    _name ="hr.expense.public"


    def get_expense_portal_dashboard(self,employee_id):
            employee_id = self.env['hr.employee'].sudo().search([('user_id','=',employee_id)])
            products =[]
            value =[]
            print(employee_id)
            query = self.env['hr.expense'].sudo().read_group([('employee_id','=',employee_id.id)
                                                        ],['product_id','total_amount'],['product_id'],lazy=True)


            for rec in query:
                id,product=rec['product_id']
                rec['product_id'] = product
                products.append(rec['product_id'])
                value.append(rec['total_amount'])

            data = {
                'labels': products,
                'datasets': [{
                    'label': 'Expense',
                    'data': value,
                    'backgroundColor': ["#0074D9", "#FF4136", "#2ECC40", "#FF851B", "#7FDBFF", "#B10DC9", "#FFDC00",
                                      "#001f3f", "#39CCCC", "#01FF70", "#85144b", "#F012BE", "#3D9970", "#111111",
                                      "#AAAAAA"],
                    'borderWidth': 1
                }]
            }

            return data





class Expense(models.Model):
    _inherit = "hr.expense"

    attachment_ids = fields.Many2many('ir.attachment',string="documents")


    def get_expense_portal_state(self,employee_id):
        query = self.read_group([('employee_id','=',employee_id)
                                                    ],['state','total_amount'],['state'],lazy=True)

        return query
