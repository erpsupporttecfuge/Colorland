odoo.define('tecfuge_hrms.tecfuge_hrms', function (require) {
'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;

publicWidget.registry.PortalDashboardExp  = publicWidget.Widget.extend({
    template: 'tecfuge_hrms.portal_dasboards_expense_chart',

      selector: '.portal_dasboards_expense_chart',
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],

     start: function () {




   const ctx = document.getElementById('myChart');

       this._rpc({
                model: 'hr.expense.public',
                method: 'get_expense_portal_dashboard',
                args: [[],session.user_id],
            }).then(function (result) {


    new Chart('ctx', {
    type: 'pie',
    data: result,
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
//
            })

    this._super.apply(this, arguments);


     }

});})

