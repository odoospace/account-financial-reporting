# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright Camptocamp SA 2011
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models


class AccountTrialBalanceWizard(models.TransientModel):
    """Will launch trial balance report and pass required args"""

    _inherit = "account.common.balance.report"
    _name = "trial.balance.webkit"
    _description = "Trial Balance Report"

    # pylint: disable=old-api7-method-defined
    def _print_report(self, cursor, uid, ids, data, context=None):
        context = context or {}
        # we update form with display account value
        vals = self.read(cursor, uid, ids, ['analytic_segment_ids'], context=context)[0]
        segment_ids = []
        segment_obj = self.pool.get('analytic_segment.segment')
        segment_tmpl_ids = []
        for i in vals['analytic_segment_ids']:
            segment = self.pool.get('trial.balance.webkit.segments').browse(cursor, uid, i)
            segment_ids += [segment.segment_id.id]
            if segment.with_children:
                segment_tmpl_ids += segment.segment_id.segment_tmpl_id.get_childs_ids()
        
        segment_ids += segment_obj.search(cr, uid, [['segment_tmpl_id', 'in', segment_tmpl_ids]])
        
        data['form']['segment_ids'] = segment_ids
        data = self.pre_print_report(cursor, uid, ids, data, context=context)
        
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account.account_report_trial_balance_webkit',
                'datas': data}
