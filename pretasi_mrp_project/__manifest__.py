# __author__ = 'trananhdung'
# -*- coding: utf-8 -*-

{
    'name': 'Pretasi - MRP Project',
    'version': '1.0',
    'summary': 'MRP Project for Pretasi Project',
    'sequence': 100,
    'description': '',
    'category': 'manufacturing',
    'website': '',
    'images': [],
    'depends': ['pretasi_mrp_boq', 'project'],
    'data': [
        'views/boq.xml',
        'views/project.xml',
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
