import blesync_client
import bluetooth


class UARTService(blesync_client.Service):
    uuid = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

    def on_received_message(self, message):
        pass

    _rx = blesync_client.Characteristic(
        bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
        on_received_message,
    )
    _tx = blesync_client.Characteristic(
        bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    )

    def send(self, message):
        self._tx.write(message)
