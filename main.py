from code import wifi, webpage


wifi.start_wifi()
webpage.run()

from machine import UART, Pin
import time


class Receiver:
    def __init__(self):
        self.uart = UART(1)
        self.uart.init(baudrate=9600, bits=8, parity=None, stop=1, tx=17, rx=16)
        self.led = Pin(4, Pin.OUT)

        self.EVENTS = {
            'Disconnected': self.reconnect,
            'presse': self.on_button
        }

    def connect(self):
        self.factory_default()
        self.reset()
        self.set_imme()
        self.set_master()
        self.reset()
        self.start()
        self.inquire()
        self.connect_first()
        self.loop()

    def on_button(self):
        print('YAY')
        self.led.on()
        time.sleep(1)
        self.led.off()

    def reconnect(self):
        while True:
            data = self.connect_first()
            if 'Connected' in data:
                return self.loop()
            time.sleep(1)

    def read(self):
        return self.uart.read()

    def run_command(self, command):
        self.uart.write(command+'\r\n')
        time.sleep(1)
        return self.wait()
        # print(self.uart.read())

    def reset(self):
        return self.run_command('AT+RESET')

    def factory_default(self):
        return self.run_command('AT+DEFAULT')

    def set_master(self):
        return self.run_command('AT+ROLE1')

    def set_imme(self):
        return self.run_command('AT+IMME1')

    def start(self):
        return self.run_command('AT+START')

    def inquire(self):
        return self.run_command('AT+INQ')

    def connect_first(self):
        return self.run_command('AT+CONN1')

    def wait(self):
        data = None
        while not data:
            data = self.read()
        print(data)
        return data

    def loop(self):
        while True:
            data = self.wait()
            for expected, action in self.EVENTS.items():
                if expected in str(data):
                    action()


# receiver = Receiver()
#
# if __name__ == '__main__':
#     receiver.connect()
