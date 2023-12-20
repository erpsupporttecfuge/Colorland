# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'TEC-HRMS',
    'version' : '1.4',
    'summary': 'Study website',
    'sequence': 10,
    'description': """
    
    """,
    'depends' : ['website','web','portal','base','hr','hr_holidays','hr_expense','hr_payroll','helpdesk','hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'views/backend/hr_timeoff.xml',
        'views/backend/hr_employee.xml',
        'views/documents/portal_document_tree_view.xml',
        'views/expense/portal_hr_expense.xml',
        'views/expense/portal_hr_expense_dashboard.xml',
        'views/timeoff/portal_dashboard.xml',
        'views/common/employee_banner.xml',
        'views/timeoff/hr_timeoff.xml',
        'views/common/basic_layout.xml',
        'views/employee/employee.xml',
        'views/expense/portal_hr_expense_tree.xml',
        'views/expense/portal_hr_expense_form.xml',
        'views/payroll/portal_payroll_main.xml',
        'views/payroll/portal_payroll_tree_view.xml',
        'views/payroll/portal_form_view.xml',
        'views/dahboard/portal_dashboard_hr.xml',
        'views/dahboard/calender_timeoff_portal.xml',
        'views/dahboard/notification_of_documents.xml',
        'views/helpdesk/portal_helpdesk_tickets.xml',
        'views/helpdesk/portal_help_desk_ticket_form.xml',
        'views/backend/hr_applicant.xml',
        'views/common/my_dashboard_redirect.xml'


    ],
    'assets': {

        'web.assets_frontend': [
            'tecfuge_hrms/static/js/dashboard_css.js',
            'tecfuge_hrms/static/js/calender_view.js',
            'tecfuge_hrms/static/js/calender_views_portal.js',
            'tecfuge_hrms/static/src/css/employee.css',
            'tecfuge_hrms/static/src/css/activity.css'
        ]
    },



    'license': 'LGPL-3',
}
