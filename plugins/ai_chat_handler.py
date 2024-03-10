contexts = []

def get_context(msg_id):
    for context in contexts:
        if msg_id in context['ids']:
            return context
    return None
