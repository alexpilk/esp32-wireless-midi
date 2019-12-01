from code.config import midi_messages


def get_notes(http_client, http_response):
    messages = midi_messages.slots.messages
    http_response.WriteResponseJSONOk(messages, headers={'Access-Control-Allow-Origin': '*'})


def set_notes(http_client, http_response):
    slots = http_client.ReadRequestContentAsJSON()
    for slot, messages in enumerate(slots):
        midi_messages.slots.set(slot, messages)
    midi_messages.save()
    http_response.WriteResponseOk()
