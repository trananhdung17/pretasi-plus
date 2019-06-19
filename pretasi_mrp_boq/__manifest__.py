# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

{
    'name': 'Pretasi - Bill of Quantity',
    'version': '1.0',
    'summary': 'Bill of Quantity for Pretasi Project',
    'sequence': 20,
    'description': '',
    'category': 'manufacturing',
    'website': '',
    'images': [],
    'depends': ['pretasi_product', 'mrp', 'purchase', 'sale'],
    'data': [
        'data/products.xml',
        'views/boq.xml',
        'views/production.xml',
        'security/ir.model.access.csv',
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
