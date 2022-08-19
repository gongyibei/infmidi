from itertools import accumulate
from typing import Sequence, Union

from ..constants import DEGREE_TO_INDEX, SCALE_NAME_TO_INTERVALS
from ..core.clip import Clip
from ..core.convert import key2index
from ..exceptions import ParameterError
from ..warps import optional_inplace

__all__ = ["scale_map"]


@optional_inplace(False)
def scale_map(clip: Clip,
              key: str = 'C',
              scale: Union[str, Sequence[Union[int, str]]] = "") -> Clip:
    if isinstance(scale, str):
        itvs = SCALE_NAME_TO_INTERVALS[scale]
        idxs = [0]
        for itv in itvs:
            idxs.append(idxs[-1] + itv)
        mapping = []
        for i in range(len(idxs) - 1):
            cur = idxs[i]
            nxt = idxs[i + 1]
            mapping.append(cur)
            r = (nxt - cur - 1) // 2
            l = (nxt - cur - 1) - r
            mapping += [cur] * l + [nxt] * r

    elif isinstance(scale, Sequence):
        if isinstance(scale[0], int):
            mapping = scale
        elif isinstance(scale[0], str):
            mapping = [DEGREE_TO_INDEX[degree] for degree in scale]
        else:
            ParameterError(f"Invalid value of scale: {scale}")
    else:
        ParameterError(f"Invalid value of scale: {scale}")

    for note in clip.notes:
        idx = key2index(note.key, key)
        note += mapping[idx] - idx
    return clip
