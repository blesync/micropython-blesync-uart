import blesync
import bluetooth


#
# def write(self, conn_handle, value_handle, data):
#     blesync.gattc_write(conn_handle, value_handle, data)


class Service:
    uuid = NotImplemented

    @classmethod
    def get_characteristics(cls):
        return (
            attr
            for attr_name, attr in cls.__dict__.items()
            if isinstance(attr, Characteristic)
        )

    def __init__(self, uuid, conn_handle, start_handle, end_handle):
        self.handles = {}
        if uuid != self.uuid:
            raise ValueError

        for def_handle, value_handle, properties, uuid in blesync.gattc_discover_characteristics(
            conn_handle, start_handle, end_handle
        ):
            if self.characteristics[uuid] != properties:
                raise ValueError

            self.handles[uuid] = value_handle
            if len(self.handles) == len(self.characteristics):
                break


class Characteristic:
    def __init__(self, uuid, flags):
        self.uuid = uuid
        self.flags = flags
        self.handle = None

    def notify(self, conn_handle, data=None):
        blesync.gatts_notify(conn_handle, self.handle, data)


class UARTService(Service):
    uuid = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

    rx = Characteristic(
        bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
        bluetooth.FLAG_WRITE
    )
    tx = Characteristic(
        bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
        bluetooth.FLAG_NOTIFY
    )


class UARTServerService(UARTService):
    pass


class BLEUARTService(UARTService):
    def on_data_received(self, characteristics, conn_handle, received_data):
        if characteristics != self.rx:
            return
        echo = b"ECHO %s" % received_data
        self.tx.notify(conn_handle, echo)

    pass
