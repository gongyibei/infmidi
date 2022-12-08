from infmidi import Clip, sheet, FluidSynth


clip = Clip()

txt = '''
    A2 E3 G3 - F2 C3 E3 - |
    G2 D3 F3 - C3 G3 B3 - 
'''
clip += sheet(txt) ** 2

txt = '''
    D5 - (E5 D5) C5 D5 G4 (E5 D5) C5 |
    D5 - (E5 D5) C5 C5 G5 D5      -  |
    D5 - (E5 D5) C5 D5 G4 (E5 D5) C5 |
    D5 - (E5 D5) C5 C5 -  B4      -  
'''
clip += sheet(txt)

synth = FluidSynth()
synth(clip, bpm=80)