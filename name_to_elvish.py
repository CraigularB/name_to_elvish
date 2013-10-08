from PIL import Image
from pprint import pprint
from os.path import join


_vowels = {'A', 'E', 'I', 'O', 'U'}
_special = {'LD', 'RD', 'TH', 'CH', 'SH', 'NT', 'ND', 'MP', 'MB'}
_letters = {'A': 'A.png',
            'B': 'B.png',
            'C': 'C.png',
            'D': 'D.png',
            'E': 'E.png',
            'F': 'F.png',
            'G': 'G.png',
            'H': 'H.png',
            'I': 'I.png',
            'J': 'J.png',
            'K': 'K.png',
            'L': 'L.png',
            'M': 'M.png',
            'N': 'N.png',
            'O': 'O.png',
            'P': 'P.png',
            'QU': 'QU.png',
            'R': 'R.png',
            'S': 'S.png',
            'T': 'T.png',
            'U': 'U.png',
            'V': 'V.png',
            'W': 'W.png',
            'X': 'X.png',
            'Y-C': 'Y-C.png',
            'Z': 'Z.png',
            '|': 'sep.png'}
_direction = {'A': 'U',
              'E': 'U',
              'I': 'U',
              'O': 'U',
              'U': 'U'}
_SQUARE_SIDE = 42


def create_image(charmap, name):
    open_images = dict()
    levels = 1
    top_level = False
    bottom_level = False
    extended = [charset for charset in charmap if len(charset) > 1]
    for entry in extended:
        for t in entry[1:]:
            if t[1] == 'U' and not top_level:
                levels += 1
                top_level = True
            elif t[1] == 'D' and not bottom_level:
                levels += 1
                bottom_level = True
        if top_level and bottom_level:
            break
    total_img_len = len(charmap)
    current_position = (0,42)
    img = Image.new("RGB", (total_img_len*_SQUARE_SIDE,levels*_SQUARE_SIDE),'white')
    for char in charmap:
        if char[0] not in open_images:
            open_images[char[0]] = Image.open(join('letters',_letters[char[0]]))
        img.paste(open_images[char[0]], current_position)
        if len(char) > 1:
            for tup in char[1:]:
                if tup[0] not in open_images:
                    open_images[tup[0]] = Image.open(join('letters',_letters[tup[0]]))
                if tup[1] == 'U':
                    img.paste(open_images[tup[0]], (current_position[0], current_position[1] - _SQUARE_SIDE))
                else:
                    raise Exception('OOPS')
        current_position = (current_position[0] + _SQUARE_SIDE, current_position[1])
    img.save('%s.png' % name, 'PNG')


def make_map(name):
    final = []
    letters = list(name)
    prev_was_vowel = False
    for letter in letters:
        if letter not in _vowels:
            final.append([letter])
            prev_was_vowel = False
        else:
            if not final:
                final.append(['|'])
            elif prev_was_vowel:
                final.append(['|'])
            final[-1].append((letter, 'U'))
            prev_was_vowel = True
    print(final)
    pprint(final)
    create_image(final, name)


def main():
    name = input("Please enter a name: ")
    while not name.isalpha():
        print('Invalid input. Names should contain only letters.')
        name = input("Please enter a name: ")
    name = name.upper()
    make_map(name)


if __name__ == "__main__":
    main()