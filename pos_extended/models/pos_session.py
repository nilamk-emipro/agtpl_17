from odoo import models,api
from datetime import datetime
class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def create(self,vals):
        # if vals.get('name') and vals.vo:
        res = super(PosSession, self).create(vals)
        name = ''
        if vals.get('config_id'):
            name = 'POS/'
            pos_config = self.env['pos.config'].browse(vals.get('config_id'))
            next_number = pos_config.pos_sequence_id.next_by_id()
            if pos_config.store_short_code :
                name += '%s/'%(pos_config.store_short_code)
            name += '%s/%s'%(datetime.now().year,next_number)
        if name:
            res.name = name
        return res