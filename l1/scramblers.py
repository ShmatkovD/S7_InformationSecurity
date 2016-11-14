import argparse

KEY = '11001'


def read(filename):
    with open(filename, 'r') as input_file:
        return input_file.readline().strip()


def write(filename, line):
    with open(filename, 'w') as output_file:
        output_file.write(line)


def crypt(line):

    key = map(int, KEY)
    crypted_line = []

    for index in xrange(len(line)):
        encrypting_bit = int(line[index])
        crypted_bit = (key[-1]) ^ encrypting_bit
        crypted_line.append(str(crypted_bit))
        key = key[1:] + [key[0] ^ key[1] ^ key[-1]]

    return ''.join(crypted_line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('key', type=int)
    parser.add_argument('input')
    parser.add_argument('output')

    arguments = parser.parse_args()

    KEY = bin(arguments.key)[2:]

    with open(arguments.input, 'r') as infile:
        with open(arguments.output, 'w') as outfile:
            for char in infile.read():
                result = crypt(
                    bin(ord(char))[2:]
                )
                outfile.write(
                    chr(int(result, base=2))
                )

