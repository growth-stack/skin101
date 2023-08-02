# -*- coding: utf-8 -*-
#
# ║ SOFTWARE DEVELOPED AND SUPPORTED BY BITLECT TECHNOLOGY           ║
# ║                   COPYRIGHT (C) 2020 - TODAY                     ║
# ║                   http://www.bitlect.net
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝
{
    'name': 'Medical Surgery',
    'category': 'Medical',
    'summary': 'Manage Medical Surgery related operations',
    'description': """
    Manage Medical Surgery related operations hospital management system medical ACS HMS
    """,
    'version': '1.0.6',
    'author': 'Bitlect Technology.',
    'support': 'info@abitlect.net',
    'website': 'www.bitlect.com',
    'depends': ['acs_hms'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'report/surgery_report.xml',
        'views/surgery_base.xml',
        'views/surgery_view.xml',
        'views/hms_base_view.xml',
        'views/res_config_settings_views.xml',
        'views/menu_item.xml',
    ],
    'demo': [
        'demo/hms_demo.xml',
    ],
    'sequence': 1,
    'application': True,
    'price': 21,
    'currency': 'EUR',
}
