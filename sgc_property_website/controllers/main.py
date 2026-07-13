# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class PropertyWebsite(http.Controller):

    @http.route('/properties', type='http', auth='public', website=True, sitemap=True)
    def property_listing(self, **kwargs):
        properties = request.env['website.property'].sudo().search([
            ('website_published', '=', True),
            ('active', '=', True),
        ])
        featured = properties.filtered('is_featured')[:6]
        return request.render('sgc_property_website.property_listing_page', {
            'featured_properties': featured,
            'all_properties': properties,
            'property_types': request.env['website.property']._fields['property_type'].selection,
            'cities': request.env['website.property']._fields['city'].selection,
        })

    @http.route('/properties/<string:slug>', type='http', auth='public', website=True, sitemap=True)
    def property_detail(self, slug, **kwargs):
        property_record = request.env['website.property'].sudo().search([
            '|',
            ('slug', '=', slug),
            ('id', '=', slug),
        ], limit=1)
        if not property_record:
            return request.not_found()

        related_properties = request.env['website.property'].sudo().search([
            ('website_published', '=', True),
            ('active', '=', True),
            ('id', '!=', property_record.id),
            ('community', '=', property_record.community),
        ], limit=3)

        return request.render('sgc_property_website.property_detail_page', {
            'property': property_record,
            'related_properties': related_properties,
        })

    @http.route('/properties/search', type='http', auth='public', website=True)
    def property_search(self, **kwargs):
        domain = [
            ('website_published', '=', True),
            ('active', '=', True),
        ]
        if kwargs.get('q'):
            domain.append(('name', 'ilike', kwargs['q']))
        if kwargs.get('type'):
            domain.append(('property_type', '=', kwargs['type']))
        if kwargs.get('city'):
            domain.append(('city', '=', kwargs['city']))
        if kwargs.get('price_type'):
            domain.append(('price_type', '=', kwargs['price_type']))

        properties = request.env['website.property'].sudo().search(domain)

        return request.render('sgc_property_website.property_listing_page', {
            'featured_properties': request.env['website.property'],
            'all_properties': properties,
            'search_query': kwargs.get('q', ''),
            'search_type': kwargs.get('type', ''),
            'search_city': kwargs.get('city', ''),
            'property_types': request.env['website.property']._fields['property_type'].selection,
            'cities': request.env['website.property']._fields['city'].selection,
        })
