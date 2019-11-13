from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button

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
    import requests
    import json

    return [
        # [[200, 100, 100], [128, 123, 150]],
        json.loads(requests.get('http://192.168.1.27/note/0/').text),
        [],
        []
    ]


def set_slots(messages):
    slots = [m.raw for m in messages]
    print(slots)


class Message:

    def __init__(self, message_type=None, channel=None, data_1=None, data_2=None):
        headers = [
            Label(text='Type'), Label(text='Channel'), Label(text='Data 1'), Label(text='Data 2')
        ]
        # self._add(headers)
        self.type = Spinner(text=message_type or '<Select>', values=MESSAGE_TYPES.values())
        # print(status.text)
        self.channel = Spinner(text=str(channel) or '1', values=(str(i) for i in range(1, 17)))
        self.data_1 = TextInput(multiline=False, input_type='number', text=str(data_1))
        self.data_2 = TextInput(multiline=False, input_type='number', text=str(data_2))

        inputs = [self.type, self.channel, self.data_1, self.data_2]
        self.widgets = headers + inputs

    def to_midi(self):
        return MidiMessage.from_form(self.type.text, self.channel.text, self.data_1.text, self.data_2.text)


class LoginScreen(GridLayout):

    def __init__(self, messages, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 4
        self.row_force_default = True
        self.row_default_height = 40
        self.messages = messages
        for message in messages:
            self._add(message.widgets)
        btn1 = Button(text='Update')
        btn1.bind(on_press=self.update)#lambda x: print(messages[0].widgets[4].text))

        self._add([btn1])

    def update(self, a):
        print(a)
        set_slots([m.to_midi() for m in self.messages])

    def _add(self, widgets):
        for widget in widgets:
            self.add_widget(widget)


class MidiApp(App):

    def build(self):
        messages = []
        for slot in get_slots():
            for message in slot:
                message = MidiMessage(*message)
                messages.append(Message(message.type, message.channel, message.data_1, message.data_2))
        # messages = [
        #     Message(), Message(), Message()
        # ]
        return LoginScreen(messages)


if __name__ == '__main__':
    MidiApp().run()
