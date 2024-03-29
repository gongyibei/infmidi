Cheat sheet
===========

.. tab:: Event

    +---------------------+------------+---------------------+
    | Name                | Binary     | Mido type           |
    +=====================+============+=====================+
    | **ChannelEvent**                                       |
    +---------------------+------------+---------------------+
    | NoteOff             | 0x8X       | note_off            |
    +---------------------+------------+---------------------+
    | NoteOn              | 0x9X       | note_on             |
    +---------------------+------------+---------------------+
    | NotePressure        | 0xAX       | poly_touch          |
    +---------------------+------------+---------------------+
    | ControlChange       | 0xBX       | control_change      |
    +---------------------+------------+---------------------+
    | ProgramChange       | 0xCX       | program_change      |
    +---------------------+------------+---------------------+
    | ChannelPressure     | 0xDX       | aftertouch          |
    +---------------------+------------+---------------------+
    | PitchBend           | 0xEX       | pitchwheel          |
    +---------------------+------------+---------------------+
    | **SysexEvent (TODO.)**                                 |
    +---------------------+------------+---------------------+
    | **MetaEvent**                                          |
    +---------------------+------------+---------------------+
    | SequenceNumber      | 0xFF 0x00  | sequence_number     |
    +---------------------+------------+---------------------+
    | Text                | 0xFF 0x01  | text                |
    +---------------------+------------+---------------------+
    | Copyright           | 0xFF 0x02  | copyright           |
    +---------------------+------------+---------------------+
    | TrackName           | 0xFF 0x03  | track_name          |
    +---------------------+------------+---------------------+
    | Lyric               | 0xFF 0x05  | lyrics              |
    +---------------------+------------+---------------------+
    | Marker              | 0xFF 0x06  | marker              |
    +---------------------+------------+---------------------+
    | CuePoint            | 0xFF 0x07  | cue_marker          |
    +---------------------+------------+---------------------+
    | SetBpm              | 0xFF 0x51  | set_tempo           |
    +---------------------+------------+---------------------+
    | TimeSignature       | 0xFF 0x58  | time_signature      |
    +---------------------+------------+---------------------+
    | KeySignature        | 0xFF 0x59  | key_signature       |
    +---------------------+------------+---------------------+
    | SequencerSpcific    | 0xFF 0x7F  | sequencer_specific  |
    +---------------------+------------+---------------------+


.. tab:: Note

    .. csv-table:: 
        :widths: 4 5 5 14
        :header-rows: 1
        :align: center
        :file: ../_static/tabs/note.csv

.. tab:: Clip

    .. csv-table:: 
        :widths: 4 5 5 14
        :header-rows: 1
        :align: center
        :file: ../_static/tabs/clip.csv

.. tab:: Track

    .. csv-table:: 
        :widths: 4 5 5 14
        :header-rows: 1
        :align: center
        :file: ../_static/tabs/track.csv


.. tab:: Midi
    
    TODO.

.. tab:: Chord

    +-------+--------------+
    | Type  | Intervals    |
    +=======+==============+
    | m7    | 3 4 3        |
    +-------+--------------+
    | mM7   | 3 4 4        |
    +-------+--------------+
    | 7     | 4 3 3        |
    +-------+--------------+
    | M7    | 4 3 4        |
    +-------+--------------+
    | m7-5  | 3 3 4        |
    +-------+--------------+
    | m9    | 3 4 3 4      |
    +-------+--------------+
    | 9     | 4 3 3 4      |
    +-------+--------------+
    | M9    | 4 3 4 3      |
    +-------+--------------+
    | m11   | 3 4 3 4 3    |
    +-------+--------------+
    | 11    | 4 3 3 4 3    |
    +-------+--------------+
    | M11   | 4 3 4 3 3    |
    +-------+--------------+
    | m13   | 3 4 3 4 3 4  |
    +-------+--------------+
    | 13    | 4 3 3 4 3 4  |
    +-------+--------------+
    | M13   | 4 3 4 3 3 4  |
    +-------+--------------+
    | add9  | 4 3 7        |
    +-------+--------------+
    | sus2  | 2 5          |
    +-------+--------------+
    | sus4  | 5 2          |
    +-------+--------------+


