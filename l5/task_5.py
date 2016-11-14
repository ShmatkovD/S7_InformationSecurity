from __future__ import unicode_literals, absolute_import

# Realization of sha-256

_K = (
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
)
_MODULE = 1 << 32


def _int_to_bytes(number):
    """Making byte array from given int number. Used for translating length in bytes sequence
    :type number: int
    :rtype: bytearray
    """
    byte_sequence = []
    while number > 0:
        byte_sequence.append(number & 0xff)
        number >>= 8

    if len(byte_sequence) == 0:
        byte_sequence = [0]

    result = bytearray(reversed(byte_sequence))

    return result


def _bytes_to_int(byte_sequence):
    """Making int number from given bytes
    :type byte_sequence: bytearray
    :rtype: int
    """
    result = 0
    for b in byte_sequence:
        result = (result << 8) + int(b)

    return result


def _rotr(number, shift, bit_digits=32):
    """Cyclic shift of number with set bit digits
    :type number: int
    :type shift: int
    :type bit_digits: int
    :rtype: int
    """
    number = number & ((1 << bit_digits) - 1)  # cut the number to avoid surprises
    shifted_part = number & ((1 << shift) - 1)

    result = (number >> shift) | (shifted_part << (bit_digits - shift))

    return result


def _bits_count(number):
    """Return bit length of number
    :type number: int
    :rtype: int
    """
    result = len(bin(number)) - 2  # because function bin returns string value starts with '0b'
    return result


def sha256(message):
    """Return sha256 hash of given message
    :type message: str
    :rtype: str
    """

    H = (
        0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
        0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
    )

    byte_message = bytearray(message)
    message_length = len(byte_message) * 8

    zero_bits_count = 0
    while (message_length + 1 + zero_bits_count) % 512 != 448:
        zero_bits_count += 1

    byte_message.extend(
        _int_to_bytes(
            (1 << (zero_bits_count + 64)) | message_length
        )
    )

    for chunk_position in xrange(0, len(byte_message), 64):

        chunk = byte_message[chunk_position:chunk_position + 64]
        w = [
            _bytes_to_int(chunk[j:j + 4])
            for j in xrange(0, len(chunk), 4)
            ]

        # generating additional 48 words
        for i in xrange(16, 64):
            s0 = _rotr(w[i - 15], 7) ^ _rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = _rotr(w[i - 2], 17) ^ _rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w.append(
                (w[i - 16] + s0 + w[i - 7] + s1) % _MODULE
            )

        a, b, c, d, e, f, g, h = H

        # main cycle
        for i in xrange(64):
            summ0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
            Ma = (a & b) ^ (a & c) ^ (b & c)
            t2 = (summ0 + Ma) % _MODULE
            summ1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
            Ch = (e & f) ^ ((~e) & g)
            t1 = (h + summ1 + Ch + _K[i] + w[i]) % _MODULE

            h = g
            g = f
            f = e
            e = (d + t1) % _MODULE
            d = c
            c = b
            b = a
            a = (t1 + t2) % _MODULE

        H = tuple([
            (i + j) % _MODULE
            for i, j in zip(H, (a, b, c, d, e, f, g, h))
        ])

    result = 0
    for _h in H:
        result = (result << 32) + _h

    result = hex(result)[2:-1]

    return result


def _print_hash(data):
    result = sha256(data)

    beautiful_output = []
    for i, c in enumerate(result):
        if i != 0 and i % 8 == 0:
            beautiful_output.append(' ')

        beautiful_output.append(c)
    beautiful_output = ''.join(beautiful_output)

    print 'message: "{}"'.format(data)
    print 'hash: {}'.format(beautiful_output.upper())
    print '-'.join(['=' for _ in xrange(100)])


def _test():
    _print_hash('The quick brown fox jumps over the lazy dog'.encode())
    _print_hash('asdf'.encode())
    _print_hash(''.encode())
    _print_hash(
        'kja;lsdkfjalkjsdfnlkajbsdklfjnalksjdfnlkjasndflkjnalksjdfnlakjsdnflkajsdnlfkjanlskdjfnlakjsdfnlkajdfnlasdfasdf'
        'asdfasdfasdfasdfasdfasdfasdfsadfad'.encode()
    )


if __name__ == '__main__':
    _test()