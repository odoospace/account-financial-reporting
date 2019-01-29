# -*- coding: utf-8 -*-
# Copyright 2009-2016 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models


class AccountTrialBalanceWizard(models.TransientModel):
    _inherit = 'trial.balance.webkit'

    # pylint: disable=old-api7-method-defined
    def xls_export(self, cr, uid, ids, context=None):
        return self.check_report(cr, uid, ids, context=context)

    # pylint: disable=old-api7-method-defined
    def _print_report(self, cr, uid, ids, data, context=None):
        context = context or {}
        if context.get('xls_export'):
            # we update form with display account value
            vals = self.read(cr, uid, ids, ['analytic_segment_ids'], context=context)[0]
            segment_ids = []
            segment_obj = self.pool.get('analytic_segment.segment')
            segment_tmpl_ids = []
            for i in vals['analytic_segment_ids']:
                segment = self.pool.get('trial.balance.webkit.segments').browse(cr, uid, i)
                segment_ids += [segment.segment_id.id]
                if segment.with_children:
                    segment_tmpl_ids += segment.segment_id.segment_tmpl_id.get_childs_ids()
            
            segment_ids += segment_obj.search(cr, uid, [['segment_tmpl_id', 'in', segment_tmpl_ids]])

            data['form']['segment_ids'] = segment_ids
            data = self.pre_print_report(cr, uid, ids, data, context=context)

            return {'type': 'ir.actions.report.xml',
                    'report_name': 'account.account_report_trial_balance_xls',
                    'datas': data}
        else:
            return super(AccountTrialBalanceWizard, self)._print_report(
                cr, uid, ids, data, context=context)
