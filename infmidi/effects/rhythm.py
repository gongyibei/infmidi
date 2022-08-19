from ..core import Clip
from ..warps import optional_inplace

__all__ = ["delay"]

@optional_inplace(False)
def delay(clip: Clip, n: int = 1, length: float = 0.1, decay: float= 1.) -> Clip:
    for _ in range(n):
        clip += (clip & decay) >> (length / n)
    return clip