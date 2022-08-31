from typing import Dict, Tuple

__all__ = [
    "KEY_TO_INDEX",
    "KEYS",
    "CONTROL_DESCRIPTIONS",
    "DEGREE_TO_INDEX",
    "CONTROL_DESCRIPTIONS",
    "INSTRUMENTS",
    "DRUM_SOUNDS",
    "MESSAGE_TYPE_TO_EVENT_TYPE",
]

#  +================================================================+
#  =                             BASIC                              =
#  +================================================================+

DEFAULT_TICKS_PER_BEAT: int = 480

KEY_TO_INDEX: Dict[str, int] = {
    'C': 0,
    'C#': 1,
    'D': 2,
    'D#': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'G': 7,
    'G#': 8,
    'A': 9,
    'A#': 10,
    'B': 11
}

KEYS: Tuple[str] = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#',
                    'B')

#  +================================================================+
#  =                           FOR SCALE                            =
#  +================================================================+

# ref: https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes
SCALE_NAME_TO_INTERVALS: Dict[str, Tuple[int]] = {
    '宫': (2, 2, 3, 2, 3),
    '商': (2, 3, 2, 3, 2),
    '角': (3, 2, 3, 2, 2),
    '徵': (2, 3, 2, 2, 3),
    '羽': (3, 2, 2, 3, 2),
    'Gong': (2, 2, 3, 2, 3),
    'Shang': (2, 3, 2, 3, 2),
    'Jue': (3, 2, 3, 2, 2),
    'Zhi': (2, 3, 2, 2, 3),
    'Yu': (3, 2, 2, 3, 2),
    'Ionian': (2, 2, 1, 2, 2, 2, 1),
    'Dorian': (2, 1, 2, 2, 2, 1, 2),
    'Phrygian': (1, 2, 2, 2, 1, 2, 2),
    'Lydian': (2, 2, 2, 1, 2, 2, 1),
    'Mixolydian': (2, 2, 1, 2, 2, 1, 2),
    'Aeolian': (2, 1, 2, 2, 1, 2, 2),
    'Locrian': (1, 2, 2, 1, 2, 2, 2),
}

#  +================================================================+
#  =                           FOR CHORD                            =
#  +================================================================+

CHORD_TYPE_TO_INTERVALS: Dict[str, Tuple[int]] = {
    # TODO. add more chord types
    # triad chord
    'm': (3, 4),
    'M': (4, 3),
    # seventh chord
    'm7': (3, 4, 3),
    'mM7': (3, 4, 4),
    '7': (4, 3, 3),
    'M7': (4, 3, 4),
    'm7-5': (3, 3, 4),
    # ninth chord
    'm9': (3, 4, 3, 4),
    '9': (4, 3, 3, 4),
    'M9': (4, 3, 4, 3),
    # eleventh chord
    'm11': (3, 4, 3, 4, 3),
    '11': (4, 3, 3, 4, 3),
    'M11': (4, 3, 4, 3, 3),
    # thirteenth chord
    'm13': (3, 4, 3, 4, 3, 4),
    '13': (4, 3, 3, 4, 3, 4),
    'M13': (4, 3, 4, 3, 3, 4),
    # other
    'add9': (4, 3, 7),
    'sus2': (2, 5),
    'sus4': (5, 2),
}

DEGREE_TO_INDEX: Dict[str, int] = {
    '1': 0,
    '#1': 1,
    'b2': 1,
    '2': 2,
    '#2': 3,
    'b3': 3,
    '3': 4,
    '#3': 5,
    'b4': 4,
    '4': 5,
    '#4': 6,
    'b5': 6,
    '5': 7,
    '#5': 8,
    'b6': 8,
    '6': 9,
    '#6': 10,
    'b7': 10,
    '7': 11,
    'b9': 1,
    '9': 2,
    '#9': 3,
    'b11': 4,
    '11': 5,
    '#11': 6,
    'b13': 8,
    '13': 9,
    '#13': 10,
}

#  +================================================================+
#  =                           FOR EVENT                            =
#  +================================================================+

