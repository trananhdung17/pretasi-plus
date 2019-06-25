# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

{
    'name': 'Pretasi - Sale MRP',
    'version': '1.0',
    'summary': 'Make MO for Sale Order - Pretasi Project',
    'sequence': 100,
    'description': '',
    'category': 'sale',
    'website': '',
    'images': [],
    'depends': ['pretasi_mrp_boq', 'sale'],
    'data': [
        'views/sale.xml',
        'views/boq.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '',
}
