# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import logging
from odoo.http import request
from odoo.addons.portal.controllers.portal import get_records_pager,CustomerPortal, pager as portal_pager
import odoo.http as http


_logger = logging.getLogger(__name__)

class ContractDrawingImages(http.Controller):

	@http.route(['/open/contract_drawing/<model("contract.drawings"):line>'], type='http', auth="public", website=True,debug=False)
	def Image(self, line):
		img = line.drawing_img
		return http.request.render('bi_job_drawing_image_contracting.contract_drawing_image',{'img': line}) 

	@http.route(['/my/task/<int:task_id>/website/open/contract_drawing/<model("contract.drawings"):line>'],type='http',auth="public",website=True)
	def image_page(self, line, task_id=None):
		img = line.drawing_img
		return http.request.render('bi_job_drawing_image_contracting.contract_drawing_image',{'img': line}) 

	@http.route(['/my/task/website/open/contract_drawing/<model("contract.drawings"):line>'],type='http',auth="public",website=True)
	def image_webpage(self, line, task_id=None):
		img = line.drawing_img
		return http.request.render('bi_job_drawing_image_contracting.contract_drawing_image',{'img': line}) 

class WebsiteJobOrder(CustomerPortal):

	def _prepare_home_portal_values(self, counters):
		values = super()._prepare_home_portal_values(counters)
		if 'job_order_count' in counters:
			job_order_obj = request.env['job.order']
			job_order_count = job_order_obj.search_count([])
			values.update({
				'job_order_count': job_order_count,
			})
		return values

	def _prepare_portal_layout_values(self):
		values = super(WebsiteJobOrder, self)._prepare_portal_layout_values()
		partner = request.env.user.partner_id
		job_order_obj = request.env['job.order']
		job_order_count = job_order_obj.search_count([])
		values.update({
			'job_order_count': job_order_count,
		})
		return values

	@http.route(['/your/job_order', '/your/job_order/page/<int:page>'], type='http', auth="user", website=True)
	def portal_job_order_list(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
		values = self._prepare_portal_layout_values()
		partner = request.env.user.partner_id
		job_order = request.env['job.order']
		domain = []
		repair_count = job_order.search_count(domain)
		pager = request.website.pager(
			url="/my/job_order",
			total=repair_count,
			page=page,
			step=self._items_per_page
		)
		partner = request.env.user.partner_id
		job = job_order.search([])
		values.update({
			'job': job,
			'page_name': 'job_order',
			'pager': pager,
			'default_url': '/my/job_order',
		})
		return request.render("bi_job_drawing_image_contracting.portal_job_order_list", values)

	@http.route(['/job/view/detail/<model("job.order"):job>'],type='http',auth="public",website=True)
	def job_view(self, job, category='', search='', **kwargs):
		context = dict(request.env.context or {})
		job_obj = request.env['job.order']
		context.update(active_id=job.id)
		job_data_list = []
		job_data = job_obj.browse(int(job))
		for items in job_data:
			job_data_list.append(items)
		return http.request.render('bi_job_drawing_image_contracting.job_order_request_view',{
			'job_data_list': job
		}) 
	
	@http.route(['/my/task/<int:task_id>/<int:job_id>'], type='http', auth="user", website=True)
	def portal_my_task(self, job_id=None,task_id=None, **kw):
		job_order = request.env['job.order'].search([('id','=',job_id)],limit=1)
		task = request.env['project.task'].browse(task_id)
		project = request.env['project.project'].search([('task_ids','in',task_id)])
		vals = {
			'task': task,
			'order':job_order,
			'job_order':job_order,
			'user': request.env.user,
			'object': task
		}
		history = request.session.get('my_tasks_history', [])
		vals.update(get_records_pager(history, task))
		vals.update({'order':job_order})
		return request.render("bi_job_drawing_image_contracting.drawing_job_order_inherit",vals)