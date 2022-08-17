import numpy as np
from notation import *
from data import readChordData

MAJOR_STEPS = [W, W, H, W, W, W, H]

def ChordBuilder(*steps):
    '''Returns a function that takes a root note and returns the chord defined by the steps given'''
    if(len(steps) == 0):
        return lambda root: [root]
    return lambda root: [root] + ChordBuilder(*steps[1:])(step(root, steps[0]))

def ChordBuilderAbsolute(steps):
    '''Returns a function that takes a root note and returns the chord defined by the steps given in relation to the root note'''
    return lambda root: [step(root, s) for s in steps]


def GetAscendingVoicing(chord):
    '''Returns voicing (array of octave number of each note) of chord such that each next note is higher than the last'''
    voicing = [0]*len(chord)
    i = 0
    for note in chord[1:]:
        while frequency(note, voicing[i+1]) < frequency(chord[i], voicing[i]):
            voicing[i+1]+=1
    return voicing

def ChordBuilders(data):
    for name, intervals in data.items():
        data[name] = ChordBuilderAbsolute(intervals)
    return data

CHORD_TYPES = ChordBuilders(readChordData())

def defineScale(root, steps=MAJOR_STEPS):
    '''Creates a list of notes in a scale with root as root note and formula steps (list of step counts up)'''
    if(steps == []):
        return []
    return [root] + defineScale(step(root, steps[0]), steps[1:])

class Scale:
    def __len__(self):
        return self.scale.length
    
    def __str__(self):
        return str(self.scale)

    def __init__(self, root, steps, correctVoicing=True):
        self.scale = defineScale(root, steps)
        self.voicing = (0)*len(self.scale)
        if(correctVoicing):
            self.voicing = GetAscendingVoicing(self.scale)
    
    def __init__(self, scale):
        self.scale = scale
        self.voicing = GetAscendingVoicing(self.scale)
    
    def raiseAtInterval(self, interval, n):
        note = step(self.scale[0], interval)
        try:
            self.scale[self.scale.index(note)] = step(note, n)
            return self
        except:
            return self
    
    def raiseAtNote(self, index, n):
        self.scale[index-1] = step(self.scale[index-1], n)
        return self
    def flat(self, index):
        return self.raiseAtNote(index, -1)
    def sharp(self, index):
        return self.raiseAtNote(index, 1)

    def chordsOfForm(self, form):
        chords = []
        for note in self.scale:
            chord = form(note)
            if(self.hasChord(chord)):
                chords.append(chord)
        return chords
                
    def hasChord(self, chord):
        for note in chord:
            if note not in self.scale:
                return False
        return True
    def chords(self):
        '''Returns list of tuples of form (chord root, chord type, chord notes) that are in the scale'''
        ls = []
        for note in self.scale:
            for ctype in CHORD_TYPES.keys():
                chord = CHORD_TYPES[ctype](note)
                if(self.hasChord(chord)):
                    ls.append((note, ctype, chord))
        return ls
    
    def intervalsOf(self, n):
        '''Returns list of note intervals of interval n in the scale'''
        ls = []
        for note in self.scale:
            other = step(note, n)
            if(other in self.scale):
                ls.append([note, other])
        return ls

def findChords(chord):
    return Scale(chord).chords()

# scale builders
Ionian = lambda root: Scale(root, MAJOR_STEPS)
Dorian = lambda root: Ionian(root).flat(3).flat(7)
Phrygian = lambda root: Ionian(root).flat(2).flat(3).flat(6).flat(7)
Lydian = lambda root: Ionian(root).sharp(4)
Mixolydian = lambda root: Ionian(root).flat(7)
Aeolian = lambda root: Ionian(root).flat(3).flat(6).flat(7)
Locrian = lambda root: Ionian(root).flat(2).flat(3).flat(6).flat(7).flat(5)

HarmonicMinor = lambda root: Aeolian(root).sharp(7)
MelodicMinor = lambda root: HarmonicMinor(root).sharp(6)