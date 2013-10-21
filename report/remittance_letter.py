# -*- coding: utf-8 -*-

from openerp import pooler
from openerp.report import report_sxw
from openerp.tools.translate import _
from osv import osv

from report_webkit.webkit_report import WebKitParser


class remittance_letter_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(remittance_letter_parser, self).__init__(
            cr, uid, name, context=context)
        self.__check_vouchers(cr, uid, context)
        self.localcontext.update({
            'debit_credit': self.get_debit_credit,
            'format_amount': self.format_amount,
            'get_voucher': self.get_voucher,
            'bottom_message': self.get_bottom_message,
            'top_message': self.get_top_message,
            'title': self.get_title,
        })

    def __check_vouchers(self, cr, uid, context=None):
        """ This function check if the message for payment
        is set in the company settings and raise in the other case.
        """
        company_osv = self.pool.get('res.company')
        company_id = company_osv._company_default_get(cr, uid, 'account.voucher', context=context)
        company_br = company_osv.browse(cr, uid, company_id, context=context)
        if not company_br.remittance_letter_top:
            raise osv.except_osv(
                _('Error'),
                _('Please set the "Remittance Letter - top message" in '
                  'company settings.')
            )

    def get_debit_credit(self, br):
        return _('Debit') if br.type == 'debit' else _('Credit')

    def format_amount(self, amount, br):
        # little check
        if not amount:
            return '0.00'
        # shortcut
        position = br.currency_id.position
        symbol = br.currency_id.symbol
        # currency after
        if position == 'after':
            return '%s %s' % (amount, symbol)
        # currency before
        if position == 'before':
            return '%s %s' % (symbol, amount)
        return amount.strip()

    def get_voucher(self, br):
        # This report already operates on account.voucher objects.
        return br

    def get_bottom_message(self, br):
        company = br.company_id
        if not company:
            return ''

        return company.remittance_letter_bottom

    def get_top_message(self, this_br):
        company = this_br.company_id
        if not company:
            return ''

        bank = this_br.partner_bank_id
        if not bank:
            return ''

        iban = bank.acc_number or ''
        date = this_br.date or ''

        return (company.remittance_letter_top
                .replace('$iban', iban)
                .replace('$date', str(date)))

    def get_title(self, br):
        return _('Remittance Letter')


class remittance_letter_report(WebKitParser):
    def remove_previous(self, cr, uid, ids, context=None):
        # get attachement model
        ir_att_osv = pooler.get_pool(cr.dbname).get('ir.attachment')
        # previous ids
        data_ids = ir_att_osv.search(
            cr,
            uid,
            [('res_model', '=', 'account.voucher'),
             ('res_id', 'in', ids)],
            context=context)
        # remove previous items
        ir_att_osv.unlink(cr, uid, data_ids)

    def create(self, cr, uid, ids, datas, context=None):
        ids = self._check_vouchers(cr, uid, ids, context)

        # remove previous items
        self.remove_previous(cr, uid, ids, context=context)
        # call parent
        return super(remittance_letter_report, self).create(
            cr, uid, ids, datas, context)

    def _check_vouchers(self, cr, uid, ids, context):
        ''' - Only print Remittance Letters for posted vouchers. '''

        voucher_obj = pooler.get_pool(cr.dbname).get('account.voucher')
        vouchers = voucher_obj.browse(cr, uid, ids, context=context)

        ids = []

        for voucher in vouchers:
            if voucher.state == 'posted':
                ids.append(voucher.id)

        if not ids:
            raise osv.except_osv(
                _('Error'),
                _('No posted voucher selected.')
            )

        return ids


remittance_letter_report('report.account_streamline.remittance_letter',
                         'account.voucher',
                         'addons/account_streamline/report/remittance_letter.mako',
                         parser=remittance_letter_parser)
