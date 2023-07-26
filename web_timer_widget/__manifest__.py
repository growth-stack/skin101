# -*- coding: utf-8 -*-
#
# ║ SOFTWARE DEVELOPED AND SUPPORTED BY BITLECT TECHNOLOGY           ║
# ║                   COPYRIGHT (C) 2020 - TODAY                     ║
# ║                   http://www.bitlect.net
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝
{
    'name': "Web Timer Widget",
    'category': "web",
    'version': "16.1.0",
    'summary': """Add timer widget on web view.""",
    'description': """This module widget which allows you to set timer on any field by passing your start and end date as parameter. start stop timer working time""",
    "website": 'https://www.bitlect.net',
    'author': 'Bitlect Technology.',
    'support': 'info@abitlect.net',
    'depends': ['base', 'web'],
    'assets': {
        'web.assets_backend': [
            'web_timer_widget/static/src/js/widget.js',
        ]
    },
    'images': [
        'static/description/timer.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    "price": 15,
    "currency": "EUR",
}
