from trytond.pool import Pool
from .partner import *
from .meeting import *
from .vacation import *
from .partnermeeting import *
from .sanction import *
from .recibo import Recibo, LineaConceptoRecibo, ReciboReport
from .account import *
from .company import *
from .importador import *


def register():
    Pool.register(Partner,
                  Meeting,
                  Vacation,
                  PartnerMeeting,
                  Sanction,
                  Recibo,
                  LineaConceptoRecibo,
                  FiscalYear,
                  Company,
                  ImportadorRecibosStart,
                  module='cooperative_ar', type_='model'
                  )
    Pool.register(
        ReciboReport,
        module='cooperative_ar', type_='report')
    Pool.register(
        ImportadorRecibos,
        module='cooperative_ar', type_='wizard')
