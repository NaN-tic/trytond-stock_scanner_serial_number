#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.

from trytond.pool import Pool
from .stock import *


def register():
    Pool.register(
        ShipmentIn,
        ShipmentInReturn,
        ShipmentOut,
        ShipmentOutReturn,
        module='stock_scanner_serial_number', type_='model')
