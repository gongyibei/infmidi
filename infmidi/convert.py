def loc2tick(loc, ticks_per_beat, bpm):
    return loc * ticks_per_beat * 4


def tick2loc(ticks, ticks_per_beat, bpm):
    return ticks / ticks_per_beat / 4


def loc2second(loc, bpm):
    return 60 / bpm * loc * 4


def second2loc(second, bpm):
    return second * bpm / 60 / 4
