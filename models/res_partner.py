from odoo import api, fields,models


class Partner(models.Model):
    _inherit = 'res.partner'
    
    is_pegawainya = fields.Boolean(string='Pegawai', default=False)
    is_customernya = fields.Boolean(string='Customer', default=False)
    
    
    
