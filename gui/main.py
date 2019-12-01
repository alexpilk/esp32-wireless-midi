from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
import requests
import json

MESSAGE_TYPES = {
    0b1001: 'note_on',
    0b1000: 'note_off',
    0b1010: 'polyphonic',
    0b1011: 'cc',
    0b1100: 'pc',
    0b1101: 'channel_pressure',
    0b1110: 'pitch_bend'
}
MESSAGE_TYPE_TO_BYTE = {v: k for k, v in MESSAGE_TYPES.items()}


class MidiMessage:

    def __init__(self, status, data_1=None, data_2=None):
        self.status = status
        self.data_1 = data_1
        self.data_2 = data_2

    @classmethod
    def from_form(cls, message_type, channel=None, data_1=None, data_2=None):
        status = MESSAGE_TYPE_TO_BYTE[message_type] * 2 ** 4 + int(channel)
        return cls(status, int(data_1), int(data_2))

    @property
    def type(self):
        type_byte = self.status // 2 ** 4
        return MESSAGE_TYPES[type_byte]

    @property
    def channel(self):
        channel_byte = self.status - (self.status // 2 ** 4) * 2 ** 4
        return channel_byte

    @property
    def raw(self):
        return [self.status, self.data_1, self.data_2]


def get_slots():
    return json.loads(requests.get('http://192.168.1.27/notes/').text)


def set_slots(slots):
    slots = [[m.raw for m in messages] for messages in slots]
    return requests.post('http://192.168.1.27/notes/', json=slots)


class Message:

    def __init__(self, message_type=None, channel=None, data_1=None, data_2=None):
        self.type = Spinner(text=message_type or '<Select>', values=MESSAGE_TYPES.values())
        self.channel = Spinner(text=str(channel) or '1', values=(str(i) for i in range(1, 17)))
        self.data_1 = TextInput(multiline=False, input_type='number', text=str(data_1))
        self.data_2 = TextInput(multiline=False, input_type='number', text=str(data_2))

        inputs = [self.type, self.channel, self.data_1, self.data_2]
        del_button = Button(text='Delete')
        self.widgets = [del_button] + inputs
        del_button.widgets = self.widgets

    def to_midi(self):
        return MidiMessage.from_form(self.type.text, self.channel.text, self.data_1.text, self.data_2.text)


class LoginScreen(GridLayout):

    def __init__(self, slots, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 5
        self.row_force_default = True
        self.row_default_height = 40
        self.slots = slots

        self.slot_indexes = [31, 16, 6]
        for i, slot in enumerate(slots):
            headers = [
                Label(text=f'Slot {i}'), Label(text='Type'), Label(text='Channel'), Label(text='Data 1'),
                Label(text='Data 2')
            ]
            self._add(headers)
            for j, message in enumerate(slot):
                self._add(message.widgets)
                message.widgets[0].slot = slot
                message.widgets[0].message_index = j
                message.widgets[0].bind(on_press=self._remove)
            add_message_button = Button(text='Add message')
            add_message_button.slot = i
            add_message_button.bind(on_press=self.add_message)
            self._add([add_message_button, Label(), Label(), Label(), Label()])

        btn1 = Button(text='Update')
        btn1.bind(on_press=self.update)

        self._add([btn1])

    def add_message(self, button):
        slot = button.slot
        message = Message()
        self.slots[slot].append(message)
        self._add(message.widgets, index=self.slot_indexes[slot])

    def update(self, a):
        set_slots([[m.to_midi() for m in messages] for messages in self.slots])

    def _add(self, widgets, index=0):
        for widget in widgets:
            self.add_widget(widget, index=index)

    def _remove(self, button):
        for widget in button.widgets:
            self.remove_widget(widget)
        del button.slot[button.message_index]


class MidiApp(App):

    def build(self):
        slots = []
        for slot in get_slots():
            messages = []
            slots.append(messages)
            for message in slot:
                message = MidiMessage(*message)
                messages.append(Message(message.type, message.channel, message.data_1, message.data_2))

        return LoginScreen(slots)


if __name__ == '__main__':
    MidiApp().run()