.. tab:: Scale

    +-------------+----------------+
    | Name        | Intervals      |
    +=============+================+
    | 宫          | 2 2 3 2 3      |
    +-------------+----------------+
    | 商          | 2 3 2 3 2      |
    +-------------+----------------+
    | 角          | 3 2 3 2 2      |
    +-------------+----------------+
    | 徵          | 2 3 2 2 3      |
    +-------------+----------------+
    | 羽          | 3 2 2 3 2      |
    +-------------+----------------+
    | Gong        | 2 2 3 2 3      |
    +-------------+----------------+
    | Shang       | 2 3 2 3 2      |
    +-------------+----------------+
    | Jue         | 3 2 3 2 2      |
    +-------------+----------------+
    | Zhi         | 2 3 2 2 3      |
    +-------------+----------------+
    | Yu          | 3 2 2 3 2      |
    +-------------+----------------+
    | Ionian      | 2 2 1 2 2 2 1  |
    +-------------+----------------+
    | Dorian      | 2 1 2 2 2 1 2  |
    +-------------+----------------+
    | Phrygian    | 1 2 2 2 1 2 2  |
    +-------------+----------------+
    | Lydian      | 2 2 2 1 2 2 1  |
    +-------------+----------------+
    | Mixolydian  | 2 2 1 2 2 1 2  |
    +-------------+----------------+
    | Aeolian     | 2 1 2 2 1 2 2  |
    +-------------+----------------+
    | Locrian     | 1 2 2 1 2 2 2  |
    +-------------+----------------+


