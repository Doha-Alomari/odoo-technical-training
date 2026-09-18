{
    'name': 'Bike Workshop',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'Manage bike workshop operations',
    'depends': ['base', 'product', 'portal'],

    'data': [
        'data/rental_sequence.xml',
        'data/repair_sequence.xml',

        'security/bike_security.xml',
        'security/ir.model.access.csv',

        'views/bike_views.xml',
        'views/rental_views.xml',
        'views/rental_analysis_views.xml',
        'views/repair_views.xml',
        'views/res_partner_views.xml',
        'views/product_views.xml',

        'views/portal/rental_portal_templates.xml',

        'reports/rental_report_templates.xml',
        'reports/rental_report.xml',
        'views/dashboard_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'bike_workshop/static/src/dashboard/dashboard.js',
            'bike_workshop/static/src/dashboard/dashboard.xml',
            'bike_workshop/static/src/css/branding.css',
        ],
        'web.assets_frontend': [
            'bike_workshop/static/src/css/portal_branding.css',
        ],
    },

    'installable': True,
    'application': True,
    'post_init_hook': 'post_init_hook',
}