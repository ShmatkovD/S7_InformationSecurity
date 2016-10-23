from __future__ import unicode_literals, absolute_import

import collections
from random import randint

# RSA


def get_gcd(a, b):
    if a == 0:
        return b, 0, 1
    d, x1, y1 = get_gcd(b % a, a)
    x = y1 - (b / a) * x1
    y = x1

    return d, x, y


def is_prime(n):
    """Check if n is prime
    :param n: number > 2
    :type n: int
    :rtype: bool
    """
    if n == 2:
        return True

    if n < 2:
        return False

    k = 50

    s = 0
    t = n - 1
    while t % 2 == 0:
        t /= 2
        s += 1

    for _ in xrange(k):
        a = randint(2, max(n - 2, 2))
        x = pow(a, t, n)

        if x == 1 or x == (n - 1):
            continue

        for _ in xrange(s - 1):
            x = pow(x, 2, n)

            if x == 1:
                return False

            if x == n - 1:
                break

        if x == n - 1:
            continue

        return False

    return True


def generate_prime(length):
    """Return prime number with size length
    :type length:
    :rtype:
    """
    result = 0

    while True:
        result = randint(0, 2 ** length - 1)

        result = result | (2 ** (length - 1)) | 1

        if is_prime(result):
            return result


def get_prime_numbers(length):
    """Return 2 prime numbers with size length
    :type length: int
    :rtype: tuple
    """
    a = generate_prime(length)
    b = 0
    while a == b or b == 0:
        b = generate_prime(length)

    return a, b


def get_exponent(eu):
    """Return relatively prime to eu which less than eu
    :type eu: int
    :rtype: int
    """
    exp = 4
    max_iteration = 1000
    max_size = len(bin(eu)[2:])
    it = 0

    while (not is_prime(exp) or exp > eu) and it < max_iteration:
        size = randint(1, max_size)
        exp = 2 ** size + 1
        it += 1

    if not it < max_iteration:
        exp = generate_prime(max_size - 1)

    return exp


def generate_keys(key_length):

    p, q = get_prime_numbers(key_length)

    n = p * q
    eu = (p - 1) * (q - 1)

    gcd = 2
    while gcd != 1:
        e = get_exponent(eu)
        gcd, d, t = get_gcd(e, eu)

    if d < 0:
        d += eu

    assert (e * d) % eu == 1, 'e = {}; d = {}; eu = {}; t = {}'.format(e, d, eu, t)

    return (e, n), (d, n)


def encrypt(input, e, n):
    """Encrypt list of numbers with key and module
    :type input: list
    :type e: int
    :type n: int
    :rtype: str
    """
    input = [item % n for item in input]
    output = []

    for item in input:
        output.append(
            pow(item, e, n)
        )

    return output


if __name__ == '__main__':
    key_length = 20

    with open('input.txt', 'r') as f:
        items = [int(item) for item in f.readline().split(' ')]

    public_key, private_key = generate_keys(key_length)

    encrypted = encrypt(items, public_key[0], public_key[1])

    with open('encrypted.txt', 'w') as f:
        f.write(
            ' '.join(str(item) for item in encrypted)
        )

    decrypted = encrypt(encrypted, private_key[0], private_key[1])

    with open('decrypted.txt', 'w') as f:
        f.write(
            ' '.join(str(item) for item in decrypted)
        )
