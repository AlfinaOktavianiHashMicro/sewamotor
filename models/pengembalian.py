from odoo import api, fields, models


class Pengembalian(models.Model):
    _name = 'sewa.pengembalian'
    _description = 'Pengembalian Barang Sewa'

    name = fields.Char(compute='_compute_nama_penyewa', string='nama penyewa')
    order_id = fields.Many2one(comodel_name='sewa.order', string='No. Order')
    
    @api.depends('order_id')
    def _compute_nama_penyewa(self):
        for record in self:
            record.name = self.env['sewa.order'].search([('id', '=', record.order_id.id)]).mapped('pemesan').name
    
    tgl_pengembalian = fields.Date(string='', default=fields.Date.today())
    
    tagihan = fields.Integer(compute='_compute_tagihan', string='tagihan')
    
    @api.depends('order_id')
    def _compute_tagihan(self):
        for record in self:
            record.tagihan = record.order_id.total            
   
        
    @api.model
    def create(self,vals):
        record = super(Pengembalian, self).create(vals) 
        if record.tgl_pengembalian:
            self.env['sewa.order'].search([('id','=',record.order_id.id)]).write({'sudah_kembali':True}) 
            self.env['sewa.akunting'].create({'kredit' : record.tagihan, 'name':record.name})          
            return record

    def unlink(self):
        for wiku in self:
            self.env['sewa.order'].search([('id','=',wiku.order_id.id)]).write({'sudah_kembali':False})
        record = super(Pengembalian, self).unlink()
   
        
            