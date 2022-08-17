'''tuple of all 12 notes'''
NOTES = ( 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab' )

'''Dictionary of form note name : frequency'''
FREQUENCY_DICT = { 
    'A' : 440, 
    'Bb' : 466.16, 
    'B' : 493.88, 
    'C' : 523.25, 
    'Db' : 554.37, 
    'D' : 587.33, 
    'Eb' : 622.25, 
    'E' : 659.25, 
    'F' : 698.46, 
    'Gb' : 739.99, 
    'G' : 783.99, 
    'Ab' : 830.61 
}

NOTE_INDEX = { 
    'A' : 0, 
    'Bb' : 1, 
    'B' : 2, 
    'C' : 3, 
    'Db' : 4, 
    'D' : 5, 
    'Eb' : 6, 
    'E' : 7, 
    'F' : 8, 
    'Gb' : 9, 
    'G' : 10, 
    'Ab' : 11 
}

INDEX_NOTE = {index:note for note, index in NOTE_INDEX.items()}

'''whole step : 2 semitones'''
W = 2

'''half step : 1 semitone'''
H = 1

Min3 = W+H
Maj3 = 2*W
Perf4 = 2*W+H
Tritone = 3*W
Perf5 = 3*W+H
Min6 = 4*W
Maj6 = 4*W+H
Min7 = 5*W
Maj7 = 5*W+H

'''dictionary containing keys=number of steps and value=name of interval described by key'''
INTERVALS = {
    H: 'Minor 2nd',
    W: 'Major 2nd',
    Min3: 'Minor 3rd',
    Maj3: 'Major 3rd',
    Perf4: 'Perfect 4th',
    Tritone: 'Tritone',
    Perf5: 'Perfect 5th',
    Min6: 'Minor 6th',
    Maj6: 'Major 6th',
    Min7: 'Minor 7th',
    Maj7: 'Major 7th'
}

def step(note, step):
    '''Returns the note that is 
     step half steps higher than the given note.'''
    n = (NOTES.index(note)+step)%12
    return NOTES[n]

def frequency(note, octave=0):
    '''Returns the frequency of the given note at the given octave.'''
    return FREQUENCY_DICT[note]*(2**octave)