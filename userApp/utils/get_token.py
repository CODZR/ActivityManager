import uuid


def generate_token():
    random_str = str(uuid.uuid4()).replace('-', '')
    return random_str
