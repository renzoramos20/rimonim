# -*- coding: utf-8 -*-
{
    'name': "mrp extends",

    'summary': """
        manufacturing extends""",
    'description': """
        manufacturing extends
    """,
    'author': "Eduwebgroup",
    'website': "http://www.eduwebgroup.com",
    'category': 'Uncategorized',
    'version': '0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mrp',],
    # always loaded
    'data': [
        'views/mrp_views.xml',
        'reports/mrp_report_bom_structure.xml'
    ],

    'demo': [
        # 'demo/demo.xml',
    ],
}