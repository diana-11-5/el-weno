# Copyright 2021 Munin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from zeep import Client
from zeep.transports import Transport


class AccountMove(models.Model):
    _inherit = 'account.move'

    edi_cancel_reason_id = fields.Many2one(comodel_name="edi.cancel.motive", string="Motivo de Cancelacion",
                                           required=False, copy=False)
    replace_folio = fields.Char(string="Reemplazar Folio", copy=False)

    def _l10n_mx_edi_finkok_cancel(self, pac_info):
        '''CANCEL for Finkok.
        '''
        url = pac_info['url']
        username = pac_info['username']
        password = pac_info['password']
        for inv in self:
            uuid = inv.l10n_mx_edi_cfdi_uuid
            certificate_ids = inv.company_id.l10n_mx_edi_certificate_ids
            certificate_id = certificate_ids.sudo().get_valid_certificate()
            company_id = self.company_id
            cer_pem = certificate_id.get_pem_cer(
                certificate_id.content)
            key_pem = certificate_id.get_pem_key(
                certificate_id.key, certificate_id.password)
            cancelled = False
            code = False
            try:
                transport = Transport(timeout=20)
                client = Client(url, transport=transport)

                # uuid_type = client.get_type('ns0:stringArray')()
                # uuid_type.string = [uuid]
                # invoices_list = client.get_type('ns1:UUIDS')(uuid_type)
                #####################################
                uuid_type = client.get_type('ns1:UUID')()
                uuid_type.UUID = uuid
                uuid_type.FolioSustitucion = inv.replace_folio or ''
                if not inv.edi_cancel_reason_id:
                    raise UserError("reason not defined")
                uuid_type.Motivo = inv.edi_cancel_reason_id.code
                invoices_list = client.get_type('ns1:UUIDS')(uuid_type)
                #####################################
                response = client.service.cancel(
                    invoices_list, username, password, company_id.vat, cer_pem, key_pem)
            except Exception as e:
                inv.l10n_mx_edi_log_error(str(e))
                continue
            if not getattr(response, 'Folios', None):
                code = getattr(response, 'CodEstatus', None)
                msg = _("Cancelling got an error") if code else _(
                    'A delay of 2 hours has to be respected before to cancel')
            else:
                code = getattr(response.Folios.Folio[0], 'EstatusUUID', None)
                cancelled = code in ('201', '202')  # cancelled or previously cancelled
                # no show code and response message if cancel was success
                code = '' if cancelled else code
                msg = '' if cancelled else _("Cancelling got an error")
            inv._l10n_mx_edi_post_cancel_process(cancelled, code, msg)
