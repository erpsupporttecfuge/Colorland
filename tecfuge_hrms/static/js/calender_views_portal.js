odoo.define('tecfuge_hrms.dashboard_portals', function (require) {
'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;

publicWidget.registry.PortalDashboardTimeoff  = publicWidget.Widget.extend({
    template: 'tecfuge_hrms.portal_main_dashboard_hr',

      selector: '.portal_dasboards_calender_view',
        jsLibs: [
            '/tecfuge_hrms/static/js/calender_view.js',
        ],

     start: function () {


         var calendarEl = document.getElementById('calendar');
   this._rpc({
                model: 'hr.leave.public',
                method: 'get_dashboard_portal_calender_view',
                args: [[],session.user_id],
            }).then(function (result) {
  var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth', // Set the initial view
                events: result

            });

            calendar.render();
            })


    this._super.apply(this, arguments);


     }

});})

