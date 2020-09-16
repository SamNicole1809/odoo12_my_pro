# -*- coding: utf-8 -*-
from odoo import http

# class Classroom(http.Controller):
#     @http.route('/classroom/classroom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/classroom/classroom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('classroom.listing', {
#             'root': '/classroom/classroom',
#             'objects': http.request.env['classroom.classroom'].search([]),
#         })

#     @http.route('/classroom/classroom/objects/<model("classroom.classroom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('classroom.object', {
#             'object': obj
#         })