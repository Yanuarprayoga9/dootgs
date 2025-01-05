from odoo import http
from odoo.http import request, Response
import json
# 10. Chat Bot Telegram untuk Pemesanan dan Status Pesanan

# Fitur Bot Telegram:
# 1. Pemrosesan Pemesanan:
# о Pelanggan dapat mengirimkan pesanan melalui bot telegram di odoo.
# о
# Bot memberikan formulir interaktif untuk memasukkan detail seperti jenis produk, ukuran, warna, dan jumlah.

# Bot memverifikasi ketersediaan stok dan memberikan nomor pesanan (quotation) kepada pelanggan.
# Jika oke maka akan mengubah Quotation jadi Sales Order
# 2. Cek Status Pesanan:
# O
# 0
# wwwwww
# Pelanggan memasukkan nomor pesanan.
# www
# Bot memberikan informasi status (e.g., "Pesanan Anda sedang dalam proses sablon" atau "Pesanan Anda telah dikirim dengan nomor resi [ABC123]").

# 3. Konfirmasi Pesanan Diterima
# O Bot mengirimkan pembaruan otomatis saat status pesanan selesai memberikan Delivery Order dan Memberikan pertanyaan feedback dan setelah dijawab maka akan tersimpan juga di odoo nya jawaban feedbacknya.

# Buatkan chatbot odoo 
# 1. buatkan api di odoo sesuai requirement dan ss modul yang ada
# 2. integrasikan menggunakan node js untuk terhubung ke telegram 
 
class TelegramBotController(http.Controller):

    from odoo import http
from odoo.http import request, Response
import json
# 10. Chat Bot Telegram untuk Pemesanan dan Status Pesanan

# Fitur Bot Telegram:
# 1. Pemrosesan Pemesanan:
# о Pelanggan dapat mengirimkan pesanan melalui bot telegram di odoo.
# о
# Bot memberikan formulir interaktif untuk memasukkan detail seperti jenis produk, ukuran, warna, dan jumlah.

# Bot memverifikasi ketersediaan stok dan memberikan nomor pesanan (quotation) kepada pelanggan.
# Jika oke maka akan mengubah Quotation jadi Sales Order
# 2. Cek Status Pesanan:
# O
# 0
# wwwwww
# Pelanggan memasukkan nomor pesanan.
# www
# Bot memberikan informasi status (e.g., "Pesanan Anda sedang dalam proses sablon" atau "Pesanan Anda telah dikirim dengan nomor resi [ABC123]").

# 3. Konfirmasi Pesanan Diterima
# O Bot mengirimkan pembaruan otomatis saat status pesanan selesai memberikan Delivery Order dan Memberikan pertanyaan feedback dan setelah dijawab maka akan tersimpan juga di odoo nya jawaban feedbacknya.

# Buatkan chatbot odoo 
# 1. buatkan api di odoo sesuai requirement dan ss modul yang ada
# 2. integrasikan menggunakan node js untuk terhubung ke telegram 
 