.. tab:: GM Instrument

    +-----------------------+-------------------------+
    | Id                    | Name                    |
    +=======================+=========================+
    | **Piano**                                       |
    +-----------------------+-------------------------+
    | 0                     | Acoustic Grand Piano    |
    +-----------------------+-------------------------+
    | 1                     | Bright Acoustic Piano   |
    +-----------------------+-------------------------+
    | 2                     | Electric Grand Piano    |
    +-----------------------+-------------------------+
    | 3                     | Honky-tonk Piano        |
    +-----------------------+-------------------------+
    | 4                     | Electric Piano 1        |
    +-----------------------+-------------------------+
    | 5                     | Electric Piano 2        |
    +-----------------------+-------------------------+
    | 6                     | Harpsichord             |
    +-----------------------+-------------------------+
    | 7                     | Clavinet                |
    +-----------------------+-------------------------+
    | **Chromatic percussion**                        |
    +-----------------------+-------------------------+
    | 8                     | Celesta                 |
    +-----------------------+-------------------------+
    | 9                     | Glockenspiel            |
    +-----------------------+-------------------------+
    | 10                    | Musical box             |
    +-----------------------+-------------------------+
    | 11                    | Vibraphone              |
    +-----------------------+-------------------------+
    | 12                    | Marimba                 |
    +-----------------------+-------------------------+
    | 13                    | Xylophone               |
    +-----------------------+-------------------------+
    | 14                    | Tubular Bell            |
    +-----------------------+-------------------------+
    | 15                    | Dulcimer                |
    +-----------------------+-------------------------+
    | **Organ**                                       |
    +-----------------------+-------------------------+
    | 16                    | Drawbar Organ           |
    +-----------------------+-------------------------+
    | 17                    | Percussive Organ        |
    +-----------------------+-------------------------+
    | 18                    | Rock Organ              |
    +-----------------------+-------------------------+
    | 19                    | Church organ            |
    +-----------------------+-------------------------+
    | 20                    | Reed organ              |
    +-----------------------+-------------------------+
    | 21                    | Accordion               |
    +-----------------------+-------------------------+
    | 22                    | Harmonica               |
    +-----------------------+-------------------------+
    | 23                    | Tango Accordion         |
    +-----------------------+-------------------------+
    | **Guitar**                                      |
    +-----------------------+-------------------------+
    | 24                    | Acoustic Guitar(nylon)  |
    +-----------------------+-------------------------+
    | 25                    | Acoustic Guitar(steel)  |
    +-----------------------+-------------------------+
    | 26                    | Electric Guitar(jazz)   |
    +-----------------------+-------------------------+
    | 27                    | Electric Guitar(clean)  |
    +-----------------------+-------------------------+
    | 28                    | Electric Guitar(muted)  |
    +-----------------------+-------------------------+
    | 29                    | Overdriven Guitar       |
    +-----------------------+-------------------------+
    | 30                    | Distortion Guitar       |
    +-----------------------+-------------------------+
    | 31                    | Guitar harmonics        |
    +-----------------------+-------------------------+
    | **Bass**                                        |
    +-----------------------+-------------------------+
    | 32                    | Acoustic Bass           |
    +-----------------------+-------------------------+
    | 33                    | Electric Bass(finger)   |
    +-----------------------+-------------------------+
    | 34                    | Electric Bass(pick)     |
    +-----------------------+-------------------------+
    | 35                    | Fretless Bass           |
    +-----------------------+-------------------------+
    | 36                    | Slap Bass 1             |
    +-----------------------+-------------------------+
    | 37                    | Slap Bass 2             |
    +-----------------------+-------------------------+
    | 38                    | Synth Bass 1            |
    +-----------------------+-------------------------+
    | 39                    | Synth Bass 2            |
    +-----------------------+-------------------------+
    | **Strings**                                     |
    +-----------------------+-------------------------+
    | 40                    | Violin                  |
    +-----------------------+-------------------------+
    | 41                    | Viola                   |
    +-----------------------+-------------------------+
    | 42                    | Cello                   |
    +-----------------------+-------------------------+
    | 43                    | Contrabass              |
    +-----------------------+-------------------------+
    | 44                    | Tremolo Strings         |
    +-----------------------+-------------------------+
    | 45                    | Pizzicato Strings       |
    +-----------------------+-------------------------+
    | 46                    | Orchestral Harp         |
    +-----------------------+-------------------------+
    | 47                    | Timpani                 |
    +-----------------------+-------------------------+
    | **Ensemble**                                    |
    +-----------------------+-------------------------+
    | 48                    | String Ensemble 1       |
    +-----------------------+-------------------------+
    | 49                    | String Ensemble 2       |
    +-----------------------+-------------------------+
    | 50                    | Synth Strings 1         |
    +-----------------------+-------------------------+
    | 51                    | Synth Strings 2         |
    +-----------------------+-------------------------+
    | 52                    | Voice Aahs              |
    +-----------------------+-------------------------+
    | 53                    | Voice Oohs              |
    +-----------------------+-------------------------+
    | 54                    | Synth Voice             |
    +-----------------------+-------------------------+
    | 55                    | Orchestra Hit           |
    +-----------------------+-------------------------+
    | **Brass**                                       |
    +-----------------------+-------------------------+
    | 56                    | Trumpet                 |
    +-----------------------+-------------------------+
    | 57                    | Trombone                |
    +-----------------------+-------------------------+
    | 58                    | Tuba                    |
    +-----------------------+-------------------------+
    | 59                    | Muted Trumpet           |
    +-----------------------+-------------------------+
    | 60                    | French horn             |
    +-----------------------+-------------------------+
    | 61                    | Brass Section           |
    +-----------------------+-------------------------+
    | 62                    | Synth Brass 1           |
    +-----------------------+-------------------------+
    | 63                    | Synth Brass 2           |
    +-----------------------+-------------------------+
    | **Reed**                                        |
    +-----------------------+-------------------------+
    | 64                    | Soprano Sax             |
    +-----------------------+-------------------------+
    | 65                    | Alto Sax                |
    +-----------------------+-------------------------+
    | 66                    | Tenor Sax               |
    +-----------------------+-------------------------+
    | 67                    | Baritone Sax            |
    +-----------------------+-------------------------+
    | 68                    | Oboe                    |
    +-----------------------+-------------------------+
    | 69                    | English Horn            |
    +-----------------------+-------------------------+
    | 70                    | Bassoon                 |
    +-----------------------+-------------------------+
    | 71                    | Clarinet                |
    +-----------------------+-------------------------+
    | **Pipe**                                        |
    +-----------------------+-------------------------+
    | 72                    | Piccolo                 |
    +-----------------------+-------------------------+
    | 73                    | Flute                   |
    +-----------------------+-------------------------+
    | 74                    | Recorder                |
    +-----------------------+-------------------------+
    | 75                    | Pan Flute               |
    +-----------------------+-------------------------+
    | 76                    | Blown Bottle            |
    +-----------------------+-------------------------+
    | 77                    | Shakuhachi              |
    +-----------------------+-------------------------+
    | 78                    | Whistle                 |
    +-----------------------+-------------------------+
    | 79                    | Ocarina                 |
    +-----------------------+-------------------------+
    | **Synth lead**                                  |
    +-----------------------+-------------------------+
    | 80                    | Lead 1(square)          |
    +-----------------------+-------------------------+
    | 81                    | Lead 2(sawtooth)        |
    +-----------------------+-------------------------+
    | 82                    | Lead 3(calliope)        |
    +-----------------------+-------------------------+
    | 83                    | Lead 4(chiff)           |
    +-----------------------+-------------------------+
    | 84                    | Lead 5(charang)         |
    +-----------------------+-------------------------+
    | 85                    | Lead 6(voice)           |
    +-----------------------+-------------------------+
    | 86                    | Lead 7(fifths)          |
    +-----------------------+-------------------------+
    | 87                    | Lead 8(bass + lead)     |
    +-----------------------+-------------------------+
    | **Synth pad**                                   |
    +-----------------------+-------------------------+
    | 88                    | Pad 1(new age)          |
    +-----------------------+-------------------------+
    | 89                    | Pad 2(warm)             |
    +-----------------------+-------------------------+
    | 90                    | Pad 3(polysynth)        |
    +-----------------------+-------------------------+
    | 91                    | Pad 4(choir)            |
    +-----------------------+-------------------------+
    | 92                    | Pad 5(bowed)            |
    +-----------------------+-------------------------+
    | 93                    | Pad 6(metallic)         |
    +-----------------------+-------------------------+
    | 94                    | Pad 7(halo)             |
    +-----------------------+-------------------------+
    | 95                    | Pad 8(sweep)            |
    +-----------------------+-------------------------+
    | **Synth effects**                               |
    +-----------------------+-------------------------+
    | 96                    | FX 1(rain)              |
    +-----------------------+-------------------------+
    | 97                    | FX 2(soundtrack)        |
    +-----------------------+-------------------------+
    | 98                    | FX 3(crystal)           |
    +-----------------------+-------------------------+
    | 99                    | FX 4(atmosphere)        |
    +-----------------------+-------------------------+
    | 100                   | FX 5(brightness)        |
    +-----------------------+-------------------------+
    | 101                   | FX 6(goblins)           |
    +-----------------------+-------------------------+
    | 102                   | FX 7(echoes)            |
    +-----------------------+-------------------------+
    | 103                   | FX 8(sci-fi)            |
    +-----------------------+-------------------------+
    | **Ethnic**                                      |
    +-----------------------+-------------------------+
    | 104                   | Sitar                   |
    +-----------------------+-------------------------+
    | 105                   | Banjo                   |
    +-----------------------+-------------------------+
    | 106                   | Shamisen                |
    +-----------------------+-------------------------+
    | 107                   | Koto                    |
    +-----------------------+-------------------------+
    | 108                   | Kalimba                 |
    +-----------------------+-------------------------+
    | 109                   | Bagpipe                 |
    +-----------------------+-------------------------+
    | 110                   | Fiddle                  |
    +-----------------------+-------------------------+
    | 111                   | Shanai                  |
    +-----------------------+-------------------------+
    | **Percussive**                                  |
    +-----------------------+-------------------------+
    | 112                   | Tinkle Bell             |
    +-----------------------+-------------------------+
    | 113                   | Agogo                   |
    +-----------------------+-------------------------+
    | 114                   | Steel Drums             |
    +-----------------------+-------------------------+
    | 115                   | Woodblock               |
    +-----------------------+-------------------------+
    | 116                   | Taiko Drum              |
    +-----------------------+-------------------------+
    | 117                   | Melodic Tom             |
    +-----------------------+-------------------------+
    | 118                   | Synth Drum              |
    +-----------------------+-------------------------+
    | 119                   | Reverse Cymbal          |
    +-----------------------+-------------------------+
    | **Sound effects**                               |
    +-----------------------+-------------------------+
    | 120                   | Guitar Fret Noise       |
    +-----------------------+-------------------------+
    | 121                   | Breath Noise            |
    +-----------------------+-------------------------+
    | 122                   | Seashore                |
    +-----------------------+-------------------------+
    | 123                   | Bird Tweet              |
    +-----------------------+-------------------------+
    | 124                   | Telephone Ring          |
    +-----------------------+-------------------------+
    | 125                   | Helicopter              |
    +-----------------------+-------------------------+
    | 126                   | Applause                |
    +-----------------------+-------------------------+
    | 127                   | Gunshot                 |
    +-----------------------+-------------------------+


