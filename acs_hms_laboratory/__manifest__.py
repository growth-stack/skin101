# -*- coding: utf-8 -*-
#
# ║ SOFTWARE DEVELOPED AND SUPPORTED BY BITLECT TECHNOLOGY           ║
# ║                   COPYRIGHT (C) 2020 - TODAY                     ║
# ║                   http://www.bitlect.net
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝
{
    'name': 'Hospital Laboratory Management',
    'summary': 'Manage Lab requests, Lab tests, Invoicing and related history for hospital.',
    'description': """
        This module add functionality to manage Laboratory flow. laboratory management system
        Hospital Management lab tests laboratory invoices laboratory test results ACS HMS
    """,
    'version': '1.0.5',
    'category': 'Medical',
    'author': 'Bitlect Technology.',
    'support': 'info@abitlect.net',
    'website': 'https://www.bitlect.net',
    'license': 'OPL-1',
    'depends': ['acs_hms_hospitalization', 'acs_hms_document'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/laboratory_data.xml',
        'views/laboratory_request.xml',
        'views/laboratory_view.xml',
        'views/laboratory_test_view.xml',
        'views/hms_base_view.xml',
        'views/menu_item.xml',
        'report/report_acs_lab_prescription.xml',
        'report/lab_report.xml',
        'report/discharge_summary_report.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'price': 51,
    'currency': 'EUR',
}
