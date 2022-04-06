from odoo import api, fields, models


class helm(models.Model):
    _name = 'sewa.helm'
    _description = 'Data Helm dan harganya'

    name = fields.Char(string='Name')
    tipe = fields.Selection(string='Tipe Helm', selection=[('Full-face','Full-face'), ('Open Face','Open Face'),  ('Cross/Offroad','Offroad'), ('Dual Sport','Dual Sport')])
    stok = fields.Integer(string='Stok Helm')
    harga = fields.Integer(string='Harga Sewa per Unit')
    
    
    
