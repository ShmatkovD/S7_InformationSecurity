import argparse

alphabet = [unichr(i) for i in xrange(ord('a'), ord('z')+1)]


def encrypt(text, key):
    new_text = []
    for char in text:
        try:
            index = alphabet.index(char)
            new_text.append(alphabet[(index + key) % len(alphabet)])
        except:
            new_text.append(char)
    return ''.join(new_text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('key', type=int)
    parser.add_argument('input')
    parser.add_argument('output')
    arguments = parser.parse_args()

    with open(arguments.input, 'r') as input_file:
        text = input_file.read()

    with open(arguments.output, 'w') as outputfile:
        outputfile.write(
            encrypt(text, arguments.key)
        )
1