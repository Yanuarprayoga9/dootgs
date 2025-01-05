from odoo import http
from odoo.http import request, Response
import json
from datetime import datetime

class QuotationController(http.Controller):
    @http.route('/api/quotation', auth='public', type='http', methods=['POST'], csrf=False)
    def create_quotation(self, **params):
        try:
            # Parsing request body
            reqbody = json.loads(request.httprequest.data)

            customer_id = reqbody.get('customer_id')
            product_id = reqbody.get('product_id')
            quantity = reqbody.get('quantity')
            unit_price = reqbody.get('unit_price')
            pricelist_id = reqbody.get('pricelist_id')
            payment_term_id = reqbody.get('payment_term_id')

            # Validation: Check if all fields are provided
            if not all([customer_id, product_id, quantity, unit_price, pricelist_id, payment_term_id]):
                return Response(
                    json.dumps({
                        "jsonrpc": "2.0",
                        "id": None,
                        "result": {
                            "success": False,
                            "error": "All fields are required: customer_id, product_id, quantity, unit_price, pricelist_id, payment_term_id"
                        }
                    }),
                    content_type='application/json',
                    status=400
                )

            # Create quotation in Odoo
            quotation = request.env['sale.order'].sudo().create({
                'partner_id': customer_id,
                'pricelist_id': pricelist_id,
                'payment_term_id': payment_term_id,
                'order_line': [(0, 0, {
                    'product_id': product_id,
                    'product_uom_qty': quantity,
                    'price_unit': unit_price,
                })]
            })

            # Serialize quotation data
            quotation_data = quotation.read(['id', 'name', 'date_order', 'amount_total', 'state'])[0]

            # Convert datetime to string (ISO 8601 format)
            if isinstance(quotation_data.get('date_order'), datetime):
                quotation_data['date_order'] = quotation_data['date_order'].isoformat()

            return Response(
                json.dumps({
                    "jsonrpc": "2.0",
                    "id": None,
                    "result": {
                        "success": True,
                        "data": quotation_data
                    }
                }),
                content_type='application/json',
                status=201
            )
        except Exception as e:
            # Handle unexpected errors
            return Response(
                json.dumps({
                    "jsonrpc": "2.0",
                    "id": None,
                    "result": {
                        "success": False,
                        "error": str(e)
                    }
                }),
                content_type='application/json',
                status=500
            )
    @http.route('/api/quotations', auth='public', type='http', methods=['GET'], csrf=False)
    def get_all_quotations(self, **params):
        try:
            # Ambil semua quotation dari model `sale.order`
            quotations = request.env['sale.order'].sudo().search([])

            # Serialisasi data quotation
            quotation_list = []
            for quotation in quotations:
                # Baca data dari setiap quotation
                data = quotation.read(['id', 'name', 'date_order', 'amount_total', 'state'])[0]
                
                # Konversi `datetime` ke string jika ada
                if isinstance(data.get('date_order'), datetime):
                    data['date_order'] = data['date_order'].isoformat()

                quotation_list.append(data)

            # Format respons
            return Response(
                json.dumps({
                    "jsonrpc": "2.0",
                    "id": None,
                    "result": {
                        "success": True,
                        "data": quotation_list
                    }
                }),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            # Tangani error tidak terduga
            return Response(
                json.dumps({
                    "jsonrpc": "2.0",
                    "id": None,
                    "result": {
                        "success": False,
                        "error": str(e)
                    }
                }),
                content_type='application/json',
                status=500
            )