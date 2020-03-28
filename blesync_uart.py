import blesync
import bluetooth


class BLEUARTService:
    def __init__(
        self,
        rxbuf=100,
    ):
        self.uuid = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        self.characteristics = {
            # RX
            bluetooth.UUID(
                "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"): bluetooth.FLAG_WRITE,
            # TX
            bluetooth.UUID(
                "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"): bluetooth.FLAG_NOTIFY,
        }

        self._rx_buf = rxbuf
        self._rx_handle = None
        self._tx_handle = None

    def register_handles(self, rx_handle, tx_handle):
        # Increase the size of the rx buffer and enable append mode.
        self._rx_handle, self._tx_handle = rx_handle, tx_handle
        blesync.gatts_set_buffer(self._rx_handle, self._rx_buf, True)

    def on_data_received(self, conn_handle, value_handle, received_data):
        print(conn_handle, value_handle, received_data)
        echo = b"ECHO %s" % received_data
        blesync.gatts_notify(conn_handle, self._tx_handle, echo)


#
# def write(self, conn_handle, value_handle, data):
#     blesync.gattc_write(conn_handle, value_handle, data)


class Service:
    uuid = NotImplemented
    characteristics = {}

    def __init__(self, uuid, conn_handle, start_handle, end_handle):
        self._handle_for_characteristics = {}
        if uuid != self.uuid:
            raise ValueError

        for def_handle, value_handle, properties, uuid in blesync.gattc_discover_characteristics(
            conn_handle, start_handle, end_handle
        ):
            if self.characteristics[uuid] != properties:
                raise ValueError

            self._handle_for_characteristics[uuid] = value_handle
            if len(self._handle_for_characteristics) == len(self.characteristics):
                break


class UARTService(Service):
    uuid = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
    characteristics = {
        # RX
        bluetooth.UUID(
            "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"): bluetooth.FLAG_WRITE,
        # TX
        bluetooth.UUID(
            "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"): bluetooth.FLAG_NOTIFY,
    }
