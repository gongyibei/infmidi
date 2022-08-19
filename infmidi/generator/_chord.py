from typing import Optional, Sequence, Union

from .. import Clip, Note
from ..constants import CHORD_TYPE_TO_INTERVALS, DEGREE_TO_INDEX
from ..exceptions import ParameterError

__all__ = [
    "chord",
]


def _chord_from_type(root: str,
                     chord_type: str,
                     gap: float = 0,
                     length: float = 1.) -> Clip:
    intervals = CHORD_TYPE_TO_INTERVALS[chord_type]
    return _chord_from_intervals(root, intervals, gap, length)


def _chord_from_intervals(root: str,
                          intervals: Sequence[int],
                          gap: float = 0.,
                          length: float = 1.) -> Clip:
    clip = Clip()
    note = Note(root, length=length)
    clip.add(note)
    loc = 0
    for itv in intervals:
        note = note + itv
        loc += gap
        clip.add(note, loc)

    return clip


def _chord_from_degrees(root: str,
                        degrees: Sequence[str],
                        gap: float = 0.,
                        length: float = 1.) -> Clip:
    indexes = [DEGREE_TO_INDEX[num] for num in degrees]
    intervals = []
    for i in range(len(indexes) - 1):
        itv = indexes[i + 1] - indexes[i]
        itv = (itv + 11) % 12 + 1
        intervals.append(itv)
    root = (Note(root) + indexes[0]).name
    return _chord_from_intervals(root, intervals, gap, length)


def chord(*args, gap: float = 0., length: float = 1.) -> Optional[Clip]:
    if len(args) == 1 and isinstance(args[0], str):
        root, chd = args[0].split(':')
        return _chord_from_type(root, chd, gap, length)
    elif len(args) == 2:
        root, chd = args
        if isinstance(chd, str):
            return _chord_from_type(root, chd, gap, length)
        elif isinstance(chd, Sequence):
            if isinstance(chd[0], int):
                return _chord_from_intervals(root, chd, gap, length)
            elif isinstance(chd[0], str):
                return _chord_from_degrees(root, chd, gap, length)
    else:
        raise ParameterError("The lenght of args shoud be less than 2.")
