# -*- coding: utf-8 -*-
# from odoo import http


# class Chatbot-test(http.Controller):
#     @http.route('/chatbot-test/chatbot-test', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/chatbot-test/chatbot-test/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('chatbot-test.listing', {
#             'root': '/chatbot-test/chatbot-test',
#             'objects': http.request.env['chatbot-test.chatbot-test'].search([]),
#         })

#     @http.route('/chatbot-test/chatbot-test/objects/<model("chatbot-test.chatbot-test"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('chatbot-test.object', {
#             'object': obj
#         })
