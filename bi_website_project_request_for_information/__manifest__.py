# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Job Costing -Request for Information in odoo',
    'version': '17.0.0.0',
    'category': 'Projects',
    'summary': 'Construction Request for Information for project job costing contracting Request for Information reporting information in Construction online information website Construction request online Construction project information job costing information request',
    'description': """
        Project Job Costing and Job Cost Sheet.
        This modules helps to manage contracting,Job Costing and Job Cost Sheet inculding dynamic material request
        Project Contracting
        Project costing
        project cost sheet
            Send Estimation to your Customers for materials, labour, overheads details in job estimation.
        Estimation for Jobs - Material / Labour / Overheads
        Material Esitmation
		reporting information in Construction
        Job estimationProject Job Costing and Job Cost Sheet.job contract, job contracting, Construction job , contracting job , contract estimation cost estimation project estimation , 
        This modules helps to manage contracting,Job Costing and Job Cost Sheet inculding dynamic material request
        labour estimation
        Overheads estimation
        BrowseInfo developed a new odoo/OpenERP module apps.
        This module use for Real Estate Management, Construction management, Building Construction,
        Material Line on JoB Estimation
        Labour Lines on Job Estimation.
        Overhead Lines on Job Estimation.
        create Quotation from the Job Estimation.
        overhead on job estimation
        Construction Projects
        Budgets
        Notes
        Materials
        Material Request For Job Orders
        Add Materials
        Job Orders
        Create Job Orders
        Job Order Related Notes
        Issues Related Project
        Vendors
        Vendors / Contractors

        Construction Management
        Construction Activity
        Construction Jobs
        Job Order Construction
        Job Orders Issues
        Job Order Notes
        Construction Notes
        Job Order Reports
        Construction Reports
        Job Order Note
        Construction app
        Project Report
        Task Report
        Construction Project - Project Manager
        real estate property
        propery management
        bill of material
        Material Planning On Job Order

        Bill of Quantity On Job Order
        Bill of Quantity construction
        Project job costing on manufacturing
    BrowseInfo developed a new odoo/OpenERP module apps.
    Material request is an instruction to procure a certain quantity of materials by purchase , internal transfer or manufacturing.So that goods are available when it require.
    Material request for purchase, internal transfer or manufacturing
    Material request for internal transfer
    Material request for purchase order
    Material request for purchase tender
    Material request for tender
    Material request for manufacturing order.
    product request, subassembly request, raw material request, order request
    manufacturing request, purchase request, purchase tender request, internal transfer request
""",
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    'depends': ['base', 'bi_odoo_job_costing_management', 'bi_material_purchase_requisitions', 'website_sale',
                'survey'],
    'data': [

        'security/ir.model.access.csv',
        'views/request_view.xml',
        'views/rfi_stage.xml',
        'views/request_template_view.xml',
        'report/rfi_report.xml',
        'report/rfi_report_view.xml',
    ],
    "price": 29,
    "license": "OPL-1",
    "currency": "EUR",
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://youtu.be/ugabdBZfpAA',
    "images": ['static/description/Banner.gif'],
}

