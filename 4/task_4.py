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


def module_pow(x, y, m):
    """Calculate x^y (mod m)
    :type x: int
    :type y: int
    :type m: int
    :rtype: int
    """
    if y == 0:
        return 1

    result = module_pow(x, y / 2, m)
    result = result * result % m

    if y % 2 == 1:
        result = (result * x) % m

    return result


def is_prime(n):
    """Check if n is prime
    :param n: number > 2
    :type n: int
    :rtype: bool
    """
    assert n > 2
    if n % 2 == 0:
        return False

    k = 50

    s = 0
    t = n - 1
    while t % 2 == 0:
        t /= 2
        s += 1

    for _ in xrange(k):
        a = randint(2, n - 2)
        x = module_pow(a, t, n)

        if x == 1 or x == n - 1:
            continue

        for _ in xrange(s - 1):
            x = x * x % n

            if x == 1:
                return False, 1

            if x == n - 1:
                break

        if x == n - 1:
            continue

        return False, 0, x

    return True


def generate_prime(length):
    """Return prime number with size length
    :type length:
    :rtype:
    """
    result = 0

    while not result:
        for _ in xrange(length):
            result *= 2
            result += randint(0, 1)

        result = result | 2 ** length | 1

        if not is_prime(result):
            result = 0

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

    e = 0
    d = 0

    while e <= 0 or d <= 0:
        e = get_exponent(eu)
        gcd, d, t = get_gcd(e, eu)
        if d == e:
            e = 0

    return (e, n), (d, n)


def encrypt(input, key, mod):
    """Encrypt list of numbers with key and module
    :type input: list
    :type key: int
    :type mod: int
    :rtype: str
    """
    input = [item % mod for item in input]
    output = []

    for item in input:
        output.append(
            module_pow(item, key, mod)
        )

    return output


if __name__ == '__main__':
    key_length = 3

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
