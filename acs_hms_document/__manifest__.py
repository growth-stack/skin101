# -*- coding: utf-8 -*-
#
# ║ SOFTWARE DEVELOPED AND SUPPORTED BY BITLECT TECHNOLOGY           ║
# ║                   COPYRIGHT (C) 2020 - TODAY                     ║
# ║                   http://www.bitlect.net
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝
{
    'name': 'Hospital Patient Document Management',
    'summary': 'Manage Patient Documents at single place or see all patinet related documents directly on patint.',
    'description': """Manage Patient Documents at single place or see all patinet related documents directly on patint.
    Patient Document Management System. hospital management medical management ACS HMS
    """,
    'version': '1.0.1',
    'category': 'Hospital Management System',
    'author': 'Bitlect Technology.',
    'support': 'info@abitlect.net',
    'website': 'https://www.bitlect.net',
    'license': 'OPL-1',
    'depends': ['acs_hms'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'view/document_view.xml',
        'view/hms_views.xml',
    ],
    'images': [
        'static/description/hms_document_management_system_almightycs_cover.jpg',
    ],
    'application': False,
    'sequence': 2,
    'price': 36,
    'currency': 'EUR',
}
