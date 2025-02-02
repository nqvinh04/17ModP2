# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, get_lang

class PurchaseOrder(models.Model):
	_inherit ='purchase.order'
	
	purchase_manual_currency_rate_active = fields.Boolean('Apply Manual Exchange')
	purchase_manual_currency_rate = fields.Float('Rate', digits=(12, 6))

	def _prepare_invoice(self):
		res = super(PurchaseOrder, self)._prepare_invoice()
		if self.purchase_manual_currency_rate_active:
			res.update({
				'manual_currency_rate_active': self.purchase_manual_currency_rate_active,
				'manual_currency_rate' : self.purchase_manual_currency_rate,
			})
		return res


class PurchaseOrderLine(models.Model):
	_inherit ='purchase.order.line'

	@api.onchange('product_qty', 'product_uom')
	def _onchange_quantity(self):
		if not self.product_id:
			return
		params = {'order_id': self.order_id}
		seller = self.product_id._select_seller(
			partner_id=self.partner_id,
			quantity=self.product_qty,
			date=self.order_id.date_order and self.order_id.date_order.date(),
			uom_id=self.product_uom,
			params=params)

		if seller or not self.date_planned:
			self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

		# If not seller, use the standard price. It needs a proper currency conversion.
		if not seller:
			po_line_uom = self.product_uom or self.product_id.uom_po_id
			price_unit = self.env['account.tax']._fix_tax_included_price_company(
				self.product_id.uom_id._compute_price(self.product_id.standard_price, po_line_uom),
				self.product_id.supplier_taxes_id,
				self.taxes_id,
				self.company_id,
			)
			if price_unit and self.order_id.currency_id and self.order_id.company_id.currency_id != self.order_id.currency_id:
				price_unit = self.order_id.company_id.currency_id._convert(
					price_unit,
					self.order_id.currency_id,
					self.order_id.company_id,
					self.date_order or fields.Date.today(),
				)

			if self.order_id.purchase_manual_currency_rate_active:
				price_unit = self.product_id.standard_price * self.order_id.purchase_manual_currency_rate

			self.price_unit = price_unit
			return

		price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.taxes_id, self.company_id) if seller else 0.0
		if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
			price_unit = seller.currency_id._convert(
				price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

		if seller and self.product_uom and seller.product_uom != self.product_uom:
			price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

		if self.order_id.purchase_manual_currency_rate_active:
			price_unit = self.product_id.standard_price * self.order_id.purchase_manual_currency_rate

		self.price_unit = price_unit

