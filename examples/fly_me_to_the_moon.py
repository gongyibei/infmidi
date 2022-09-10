from infmidi import Note, Clip, Track, Midi
from infmidi import chord, sheet
from infmidi import FluidSynth, Controller
from infmidi.effects.rhythm import delay


# ====== Initialize ======
synth = FluidSynth()
song = Midi(bpm=123, time_signature='4/4')


# ====== Track 1 ======
track1 = song.new_track('chord track', instrument=5)

txt = '''
    A4:m7 | D4:m9   | G4:7 | C4:M7     |
    F4:M7 | B3:m7-5 | E4:7 | A4:m7 A4:7
'''
progression = sheet(txt)
track1.add(progression)

# ====== Track 2 ======
track2 = song.new_track('melody track', instrument=12)

txt = '''
    (C5 -)  (-  B4)  (A4 G4)  (- F4) | (-  -)  (- G4)  (A4 C5)  (- B4) | 
     -      (-  A4)  (G4 F4)  (- E4) |  -               0              | 
    (A4 -)  (-  G4)  (F4 E4)  (- D4) |  -      (- E4)  (F4  A4)  -     |
     G#4    (F4 E4)  (-  D4)  (- C4) |  -       -       -        C#4   
'''

melody = sheet(txt)

delayed_melody = delay(melody, n=3, length=0.3, decay=0.7)
bass_melody = melody - 24

mixed_melody = delayed_melody + bass_melody
track2.add(mixed_melody)

# ====== play ======
synth(song)
