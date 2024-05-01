# Copyright 2020-2023 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    add_prepayment_test = fields.Boolean(
        config_parameter="credit_management.prepayment_test",
        help="If selected then the test should be done even if the credit limit is zero.",
    )

    no_of_days_overdue_test = fields.Boolean(
        string="Add Overdue Days Test",
        config_parameter="credit_management.no_of_days_overdue_test",
        help="If selected then the test should be done for the number of days overdue.",
    )

    x_no_of_overdue_days = fields.Integer(
        string="No. Of Overdue Days",
        config_parameter="credit_management.x_no_of_overdue_days",
        readonly=False,
    )

    stock_allow_check_availability = fields.Boolean(
        string="Allow DO Check Availability even if Hold Delivery Till is selected",
        config_parameter="credit_management.stock_allow_check_availability",
    )