# ref: https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2
CONTROL_DESCRIPTIONS = [
    'Bank Select',
    '* Modulation wheel',
    'Breath control',
    'Undefined',
    'Foot controller',
    'Portamento time',
    'Data Entry',
    'Channel Volume (formerly Main Volume)',
    'Balance',
    'Undefined',
    'Pan',
    'Expression Controller',
    'Effect control 1',
    'Effect control 2',
    'Undefined',
    'Undefined',
    'General Purpose Controller #1',
    'General Purpose Controller #2',
    'General Purpose Controller #3',
    'General Purpose Controller #4',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Bank Select',
    'Modulation wheel',
    'Breath control',
    'Undefined',
    'Foot controller',
    'Portamento time',
    'Data entry',
    'Channel Volume (formerly Main Volume)',
    'Balance',
    'Undefined',
    'Pan',
    'Expression Controller',
    'Effect control 1',
    'Effect control 2',
    'Undefined',
    'Undefined',
    'General Purpose Controller #1',
    'General Purpose Controller #2',
    'General Purpose Controller #3',
    'General Purpose Controller #4',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Damper pedal on/off (Sustain)',
    'Portamento on/off',
    'Sustenuto on/off',
    'Soft pedal on/off',
    'Legato Footswitch',
    'Hold 2',
    'Sound Controller 1 (Sound Variation)',
    'Sound Controller 2 (Timbre)',
    'Sound Controller 3 (Release Time)',
    'Sound Controller 4 (Attack Time)',
    'Sound Controller 5 (Brightness)',
    'Sound Controller 6',
    'Sound Controller 7',
    'Sound Controller 8',
    'Sound Controller 9',
    'Sound Controller 10',
    'General Purpose Controller #5',
    'General Purpose Controller #6',
    'General Purpose Controller #7',
    'General Purpose Controller #8',
    'Portamento Control',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Undefined',
    'Effects 1 Depth',
    'Effects 2 Depth',
    'Effects 3 Depth',
    'Effects 4 Depth',
    'Effects 5 Depth',
    'Data entry +1 ',
    'Data entry -1 ',
    'Non-Registered Parameter Number LSB',
    'Non-Registered Parameter Number MSB',
    'Registered Parameter Number LSB',
    'Registered Parameter Number MSB',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'Undefined ',
    'All Sound Off',
    'Reset All Controllers',
    'Local control on/off',
    'All notes off',
    'Omni mode off (+ all notes off)',
    'Omni mode on (+ all notes off)',
    'Poly mode on/off (+ all notes off)',
    'Poly mode on (incl mono=off +all notes off)',
]

# ref: https://www.recordingblogs.com/wiki/midi-program-change-message
PIANO: Tuple[str] = (
    'Acoustic Grand Piano',
    'Bright Acoustic Piano',
    'Electric Grand Piano',
    'Honky-tonk Piano',
    'Electric Piano 1',
    'Electric Piano 2',
    'Harpsichord',
    'Clavinet',
)

CHROMATIC_PERCUSSION: Tuple[str] = (
    'Celesta',
    'Glockenspiel',
    'Musical box',
    'Vibraphone',
    'Marimba',
    'Xylophone',
    'Tubular Bell',
    'Dulcimer',
)

ORGAN: Tuple[str] = (
    'Drawbar Organ',
    'Percussive Organ',
    'Rock Organ',
    'Church organ',
    'Reed organ',
    'Accordion',
    'Harmonica',
    'Tango Accordion',
)

GUITAR: Tuple[str] = (
    'Acoustic Guitar(nylon)',
    'Acoustic Guitar(steel)',
    'Electric Guitar(jazz)',
    'Electric Guitar(clean)',
    'Electric Guitar(muted)',
    'Overdriven Guitar',
    'Distortion Guitar',
    'Guitar harmonics',
)

BASS: Tuple[str] = (
    'Acoustic Bass',
    'Electric Bass(finger)',
    'Electric Bass(pick)',
    'Fretless Bass',
    'Slap Bass 1',
    'Slap Bass 2',
    'Synth Bass 1',
    'Synth Bass 2',
)

STRINGS: Tuple[str] = (
    'Violin',
    'Viola',
    'Cello',
    'Contrabass',
    'Tremolo Strings',
    'Pizzicato Strings',
    'Orchestral Harp',
    'Timpani',
)

ENSEMBLE: Tuple[str] = (
    'String Ensemble 1',
    'String Ensemble 2',
    'Synth Strings 1',
    'Synth Strings 2',
    'Voice Aahs',
    'Voice Oohs',
    'Synth Voice',
    'Orchestra Hit',
)

BRASS: Tuple[str] = (
    'Trumpet',
    'Trombone',
    'Tuba',
    'Muted Trumpet',
    'French horn',
    'Brass Section',
    'Synth Brass 1',
    'Synth Brass 2',
)

REED: Tuple[str] = (
    'Soprano Sax',
    'Alto Sax',
    'Tenor Sax',
    'Baritone Sax',
    'Oboe',
    'English Horn',
    'Bassoon',
    'Clarinet',
)