.. tab:: GM Percussion

    +-------------+------------+---------------------+
    | Note Value  | Note Name  | Percussion Name     |
    +=============+============+=====================+
    | 35          | B1         | Acoustic Bass Drum  |
    +-------------+------------+---------------------+
    | 36          | C2         | Bass Drum 1         |
    +-------------+------------+---------------------+
    | 37          | C#2        | Side Stick          |
    +-------------+------------+---------------------+
    | 38          | D2         | Acoustic Snare      |
    +-------------+------------+---------------------+
    | 39          | Eb2        | Hand Clap           |
    +-------------+------------+---------------------+
    | 40          | E2         | Electric Snare      |
    +-------------+------------+---------------------+
    | 41          | F2         | Low Floor Tom       |
    +-------------+------------+---------------------+
    | 42          | F#2        | Closed Hi Hat       |
    +-------------+------------+---------------------+
    | 43          | G2         | High Floor Tom      |
    +-------------+------------+---------------------+
    | 44          | Ab2        | Pedal Hi Hat        |
    +-------------+------------+---------------------+
    | 45          | A2         | Low Tom             |
    +-------------+------------+---------------------+
    | 46          | Bb2        | Open Hi Hat         |
    +-------------+------------+---------------------+
    | 47          | B2         | Low-Mid Tom         |
    +-------------+------------+---------------------+
    | 48          | C3         | Hi-Mid Tom          |
    +-------------+------------+---------------------+
    | 49          | C#3        | Crash Cymbal 1      |
    +-------------+------------+---------------------+
    | 50          | D3         | High Tom            |
    +-------------+------------+---------------------+
    | 51          | Eb3        | Ride Cymbal 1       |
    +-------------+------------+---------------------+
    | 52          | E3         | Chinese Cymbal      |
    +-------------+------------+---------------------+
    | 53          | F3         | Ride Bell           |
    +-------------+------------+---------------------+
    | 54          | F#3        | Tambourine          |
    +-------------+------------+---------------------+
    | 55          | G3         | Splash Cymbal       |
    +-------------+------------+---------------------+
    | 56          | Ab3        | Cowbell             |
    +-------------+------------+---------------------+
    | 57          | A3         | Crash Cymbal 2      |
    +-------------+------------+---------------------+
    | 58          | Bb3        | Vibraslap           |
    +-------------+------------+---------------------+
    | 59          | B3         | Ride Cymbal 2       |
    +-------------+------------+---------------------+
    | 60          | C4         | Hi Bongo            |
    +-------------+------------+---------------------+
    | 61          | C#4        | Low Bongo           |
    +-------------+------------+---------------------+
    | 62          | D4         | Mute Hi Conga       |
    +-------------+------------+---------------------+
    | 63          | Eb4        | Open Hi Conga       |
    +-------------+------------+---------------------+
    | 64          | E4         | Low Conga           |
    +-------------+------------+---------------------+
    | 65          | F4         | High Timbale        |
    +-------------+------------+---------------------+
    | 66          | F#4        | Low Timbale         |
    +-------------+------------+---------------------+
    | 67          | G4         | High Agogo          |
    +-------------+------------+---------------------+
    | 68          | Ab4        | Low Agogo           |
    +-------------+------------+---------------------+
    | 69          | A4         | Cabasa              |
    +-------------+------------+---------------------+
    | 70          | Bb4        | Maracas             |
    +-------------+------------+---------------------+
    | 71          | B4         | Short Whistle       |
    +-------------+------------+---------------------+
    | 72          | C5         | Long Whistle        |
    +-------------+------------+---------------------+
    | 73          | C#5        | Short Guiro         |
    +-------------+------------+---------------------+
    | 74          | D5         | Long Guiro          |
    +-------------+------------+---------------------+
    | 75          | Eb5        | Claves              |
    +-------------+------------+---------------------+
    | 76          | E5         | Hi Wood Block       |
    +-------------+------------+---------------------+
    | 77          | F5         | Low Wood Block      |
    +-------------+------------+---------------------+
    | 78          | F#5        | Mute Cuica          |
    +-------------+------------+---------------------+
    | 79          | G5         | Open Cuica          |
    +-------------+------------+---------------------+
    | 80          | Ab5        | Mute Triangle       |
    +-------------+------------+---------------------+
    | 81          | A5         | Open Triangle       |
    +-------------+------------+---------------------+


.. tab:: CC

    TODO.


