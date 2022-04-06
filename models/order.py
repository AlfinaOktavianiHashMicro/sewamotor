from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'sewa.order'
    _description = 'New Description'

    
    ordermotordetail_ids = fields.One2many(
        comodel_name='sewa.ordermotordetail', 
        inverse_name='orderk_id', 
        string='Order Motor')
    
    orderhelmdetail_ids = fields.One2many(
        comodel_name='sewa.orderhelmdetail', 
        inverse_name='orderk_id', 
        string='Order Helm')
    
    name = fields.Char(string='Kode Order', required=True)
    tanggal_pesan = fields.Datetime('Tanggal Pemesanan',default=fields.Datetime.now())
    tanggal_pengiriman = fields.Date(string='Tanggal Pengiriman', default=fields.Date.today())
    pemesan = fields.Many2one(
        comodel_name='res.partner', 
        string='Pemesan', 
        domain=[('is_customernya','=', True)],store=True)
        
    
    total = fields.Integer(compute='_compute_total', string='Total', store=True)
    
    sudah_kembali = fields.Boolean(string='Sudah Dikembalikan', default=False)
            
class OrdermotorDetail(models.Model):
    _name = 'sewa.ordermotordetail'
    _description = 'New Description'
    
    orderk_id = fields.Many2one(comodel_name='sewa.order', string='Order Motor')
    motor_id = fields.Many2one(
        comodel_name='sewa.motor', 
        string='Motor',
        domain=[('stok','>','100')])
    
    name = fields.Char(string='Name')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='harga satuan')
    
    @api.depends('motor_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.motor_id.harga
    
    qty = fields.Integer(string='Quantity')
    
    @api.constrains('qty')
    def _check_stok(self):
        for record in self:
            bahan = self.env['sewa.motor'].search([('stok', '<',record.qty),('id', '=',record.id)])
            if bahan:
                raise ValidationError("Stok motor yang dipilih tidak cukup")
    
    harga = fields.Integer(compute='_compute_harga', string='harga')
    
    @api.depends('harga_satuan','qty')
    def _compute_harga(self):
        for record in self:
               record.harga = record.harga_satuan * record.qty
               
    
    @api.model
    def create(self,vals):
        record = super(OrdermotorDetail, self).create(vals) 
        if record.qty:
            self.env['sewa.motor'].search([('id','=',record.motor_id.id)]).write({'stok':record.motor_id.stok-record.qty})
            return record
    

class OrderhelmDetail(models.Model):
    _name = 'sewa.orderhelmdetail'
    _description = 'New Description'
    
    orderk_id = fields.Many2one(comodel_name='sewa.order', string='Order Helm')
    helm_id = fields.Many2one(
        comodel_name='sewa.helm', 
        string='Helm',
        domain=[('stok','>','100')])
    
    name = fields.Char(string='Name')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='harga satuan')
    
    @api.depends('helm_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.helm_id.harga
    
    qty = fields.Integer(string='Quantity')
    
    @api.constrains('qty')
    def _check_stok(self):
        for record in self:
            bahan = self.env['sewa.helm'].search([('stok', '<',record.qty),('id', '=',record.id)])
            if bahan:
                raise ValidationError("Stok helm yang dipilih tidak cukup")
    
    harga = fields.Integer(compute='_compute_harga', string='harga')
    
    @api.depends('harga_satuan','qty')
    def _compute_harga(self):
        for record in self:
               record.harga = record.harga_satuan * record.qty
               
    
    @api.model
    def create(self,vals):
        record = super(OrderhelmDetail, self).create(vals) 
        if record.qty:
            self.env['sewa.helm'].search([('id','=',record.helm_id.id)]).write({'stok':record.helm_id.stok-record.qty})
            return record