from odoo import http, fields, models
from odoo.http import request
import json


class motorCon(http.Controller):
    @http.route(['/motor','/motor/<int:idnya>'], auth='public', methods=['GET'], csrf=True)
    def getmotor(self, idnya=None, **kwargs):
        value = []
        if not idnya:
            motor = request.env['sewa.motor'].search([])            
            for k in motor:
                value.append({"id": k.id,
                            "namamotor" : k.name,
                            "tipe" : k.tipe,
                            "stok_tersedia" : k.stok,
                            "harga_sewa" : k.harga})
            return json.dumps(value)
        else:
            motorid = request.env['sewa.motor'].search([('id','=',idnya)])
            for k in motorid:
                value.append({"id": k.id,
                            "namamotor" : k.name,
                            "tipe" : k.tipe,
                            "stok" : k.stok,
                            "harga_sewa" : k.harga})
            return json.dumps(value)
    
    @http.route('/createmotor',auth='user', type='json', methods=['POST'])
    def createmotor(self, **kw):    
        if request.jsonrequest:    
            if kw['name']:
                vals={
                    'name': kw['name'], 
                    'tipe' : kw['tipe'],
                    'stok' : kw['stok'],
                    'harga' : kw['harga'],
                }
                motorbaru = request.env['sewa.motor'].create(vals)
                args = {'success': True, 'ID':motorbaru.id}
                return args