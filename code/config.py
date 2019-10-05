import ujson


ACCESS_POINT_MODE = False


class AccessPointConfig:
    SSID = 'ESP-32-WOOWOOWOO'
    PASSWORD = 'thisisnotaspoon'


class StationConfig:
    SSID = 'FunBox2-3F12'
    PASSWORD = '85371851YI'
    IP = '192.168.1.27'
    SUBNET_MASK = '255.255.255.0'
    GATEWAY = '192.168.1.1'


class IncorrectSlot(Exception):
    pass


def validate_slot(method):
    def new_method(self, slot, *args, **kwargs):
        if slot < 0 or slot >= self.quantity:
            raise IncorrectSlot
        return method(self, slot, *args, **kwargs)
    return new_method


class Slots:

    quantity = 3

    def __init__(self):
        self.indexes = {slot: 0 for slot in range(self.quantity)}
        self.messages = {slot: [] for slot in range(self.quantity)}

    @validate_slot
    def pop_message(self, slot):
        index = self.indexes[slot]
        messages = self.messages[slot]
        index = (index + 1) % len(messages)
        self.indexes[slot] = index
        return messages[index]

    @validate_slot
    def get(self, slot):
        return self.messages[slot]

    @validate_slot
    def set(self, slot, messages):
        self.indexes[slot] = 0
        self.messages[slot] = messages


class MidiMessages:

    config_json_path = '/code/config.json'

    def __init__(self):
        self.slots = Slots()

    def load(self):
        with open(self.config_json_path) as config_json:
            data = ujson.load(config_json)
            for slot, messages in enumerate(data['notes']):
                self.slots.set(slot, messages)

    def save(self):
        with open(self.config_json_path, 'w+') as config_json:
            ujson.dump({"notes": self.slots.messages}, config_json)


midi_messages = MidiMessages()
midi_messages.load()
