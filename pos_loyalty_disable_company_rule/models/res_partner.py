# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_points = fields.Float(company_dependent=False)

    def update_old_loyalty_points(self):
        loyalty_field = self.env.ref('pos_loyalty.field_res_partner__loyalty_points')
        domain = [('fields_id','=',loyalty_field.id),
                ('res_id','!=',False),
                ('value_float','!=',0)]
        ir_properties = self.env['ir.property'].search(domain)
        obj_partner = self.env['res.partner']
        for ip in ir_properties:
            res_id_split = ip.res_id.split(',')
            if len(res_id_split) == 2:
                customer = obj_partner.browse(int(res_id_split[1]))
                customer.loyalty_points += ip.value_float