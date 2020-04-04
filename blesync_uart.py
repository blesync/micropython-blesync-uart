import bluetooth


#
# def write(self, conn_handle, value_handle, data):
#     blesync.gattc_write(conn_handle, value_handle, data)


class Service:
    uuid = NotImplemented

    @classmethod
    def get_characteristics(cls):
        return (
            attr_name, attr
            for attr_name, attr in cls.__dict__.items()
            if isinstance(attr, Characteristic)
        )


class ClientService(Service):
    def __init__(self, uuid):
        if uuid != self.uuid:
            raise ValueError





class UARTService(Service):
    uuid = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

    rx = Characteristic(
        bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
        bluetooth.FLAG_WRITE,
    )
    tx = Characteristic(
        bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
        bluetooth.FLAG_NOTIFY
    )


class UARTServer(UARTService):
    def on_rx_write(self, data):
        self.tx.notify(data)
