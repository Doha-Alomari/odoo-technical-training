{
'name' : 'Bike Workshop',
'version' : '19.0.1.0.0',
'category': 'Services',
'summary': 'Manage bike workshop operations',
'depends' : ['base', 'product'],
'data': [
    'data/rental_sequence.xml',
    'data/repair_sequence.xml',
    'security/bike_security.xml',
    'security/ir.model.access.csv',
    'views/bike_views.xml',
    'views/rental_views.xml',
    'views/repair_views.xml',
    'views/res_partner_views.xml',
],
'installable': True,
'application': True,
}