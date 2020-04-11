import blesync_server
import bluetooth


class UARTService(blesync_server.Service):
    uuid = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

    # def on_received_message(self, message):
    #     pass

    tx = blesync_server.Characteristic(
        bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
        bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
        # on_received_message,
    )

    rx = blesync_server.Characteristic(
        bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
        bluetooth.FLAG_WRITE,
        buffer_size=100,
        append=True
    )

    characteristics = (tx, rx)

    def send(self, message):
        self.tx.write(message)
