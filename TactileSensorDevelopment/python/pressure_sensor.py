from comms_wrapper import Arduino

class Pressure_sensor:
    def __init__(self, port, baudrate) -> None:
        self.pressure_sensor = Arduino("pressure sensor", port, baudrate)
        self.pressure_sensor.connect_and_handshake()

    def read_sensor(self):
        self.pressure_sensor.receive_message()
        msg = self.pressure_sensor.receivedMessages

        output = {}
        for key, value in zip(msg.keys(), msg.values()):
            output[key] = float(value)

        return output