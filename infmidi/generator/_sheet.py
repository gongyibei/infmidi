import re
from typing import Callable, Dict

from .. import Clip, Note
from ..core.convert import drum2value
from ._chord import chord

__all__ = [
    'sheet',
]


def _chord_and_note_sheet(item: str, length: float):

    def _note(note, length):
        return Note(note, length=length)

    def _chord(chord_name, length):
        root, chord_type = chord_name.split(':')
        return chord(root, chord_type, length=length)

    if item.isdigit():
        return _note(int(item), length)
    if re.match('[ABCDEFG][b#]*[0-9]$', item):
        return _note(item, length)
    if re.match('[ABCDEFG][b#]*[0-9]:\S*$', item):
        return _chord(item, length)


DEFAULT_MAPPING = {
    # Kick
    'K':
    lambda _, length: Note(
        drum2value('Acoustic Bass Drum'), length=length, channel=9),
    # Flore Tom
    'FT':
    lambda _, length: Note(
        drum2value('Low Floor Tom'), length=length, channel=9),
    # Tom Drum1
    'T':
    lambda _, length: Note(drum2value('High Tom'), length=length, channel=9),
    'HT':
    lambda _, length: Note(drum2value('High Tom'), length=length, channel=9),
    # Tom Drum2
    'LT':
    lambda _, length: Note(drum2value('Low Tom'), length=length, channel=9),
    # Snare Drum
    'S':
    lambda _, length: Note(
        drum2value('Acoustic Snare'), length=length, channel=9),
    # Ride Cymbal
    'R':
    lambda _, length: Note(
        drum2value('Ride Cymbal 1'), length=length, channel=9),
    # Closed Hi-Hat
    'H':
    lambda _, length: Note(
        drum2value('Closed Hi Hat'), length=length, channel=9),
    'CH':
    lambda _, length: Note(
        drum2value('Closed Hi Hat'), length=length, channel=9),
    # Open Hi-Hat
    'OH':
    lambda _, length: Note(drum2value('Open Hi Hat'), length=length, channel=9
                           ),
    # Hi-Hat Pedal
    'PH':
    lambda _, length: Note(
        drum2value('Pedal Hi Hat'), length=length, channel=9),
    # Crash Cymbal
    'CC':
    lambda _, length: Note(
        drum2value('Crash Cymbal 1'), length=length, channel=9),
    # note and chord
    '*':
    _chord_and_note_sheet
}


def sheet(text: str,
          mapping: Dict = DEFAULT_MAPPING,
          length_per_bar: float = 4.,
          bar_symbol: str = '|',
          rest_symbol: str = '0',
          delay_symbol: str = '-') -> Clip:
    res, n_bars = _parse_sheet(text, bar_symbol, delay_symbol)
    clip = Clip()
    loc = 0
    new_res = []

    for key, ration in res:
        length = ration * length_per_bar
        if key == rest_symbol:
            pass
        elif key == delay_symbol:
            if new_res:
                new_res[-1][1] += length
        else:
            new_res.append([key, length, loc])

        loc += length

    for key, length, loc in new_res:

        if key in mapping:
            val = mapping[key]
        else:
            val = mapping['*']

        if isinstance(val, Callable):
            val = val(key, length)
            clip.add(val, loc)
        elif isinstance(val, Note):
            clip.add(val, loc)
        elif isinstance(val, Clip):
            clip.add(val, loc)
    return clip


def _parse_sheet(sheet, bar_symbol, delay_symbol):
    bars = sheet.split(bar_symbol)
    n_bars = len(bars)
    res = []
    for bar in bars:
        bar = bar.strip()
        res.extend(_parse_bar(bar.strip(), delay_symbol))
    return res, n_bars


def _parse_bar(bar: str, delay_symbol):
    bar = _read_from_tokens(_tokenize(bar))

    def _parse(bar, ration):
        res = []
        l0 = 1 / len(bar) * ration
        for item in bar:
            if isinstance(item, list):
                res.extend(_parse(item, l0))
            elif item == delay_symbol:
                if res:
                    res[-1][1] += l0
                else:
                    res.append([delay_symbol, l0])
            else:
                res.append([item, l0])
        return res

    return _parse(bar, 1)


# borrowed from https://github.com/fluentpython/lispy
def _tokenize(s):
    s = f'({s})'
    s = s.replace('(', ' ( ').replace(')', ' ) ')
    s = s.split()
    return s


def _read_from_tokens(tokens):
    token = tokens.pop(0)
    if token == '(':
        exp = []
        while tokens and tokens[0] != ')':
            exp.append(_read_from_tokens(tokens))
        tokens.pop(0)
        return exp
    else:
        return token
