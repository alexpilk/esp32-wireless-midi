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
