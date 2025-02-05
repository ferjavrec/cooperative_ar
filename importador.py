from trytond.model import ModelView, ModelSQL, fields
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.pyson import Eval, If
import StringIO
import csv
from decimal import Decimal
from trytond.pool import Pool


class ImportadorRecibosStart(ModelView):
    'Cooperative Partner Recibo Importador Start'
    __name__ = 'cooperative.partner.recibo.importador.start'

    company = fields.Many2One('company.company', 'Cooperativa', required=True,
                              domain=[
                                  ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                                   Eval('context', {}).get('company', -1)),
                              ], select=True)
    fecha = fields.Date('Fecha', required=True)
    periodo = fields.Char('Periodo Liquidado', size=None, required=True)
    archivo = fields.Binary('Archivo', filename="archivo_importar", required=True)


class ImportadorRecibos(Wizard):
    'Cooperative Partner Recibo Importador'
    __name__ = 'cooperative.partner.recibo.importador'

    start = StateView('cooperative.partner.recibo.importador.start',
        'cooperative_ar.cooperative_partner_recibo_importador_start_view_form', [
            Button('Cancelar', 'end', 'tryton-cancel'),
            Button('Importar', 'importar', 'tryton-ok', default=True),
            ])
    importar = StateTransition()

    def get_socio_id(self, socio):
        Partner = Pool().get('cooperative.partner')
        partner = Partner.search([
            ('file', '=', int(socio)),
        ])
        return partner[0] if partner else None

    def convert_to_decimal(self, valor):
        if isinstance(valor, str):
            valor = valor.replace('.', '').replace(',', '.')
        try:
            return Decimal(valor)
        except:
            raise ValueError("El valor no es valido para Decimal: {}".format(valor))

    def guardar_valor(self, valor):
        try:
            valor_num = self.convert_to_decimal(valor)
            return valor_num
        except ValueError:
            return None

    def es_entero(self, valor):
        try:
            int(valor)
            return True
        except ValueError:
            return False

    def transition_importar(self):
        archivo = StringIO.StringIO(self.start.archivo)
        periodo_liquidado = self.start.periodo
        company = self.start.company
        fecha = self.start.fecha

        spamreader = csv.reader(archivo, delimiter=';')
        for row in spamreader:
            socio_nro = row[0]

            if self.es_entero(socio_nro):
                partner = self.get_socio_id(socio_nro)
                amount = self.guardar_valor(row[1])

                if partner:
                    lineas = Pool().get('cooperative.partner.recibo')()
                    lineas.partner = partner
                    lineas.company = company
                    lineas.periodo_liquidado = periodo_liquidado
                    lineas.amount = amount
                    lineas.date = fecha
                    lineas.save()

        return 'end'