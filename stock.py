# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.modules.stock_scanner.stock import MIXIN_STATES


__all__ = ['ShipmentIn', 'ShipmentInReturn', 'ShipmentOut',
    'ShipmentOutReturn']

__metaclass__ = PoolMeta


class StockScanMixin(object):

    scanned_start_lot = fields.Char('Start Lot', states=MIXIN_STATES,
        depends=['state'])
    scanned_end_lot = fields.Char('End Lot', states=MIXIN_STATES,
        depends=['state'])

    @classmethod
    def clear_scan_values(cls, shipments):
        cls.write(shipments, {
            'scanned_start_lot': None,
            'scanned_end_lot': None,
        })
        super(StockScanMixin, cls).clear_scan_values(shipments)

    @classmethod
    def scan(cls, shipments):
        for shipment in shipments:
            shipment.scanned_product
            if not shipment.scanned_start_lot and not shipment.scanned_end_lot:
                continue
            for move in shipment.get_matching_moves():
                if move.product == shipment.scanned_product:
                    move.split_by_lot(1, move.uom,
                        start_lot=shipment.scanned_start_lot,
                        end_lot=shipment.scanned_end_lot)
        super(StockScanMixin, cls).scan(shipments)


class ShipmentIn(StockScanMixin):
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.in'


class ShipmentInReturn(ShipmentIn):
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.in.return'


class ShipmentOut(StockScanMixin):
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.out'


class ShipmentOutReturn(ShipmentOut):
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.out.return'
