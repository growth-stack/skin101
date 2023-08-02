# -*- coding: utf-8 -*-
#
# ║ SOFTWARE DEVELOPED AND SUPPORTED BY BITLECT TECHNOLOGY           ║
# ║                   COPYRIGHT (C) 2020 - TODAY                     ║
# ║                   http://www.bitlect.net
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝
{
    'name': 'Hospitalization',
    'category': 'Medical',
    'summary': 'Manage your Hospital equipment and related process of Inpatient Registration, Surgery, Care, Discharge',
    'description': """
    Hospitalization is include Inpatient Registration, Surgery, Care, Discharge. Hospital related Flows. ACS HMS
    """,
    'version': '1.0.13',
    'author': 'Bitlect Technology.',
    'support': 'info@abitlect.net',
    'website': 'www.almightycs.com',
    'depends': ['acs_hms', 'acs_hms_surgery'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/transfer_accomodation_view.xml',
        'views/hospitalization_view.xml',
        'views/hospitalization_care_views.xml',
        'views/bed_view.xml',
        'views/ward_view.xml',
        'views/building_view.xml',
        'views/ot_view.xml',
        'views/hms_base_view.xml',
        'views/death_register.xml',
        'views/res_config_settings_views.xml',
        'report/report_hospital_discharge.xml',
        'report/report_visiting_pass.xml',
        'report/report_hospitalization_patient_card.xml',
        'report/ward_patient_list_report.xml',
        'data/sequence.xml',
        'data/hms_data.xml',
        'views/menu_item.xml',
    ],
    'demo': [],
    'sequence': 1,
    'application': True,
    'price': 51,
    'currency': 'EUR',
}
