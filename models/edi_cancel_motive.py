# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class EdiCancelMotive(models.Model):
    _name = 'edi.cancel.motive'
    _description = 'Edi Cancel Motive'  # TODO
    _rec_name = 'code'

    code = fields.Char()
    description = fields.Char()

    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('description', 'code')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '{0} - {1}'.format(record.code, record.description)


