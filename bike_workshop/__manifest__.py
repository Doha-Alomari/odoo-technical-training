{
'name' : 'Bike Workshop',
'version' : '19.0.1.0.0',
'category': 'Services',
'summary': 'Manage bike workshop operations',
'depends' : ['base'],
'data' : [
      'security/bike_security.xml',
      'security/ir.model.access.csv',
      'views/bike_views.xml',
],
'installable': True,
'application': True,
}