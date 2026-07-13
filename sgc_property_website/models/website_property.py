# -*- coding: utf-8 -*-
from odoo import api, fields, models


class WebsiteProperty(models.Model):
    _name = 'website.property'
    _description = 'Website Property Listing'
    _inherit = ['website.published.mixin', 'website.seo.metadata']
    _order = 'is_featured desc, sequence, id desc'
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    slug = fields.Char(compute='_compute_slug', store=True)
    description = fields.Text(translate=True)
    short_description = fields.Char(string='Tagline', translate=True, size=120)

    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('townhouse', 'Townhouse'),
        ('penthouse', 'Penthouse'),
        ('studio', 'Studio'),
        ('duplex', 'Duplex'),
        ('office', 'Office'),
        ('shop', 'Shop'),
        ('warehouse', 'Warehouse'),
        ('land', 'Land'),
    ], default='apartment', required=True)
    community = fields.Char(string='Community', translate=True)
    city = fields.Selection([
        ('dubai', 'Dubai'),
        ('abu_dhabi', 'Abu Dhabi'),
        ('sharjah', 'Sharjah'),
    ], default='dubai')
    address = fields.Char(string='Address', translate=True)

    bedrooms = fields.Integer(string='Bedrooms')
    bathrooms = fields.Integer(string='Bathrooms')
    area_sqft = fields.Integer(string='Area (sqft)')
    furnishing = fields.Selection([
        ('unfurnished', 'Unfurnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('fully_furnished', 'Fully Furnished'),
    ], default='unfurnished')

    price = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    price_type = fields.Selection([
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ], default='sale', required=True)

    completion_status = fields.Selection([
        ('ready', 'Ready'),
        ('off_plan', 'Off-Plan'),
        ('under_construction', 'Under Construction'),
    ], default='ready')
    handover_date = fields.Char(string='Handover Date', translate=True)

    project_id = fields.Many2one('construction.project', string='Construction Project')
    latitude = fields.Float(digits=(10, 7))
    longitude = fields.Float(digits=(10, 7))
    map_url = fields.Char(string='Map URL', compute='_compute_map_url')

    photo_ids = fields.One2many('website.property.photo', 'property_id', string='Photos')
    amenity_ids = fields.Many2many('website.property.amenity', string='Amenities')
    agent_name = fields.Char(string='Agent Name', translate=True)
    agent_phone = fields.Char(string='Agent Phone')
    agent_email = fields.Char(string='Agent Email')
    agent_photo_url = fields.Char(string='Agent Photo URL')

    sequence = fields.Integer(default=10)
    is_featured = fields.Boolean(string='Featured', default=False)
    active = fields.Boolean(default=True)

    @api.depends('name', 'community')
    def _compute_slug(self):
        for rec in self:
            base = (rec.name or '').lower().replace(' ', '-').replace('/', '-')
            community_part = (rec.community or '').lower().replace(' ', '-').replace('(', '').replace(')', '')
            rec.slug = f"{community_part}-{base}" if community_part else base

    @api.depends('latitude', 'longitude')
    def _compute_map_url(self):
        for rec in self:
            if rec.latitude and rec.longitude:
                rec.map_url = f"https://www.google.com/maps?q={rec.latitude},{rec.longitude}"
            else:
                rec.map_url = False

    def _get_website_url(self):
        self.ensure_one()
        return f'/properties/{self.slug or self.id}'


class WebsitePropertyPhoto(models.Model):
    _name = 'website.property.photo'
    _description = 'Website Property Photo'
    _order = 'sequence, id'

    property_id = fields.Many2one('website.property', required=True, ondelete='cascade', index=True)
    name = fields.Char(string='Caption', translate=True)
    image_1920 = fields.Image(string='Photo', max_width=1920, max_height=1920, required=True)
    image_128 = fields.Image(related='image_1920', max_width=128, max_height=128, store=True)
    sequence = fields.Integer(default=10)
    is_cover = fields.Boolean(string='Cover Photo', default=False)


class WebsitePropertyAmenity(models.Model):
    _name = 'website.property.amenity'
    _description = 'Property Amenity'
    _order = 'name'

    name = fields.Char(required=True, translate=True)
