from ..midi import Note, Midi
import random

CHORD_TYPE_TO_INTERVALS = {
        'M': [4, 3],
        'm': [3, 4],
        '7': [4, 3, 3],
        'm7': [3, 4, 3],
        'mM7': [3, 4, 4],
        'M7': [4, 3, 4],
        }


def chord(root, chord_type):
    mid = Midi()
    intervals = CHORD_TYPE_TO_INTERVALS[chord_type]
    note = Note(root)
    mid.add(note)
    notes = []
    for itv in intervals:
        note = note + itv
        notes.append(note)
    for i in range(8):
        note = random.choice(notes)
        loc = random.randint(1, 7)/8
        mid.add(note, loc)
    return mid


