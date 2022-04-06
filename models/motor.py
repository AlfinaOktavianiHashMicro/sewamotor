from odoo import api, fields, models


class motor(models.Model):
    _name = 'sewa.motor'
    _description = 'Data Motor dan harganya'

    name = fields.Char(string='Name')
    tipe = fields.Selection(string='Tipe Motor', selection=[('sportbike','Sportbike'), ('standart','Standart'),  ('skuter','Skuter'), ('dual-sport','Dual Sport'),('touring','Touring'),('cruiser','cruiser'),('retro','retro')])
    stok = fields.Integer(string='Stok Motor')
    harga = fields.Integer(string='Harga Sewa per Unit')
    
    
    
