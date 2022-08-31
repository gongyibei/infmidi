import random
from ..core.clip import Clip

__all__ = []

def random_velocity(clip:Clip, min_velocity: int=0, max_velocity: int=127) -> Clip:
    for note in clip.notes:
        note.velocity = random.randint(min_velocity, max_velocity)
    return clip

def uniform_velocity(clip:Clip, min_velocity: int=0, max_velocity: int=127) -> Clip:
    for note in clip.notes:
        note.velocity = random.uniform(min_velocity, max_velocity)
    return clip