PIPE: Tuple[str] = (
    'Piccolo',
    'Flute',
    'Recorder',
    'Pan Flute',
    'Blown Bottle',
    'Shakuhachi',
    'Whistle',
    'Ocarina',
)

SYNTH_LEAD: Tuple[str] = (
    'Lead 1(square)',
    'Lead 2(sawtooth)',
    'Lead 3(calliope)',
    'Lead 4(chiff)',
    'Lead 5(charang)',
    'Lead 6(voice)',
    'Lead 7(fifths)',
    'Lead 8(bass + lead)',
)

SYNTH_PAD: Tuple[str] = (
    'Pad 1(new age)',
    'Pad 2(warm)',
    'Pad 3(polysynth)',
    'Pad 4(choir)',
    'Pad 5(bowed)',
    'Pad 6(metallic)',
    'Pad 7(halo)',
    'Pad 8(sweep)',
)

SYNTH_EFFECTS: Tuple[str] = (
    'FX 1(rain)',
    'FX 2(soundtrack)',
    'FX 3(crystal)',
    'FX 4(atmosphere)',
    'FX 5(brightness)',
    'FX 6(goblins)',
    'FX 7(echoes)',
    'FX 8(sci-fi)',
)

ETHNIC: Tuple[str] = (
    'Sitar',
    'Banjo',
    'Shamisen',
    'Koto',
    'Kalimba',
    'Bagpipe',
    'Fiddle',
    'Shanai',
)

PERCUSSIVE: Tuple[str] = (
    'Tinkle Bell',
    'Agogo',
    'Steel Drums',
    'Woodblock',
    'Taiko Drum',
    'Melodic Tom',
    'Synth Drum',
    'Reverse Cymbal',
)

SOUND_EFFECTS: Tuple[str] = (
    'Guitar Fret Noise',
    'Breath Noise',
    'Seashore',
    'Bird Tweet',
    'Telephone Ring',
    'Helicopter',
    'Applause',
    'Gunshot',
)

INSTRUMENTS = PIANO + CHROMATIC_PERCUSSION + ORGAN + GUITAR + \
    BASS + STRINGS + ENSEMBLE + BRASS + REED + PIPE + SYNTH_LEAD + \
    SYNTH_PAD + SYNTH_EFFECTS + ETHNIC + PERCUSSIVE + SOUND_EFFECTS

# ref: https://www.midi.org/specifications/item/gm-level-1-sound-set
DRUM_SOUNDS: Tuple[str] = (
    'Acoustic Bass Drum', 'Bass Drum 1', 'Side Stick', 'Acoustic Snare',
    'Hand Clap', 'Electric Snare', 'Low Floor Tom', 'Closed Hi Hat',
    'High Floor Tom', 'Pedal Hi Hat', 'Low Tom', 'Open Hi Hat', 'Low-Mid Tom',
    'Hi-Mid Tom', 'Crash Cymbal 1', 'High Tom', 'Ride Cymbal 1',
    'Chinese Cymbal', 'Ride Bell', 'Tambourine', 'Splash Cymbal', 'Cowbell',
    'Crash Cymbal 2', 'Vibraslap', 'Ride Cymbal 2', 'Hi Bongo', 'Low Bongo',
    'Mute Hi Conga', 'Open Hi Conga', 'Low Conga', 'High Timbale',
    'Low Timbale', 'High Agogo', 'Low Agogo', 'Cabasa', 'Maracas',
    'Short Whistle', 'Long Whistle', 'Short Guiro', 'Long Guiro', 'Claves',
    'Hi Wood Block', 'Low Wood Block', 'Mute Cuica', 'Open Cuica',
    'Mute Triangle', 'Open Triangle')

MESSAGE_TYPE_TO_EVENT_TYPE: Dict[str, str] = {
    'note_off': 'NoteOff',
    'note_on': 'NoteOn',
    'polytouch': 'NotePressure',
    'control_change': 'ControlChange',
    'program_change': 'ProgramChange',
    'aftertouch': 'ChannelPressure',
    'pitchwheel': 'PitchBend',
    'text': 'Text',
    'track_name': 'TrackName',
    'lyrics': 'Lyric',
    'marker': 'Marker',
    'cue_marker': 'CuePoint',
    'set_tempo': 'SetBpm',
    'time_signature': 'TimeSignature',
    'key_signature': 'KeySignature',
}

EVENT_TYPE_TO_MESSAGE_TYPE: Dict[str, str] = dict(
    zip(MESSAGE_TYPE_TO_EVENT_TYPE.values(),
        MESSAGE_TYPE_TO_EVENT_TYPE.keys()))
