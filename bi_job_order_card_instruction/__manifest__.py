# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################

{
    "name" : "Instruction and Quality Checklist on Job Order in Odoo",
    "version" : "17.0.0.0",
    "category" : "Projects",
    "depends" : ['base','hr_expense','bi_odoo_job_costing_management','bi_material_purchase_requisitions'],
    "author": "BrowseInfo",
    "website" : "https://www.browseinfo.com",
    "price": 15.00,
    "currency": 'EUR',
    'summary': 'Manage Instruction Quality Checklist on Job Order Quality Checklist Construction Quality Checklist contracting Quality Checklist Job costing Quality Checklist Instruction  on Job Order Instruction Construction Instruction Job costing Instruction on project',
    'description': """
    Instruction and Quality Checklist on Job Order 
    Job Order Instruction and Quality Checklist
    Job Order Quality checklist
    project job costing Instruction
 project job costing quality Checklists
        Project Job Costing and Job Cost Sheet.
        job contract, job contracting, Construction job , contracting job , contract estimation cost estimation project estimation , 
        This modules helps to manage contracting,Job Costing and Job Cost Sheet inculding dynamic material request
        Odoo job costing bundle
        This modules helps to manage contracting,Job Costing and Job Cost Sheet inculding dynamic material request
        Project Contracting
        Project costing
        project cost sheet
            Send Estimation to your Customers for materials, labour, overheads details in job estimation.
        Estimation for Jobs - Material / Labour / Overheads
        Material Esitmation
        Job estimation
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
    material change request on construction project
    order change request on consturction project
    change order request on constuction projects
    change product request on project constuction
    product change request for project constuction

    product change request on constuction project
""",
    "data": [
        'security/ir.model.access.csv',
         'data/ir_sequence_data.xml',
        'views/job_instruction.xml',
        'report/report_menu.xml',
        'report/job_instruction_temp_id.xml',
    ],
    'qweb': [],
    "auto_install": False,
    "installable": True,
    'license': 'OPL-1',
    "live_test_url":'https://youtu.be/_gLlhIITAHM',
    "images":['static/description/Banner.gif'],
}

