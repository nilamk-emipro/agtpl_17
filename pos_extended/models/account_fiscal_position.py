from odoo import models, fields, api

class FiscalPositionExt(models.Model):
    _inherit = 'account.fiscal.position'

    def search(self, args, **kwargs):
        configured_fpos = self._context.get('fpos')
        if configured_fpos:
            args.extend([('id', 'in', configured_fpos.ids)])
        return super(FiscalPositionExt, self).search(args, **kwargs)
