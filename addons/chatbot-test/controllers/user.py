from odoo import http
from odoo.http import request
import re

class UserAPI(http.Controller):

    @http.route('/api/user', type='http', auth='public', methods=['GET'], csrf=False)
    def get_user_by_phone_or_name(self, **kwargs):
        """
        API untuk menampilkan nama pengguna berdasarkan nomor telepon atau nama.
        Query Parameters:
        - phone (string) : untuk mencari berdasarkan nomor telepon
        - name (string)  : untuk mencari berdasarkan nama
        """
        try:
            phone = kwargs.get('phone')
            name = kwargs.get('name')

            if not phone and not name:
                return request.make_response(
                    '{"error": "Parameter `phone` atau `name` harus diberikan."}',
                    headers={'Content-Type': 'application/json'}
                )

            domain = []

            # Jika ada nomor telepon, masukkan dalam pencarian
            if phone:
                formatted_phone = re.sub(r'\D', '', phone)
                domain += ['|', 
                           ('phone', 'ilike', formatted_phone),
                           ('mobile', 'ilike', formatted_phone)
                ]
            
            # Jika ada nama, masukkan dalam pencarian
            if name:
                domain.append(('name', 'ilike', name))

            # Cari pengguna berdasarkan domain
            user = request.env['res.partner'].sudo().search(domain, limit=1)

            if not user:
                return request.make_response(
                    '{"error": "Tidak ada pengguna ditemukan dengan parameter yang diberikan."}',
                    headers={'Content-Type': 'application/json'}
                )

            # Kembalikan data pengguna
            return request.make_response(
                f'{{"success": true, "data": {{"id": {user.id}, "name": "{user.name}", "phone": "{user.phone}"}}}}',
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            return request.make_response(
                f'{{"error": "{str(e)}"}}',
                headers={'Content-Type': 'application/json'}
            )

    @http.route('/api/users', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_users(self, **kwargs):
        """
        API untuk menampilkan semua pengguna.
        """
        try:
            users = request.env['res.partner'].sudo().search([])

            if not users:
                return request.make_response(
                    '{"error": "Tidak ada pengguna ditemukan."}',
                    headers={'Content-Type': 'application/json'}
                )

            # Kembalikan data semua pengguna
            users_data = [{"id": user.id, "name": user.name, "phone": user.phone} for user in users]
            return request.make_response(
                f'{{"success": true, "data": {users_data}}}',
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            return request.make_response(
                f'{{"error": "{str(e)}"}}',
                headers={'Content-Type': 'application/json'}
            )
