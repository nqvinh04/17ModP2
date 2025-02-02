# -*- coding: utf-8 -*-

from odoo import fields, models


class Account(models.Model):
    _inherit = "account.analytic.account"

    helpdesk_sla_level = fields.Many2one(
        'helpdesk.level.config',
        string="Service Level Agreement Level",
        required=False,
        copy=True,
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
