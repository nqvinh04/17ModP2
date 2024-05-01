# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class res_config_settings(models.TransientModel):
    """
    Cloud storage basic settings
    """
    _inherit = "res.config.settings"

    @api.depends("cloud_ir_actions_server_ids_str")
    def _compute_cloud_ir_actions_server_prm_default_model_id(self):
        """
        Compute method for cloud_ir_actions_server_prm_default_model_id
        """
        attachment_model_id = self.env["ir.model"].search([("model", "=", "ir.attachment")], limit=1).id
        for conf in self:
            conf.cloud_ir_actions_server_prm_default_model_id = attachment_model_id

    @api.depends("cloud_ir_actions_server_ids_str")
    def _compute_cloud_ir_actions_server_ids(self):
        """
        Compute method for cloud_ir_actions_server_ids
        """
        for setting in self:
            cloud_ir_actions_server_ids = []
            if setting.cloud_ir_actions_server_ids_str:
                try:
                    actions_list = safe_eval(setting.cloud_ir_actions_server_ids_str)
                    cloud_ir_actions_server_ids = self.env["ir.actions.server"].search([("id", "in", actions_list)]).ids
                except Exception as e:
                    cloud_ir_actions_server_ids = []
            setting.cloud_ir_actions_server_ids = [(6, 0, cloud_ir_actions_server_ids)]

    def _inverse_cloud_ir_actions_server_ids(self):
        """
        Inverse method for cloud_ir_actions_server_ids
        """
        for setting in self:
            cloud_ir_actions_server_ids_str = ""
            if setting.cloud_ir_actions_server_ids:
                cloud_ir_actions_server_ids_str = "{}".format(setting.cloud_ir_actions_server_ids.ids)
            setting.cloud_ir_actions_server_ids_str = cloud_ir_actions_server_ids_str

    @api.onchange("cloud_log_days")
    def _onchange_cloud_log_days(self):
        """
        Onchange method for cloud_log_days
        """
        for config in self:
            if config.cloud_log_days < 3:
                config.cloud_log_days = 3

    module_google_drive_odoo = fields.Boolean(string="Google Drive Sync")
    module_onedrive = fields.Boolean(string="OneDrive / SharePoint Sync")
    module_owncloud_odoo = fields.Boolean(string="ownCloud / Nextcloud Sync")
    module_dropbox = fields.Boolean(string="Dropbox Sync")
    module_cloud_base_documents = fields.Boolean(string="Sync Enterprise Documents")
    notsynced_mimetypes = fields.Char(string="Not synced mimetypes", config_parameter="cloud_base.notsynced_mimetypes")
    cloud_log_days = fields.Integer(
        string="Logs storage period (days)",
        config_parameter="cloud_base.cloud_log_days",
        default=3,
    )
    cloud_ir_actions_server_prm_default_model_id = fields.Many2one(
        "ir.model",
        compute=_compute_cloud_ir_actions_server_prm_default_model_id,
        string="Default CB model"
    )
    cloud_ir_actions_server_ids = fields.Many2many(
        "ir.actions.server",
        compute=_compute_cloud_ir_actions_server_ids,
        inverse=_inverse_cloud_ir_actions_server_ids,
        string="File Manager Mass actions",
        domain=[("model_name", "=", "ir.attachment")],
    )
    cloud_ir_actions_server_ids_str = fields.Char(
        string="File Manager Mass actions (Str)",
        config_parameter="cloud_base.ir_actions_server_ids",
    )

    def action_test_prepare_folders(self):
        """
        The method to manually launch folders' preparation cron job

        Methods:
         * method_direct_trigger of ir.cron
        """
        cron_id = self.sudo().env.ref("cloud_base.cloud_base_prepare_folders")
        cron_id.method_direct_trigger()

    def action_test_sync_job(self):
        """
        The method to manually launch sync cron job

        Methods:
         * method_direct_trigger of ir.cron
        """
        cron_id = self.sudo().env.ref("cloud_base.cloud_base_run_prepare_queue")
        cron_id.method_direct_trigger()
