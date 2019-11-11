from code.config import midi_messages


class MidiMessage:

    def __init__(self, status, data_1=None, data_2=None):
        self.status = status
        self.data_1 = data_1
        self.data_2 = data_2

    @property
    def type(self):
        type_byte = self.status // 2 ** 4
        type_map = {
            0b1001: 'note_on',
            0b1000: 'note_off',
            0b1010: 'polyphonic',
            0b1011: 'cc',
            0b1100: 'pc',
            0b1101: 'channel_pressure',
            0b1110: 'pitch_bend'
        }
        return type_map[type_byte]

    @property
    def channel(self):
        channel_byte = self.status - (self.status // 2 ** 4) * 2 ** 4
        return channel_byte


def process_template(template, **kwargs):
    for var, value in kwargs.items():
        template = template.replace('{{{{ {var} }}}}'.format(var=var), str(value))
    return template


def render_notes(row, template):
    rows = ''
    print(midi_messages.slots.quantity)
    for slot in range(midi_messages.slots.quantity):
        print(slot)
        messages = midi_messages.slots.get(slot)
        print(messages)
        for message in messages:
            print(message)
            message = MidiMessage(*message)
            rendered_row = process_template(row, data_1=message.data_1, data_2=message.data_2, prefix='0_1', type=message.type, channel=message.channel)
            print(rendered_row)
            rows += rendered_row
    return process_template(template, row=rows)



def _get_slot(route_args):
    return int(route_args['slot'])


def get_note(http_client, http_response, route_args):
    slot = _get_slot(route_args)
    messages = midi_messages.slots.get(slot)
    http_response.WriteResponseJSONOk(messages, headers={'Access-Control-Allow-Origin': '*'})


def set_note(http_client, http_response, route_args):
    slot = _get_slot(route_args)
    messages = http_client.ReadRequestContentAsJSON()
    midi_messages.slots.set(slot, messages)
    http_response.WriteResponseOk()


def home(http_client, http_response):
    filename = 'index.html'
    row = '/code/html/row_template.html'
    template = '/code/html/index.html'
    with open(row) as row_file, open(template) as template_file:
        row_read = row_file.read()
        template_read = template_file.read()
        rendered = render_notes(row_read, template_read)
        # row_read = row_read.replace('{{ prefix }}', '1_1')
        # template_read = template_read.replace('{{ row }}', row_read)
        http_response.WriteResponseOk(contentType='text/html', content=rendered)
    # _serve_file(filename, 'text/html', http_response)


def css(http_client, http_response):
    _serve_file('bootstrap.min.css', 'text/css', http_response)


def js(http_client, http_response):
    _serve_file('bootstrapcreative.js', 'application/javascript', http_response)


def _serve_file(filename, content_type, http_response):
    http_response.WriteResponseFile('/code/html/{}'.format(filename), contentType=content_type, headers=None)
