from __future__ import absolute_import, unicode_literals

from l4.task_4 import generate_keys, encrypt, decrypt
from l5.task_5 import sha256


def get_signature(message, secret_key):
    """Return encrypted sign of message
    :type message: unicode
    :param secret_key: tuple
    :rtype: int
    """
    message = message.encode()
    raw_sign = sha256(message)
    prepared_sign = int(raw_sign, base=16)

    signature = encrypt(prepared_sign, secret_key)
    return signature


def check_signature(message, signature, public_key):
    """Check signature of message
    :type message: unicode
    :type signature: int
    :type public_key: tuple
    :rtype: bool
    """
    message = message.encode()
    message_hash = int(sha256(message), base=16)

    original_hash = decrypt(signature, public_key)

    return message_hash == original_hash


def _test():

    message = 'Some random text written for testing lab.'

    public_key, private_key = generate_keys(512)

    signature = get_signature(message, private_key)

    print hex(signature)[2:-1]
    print len(bin(signature)) - 2

    print check_signature(message, signature, public_key)
    print check_signature(message, signature + 1, public_key)


if __name__ == '__main__':
    _test()
