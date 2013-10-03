# -*- coding: utf-8 -*-

from openerp.report import report_sxw
from openerp.tools.translate import _
from osv import osv

from report_webkit.webkit_report import WebKitParser


class payment_notice_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        print "TOTO"
        super(payment_notice_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
        })


class payment_notice_report(WebKitParser):
    pass


payment_notice_report('report.account_streamline.payment_notice',
               'account.voucher',
               'addons/account_streamline/report'
               '/payment_notice.mako',
               parser=payment_notice_parser)
