from code.config import midi_messages


def _get_slot(route_args):
    return int(route_args['slot'])


def get_note(http_client, http_response, route_args):
    slot = _get_slot(route_args)
    messages = midi_messages.slots.get(slot)
    http_response.WriteResponseJSONOk(messages)


def set_note(http_client, http_response, route_args):
    slot = _get_slot(route_args)
    messages = http_client.ReadRequestContentAsJSON()
    midi_messages.slots.set(slot, messages)
    http_response.WriteResponseOk()


def home(http_client, http_response):
    filename = 'index.html'
    _serve_file(filename, 'text/html', http_response)


def css(http_client, http_response):
    _serve_file('bootstrap.min.css', 'text/css', http_response)


def js(http_client, http_response):
    _serve_file('bootstrapcreative.js', 'application/javascript', http_response)


def _serve_file(filename, content_type, http_response):
    http_response.WriteResponseFile('/code/html/{}'.format(filename), contentType=content_type, headers=None)
