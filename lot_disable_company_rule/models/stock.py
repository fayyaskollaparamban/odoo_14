from odoo import models, fields, api

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    lot_id = fields.Many2one(domain="[('product_id', '=', product_id)]", check_company=False)

class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    prod_lot_id = fields.Many2one(check_company=False, domain="[('product_id','=',product_id)]")

class StockMOveLine(models.Model):
    _inherit = 'stock.move.line'

    lot_id = fields.Many2one(domain="[('product_id', '=', product_id)]", check_company=False)

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    _check_company_auto = False

    company_id = fields.Many2one(required=False)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        arg_to_del = []
        for arg in args:
            if len(arg) > 0 and arg[0] == 'company_id':
                arg_to_del.append(arg)
        for to_del in arg_to_del:
            args.remove(to_del)
        return super(StockProductionLot,self).search(args=args, offset=offset, limit=limit, order=order, count=count)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                vals['company_id'] = False
        res = super(StockProductionLot, self).create(vals_list)
        #some unknown case company_id set after create
        res.reset_company_id_failure()
        return res

    def reset_company_id_failure(self):
        self = self.filtered(lambda l: l.company_id)
        if self:
            qry = f"update stock_production_lot set company_id = null where id in {tuple(self.ids + [0])}"
            self._cr.execute(qry)

    def write(self, vals):
        if 'company_id' in vals:
            vals['company_id'] = False
        return super(StockProductionLot, self).write(vals)

    def reset_lot_company_pet_arabia(self):
        qry = "update stock_production_lot set company_id=null where company_id is not null"
        self._cr.execute(qry)
