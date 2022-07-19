# -*- coding: utf-8 -*-
{
    'name': "product packaging extends",

    'summary': """
        product packaging extends""",
    'description': """
       product packaging extends
    """,
    'author': "Eduwebgroup",
    'website': "http://www.eduwebgroup.com",
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'product',],
    # always loaded
    'data': [
        'views/product_package_view.xml'
    ],

    'demo': [
        # 'demo/demo.xml',
    ],
}