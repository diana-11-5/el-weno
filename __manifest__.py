# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'L10n Mx Edi Cancel Fix',
    'description': """
        Temporal Fix for 2022 new sat/finkok cancel method""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Munin',
    'depends': [
        'account', 'l10n_mx_edi'
    ],
    'data': [
        'views/account_payment.xml',
        'data/data.xml',
        'security/edi_cancel_motive.xml',
        'views/edi_cancel_motive.xml',
        'views/account_move.xml',
    ],
    'demo': [
    ],
}
