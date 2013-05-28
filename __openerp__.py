# -*- coding: utf-8 -*-
##############################################################################
#
##############################################################################
{
    "name" : "Account Streamline",
    "version" : "0.1",
    "author" : "XCG Consulting",
    "category": 'Accounting',
    "description": """Enhancements to the account module to streamline its
    usage.
    """,
    'website': 'http://www.openerp-experts.com',
    'init_xml': [],
    "depends" : ['base', 'account_accountant', 'account_voucher', 'account_sequence'],
    "data": [
        'data/partner_data.xml',
        'wizard/account_reconcile_view.xml',
        'account_move_line_search_unreconciled.xml',
        'account_move_line_tree.xml',
        'account_move_view.xml',
        'partner_view.xml',
        'payment_selection.xml',
        'account_move_line_journal_items.xml',
        'account_menu_entries.xml'
    ],
    'js': [
        'static/src/js/account_streamline_move_reconcile.js',
    ],
    'qweb' : [
        'static/src/xml/account_streamline_move_reconcile.xml',
    ],
    #'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