class TelegramBotController(http.Controller):
    # Check Stock (POST)
    # Check Stock (POST)
    @http.route('/api/stock', auth='public', type='http', methods=['POST'], csrf=False)
    def check_stock(self, **params):
        try:
            reqbody = json.loads(request.httprequest.data)
            product_name = reqbody.get('product_name')

            if not product_name:
                return Response(
                    json.dumps({"error": "Product name is required"}),
                    content_type='application/json',
                    status=400
                )

            product = request.env['product.product'].sudo().search([('name', '=', product_name)], limit=1)

            if not product:
                return Response(
                    json.dumps({"error": "Product not found"}),
                    content_type='application/json',
                    status=404
                )

            # Serialize the product object
            product_data = product.read(['id', 'display_name', 'qty_available', 'type', 'list_price'])[0]

            return Response(
                json.dumps(product_data),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                content_type='application/json',
                status=500
            )

  
    # Get All Orders (GET)
    @http.route('/api/orders', auth='none', type='http', methods=['GET'], csrf=False)
    def get_all_orders(self, **kw):
        try:
            orders = request.env['sale.order'].sudo().search([])
            result = [{
                'order_id': order.id,
                'order_name': order.name,
                'customer_name': order.partner_id.name,
                'state': order.state,
                'total_amount': order.amount_total
            } for order in orders]

            return Response(json.dumps(result), content_type='application/json', status=200)
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), content_type='application/json', status=500)

    # Get Order Status (GET)
    @http.route('/api/order_status', auth='none', type='http', methods=['GET'], csrf=False)
    def get_order_status(self, **params):
        try:
            order_name = params.get('order_name')

            if not order_name:
                return Response(json.dumps({"error": "Order name is required"}), content_type='application/json', status=400)

            order = request.env['sale.order'].sudo().search([('name', '=', order_name)], limit=1)

            if not order:
                return Response(json.dumps({"error": "Order not found"}), content_type='application/json', status=404)

            return Response(json.dumps({
                'order_id': order.id,
                'order_name': order.name,
                'state': order.state,
                'delivery_status': order.picking_ids.mapped('state')
            }), content_type='application/json', status=200)
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), content_type='application/json', status=500)

    # # Get All Products (GET)
    # @http.route('/api/products', auth='none', type='http', methods=['GET'], csrf=False)
    # def get_all_products(self, **kw):
    #     try:
    #         products = request.env['product.template'].sudo().search([])
    #         result = [{
    #             'product_id': product.id,
    #             'name': product.name,
    #             'list_price': product.list_price
    #         } for product in products]

    #         return Response(json.dumps(result), content_type='application/json', status=200)
    #     except Exception as e:
    #         return Response(json.dumps({"error": str(e)}), content_type='application/json', status=500)

    # # Save Feedback (POST)
    # @http.route('/api/feedback', auth='none', type='http', methods=['POST'], csrf=False)
    # def save_feedback(self, **params):
    #     try:
    #         reqbody = json.loads(request.httprequest.data)
    #         order_name = reqbody.get('order_name')
    #         feedback = reqbody.get('feedback')

    #         if not (order_name and feedback):
    #             return Response(json.dumps({"error": "Order name and feedback are required"}), content_type='application/json', status=400)

    #         # Search for the order by name
    #         order = request.env['sale.order'].sudo().search([('name', '=', order_name)], limit=1)

    #         if not order:
    #             return Response(json.dumps({"error": "Order not found"}), content_type='application/json', status=404)

    #         # Create feedback for the order
    #         request.env['order.feedback'].sudo().create({
    #             'order_name': order_name,
    #             'feedback': feedback
    #         })

    #         return Response(json.dumps({"message": "Feedback saved successfully"}), content_type='application/json', status=200)
    #     except Exception as e:
    #         return Response(json.dumps({"error": str(e)}), content_type='application/json', status=500)


   
    # Get All Orders (GET)
    @http.route('/api/orders', auth='none', type='http', methods=['GET'], csrf=False)
    def get_all_orders(self, **kw):
        try:
            orders = request.env['sale.order'].sudo().search([])
            result = [{
                'order_id': order.id,
                'order_name': order.name,
                'customer_name': order.partner_id.name,
                'state': order.state,
                'total_amount': order.amount_total
            } for order in orders]

            return Response(json.dumps(result), content_type='application/json', status=200)
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), content_type='application/json', status=500)

 
 
    # Save Feedback (POST)
    @http.route('/api/feedback', auth='none', type='http', methods=['POST'], csrf=False)
    def save_feedback(self, **params):
        try:
            reqbody = json.loads(request.httprequest.data)
            order_name = reqbody.get('order_name')
            feedback = reqbody.get('feedback')

            if not (order_name and feedback):
                return Response(json.dumps({"error": "Order name and feedback are required"}), content_type='application/json', status=400)

            # Search for the order by name
            order = request.env['sale.order'].sudo().search([('name', '=', order_name)], limit=1)

            if not order:
                return Response(json.dumps({"error": "Order not found"}), content_type='application/json', status=404)

            # Create feedback for the order
            request.env['order.feedback'].sudo().create({
                'order_name': order_name,
                'feedback': feedback
            })

            return Response(json.dumps({"message": "Feedback saved successfully"}), content_type='application/json', status=200)
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), content_type='application/json', status=500)

    # Get All Products (GET)
    @http.route('/api/products', auth='public', type='http', methods=['GET'], csrf=False)
    def get_all_products(self, **kw):
        try:
            products = request.env['product.template'].sudo().search([])
            result = [{
                'product_id': product.id,
                'name': product.name,
                'display_name': product.display_name,
                'list_price': product.list_price,
                'stock_available': product.qty_available,
                'stock_reserved': product.virtual_available,
                'uom': product.uom_id.name,  # Unit of Measure
                'category': product.categ_id.name,  # Product Category
                'description': product.description_sale or product.description or '',  # Product Description
            } for product in products]

            return Response(json.dumps(result), content_type='application/json', status=200)
        except Exception as e:
            return Response(json.dumps({"error": str(e)}), content_type='application/json', status=500)
